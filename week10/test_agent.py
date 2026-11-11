"""Protocol tests use explicit doubles, never claim live model accuracy."""
import copy
from pathlib import Path
import tempfile
import unittest

from agent import Bot, ModelError
from handbook import VectorIndex
from models import Conversation, Store, User


class ScriptedModel:
    def __init__(self, answers):
        self.answers = iter(answers)
        self.requests = []
        self.offered_tools = []

    def chat(self, messages, tools):
        self.requests.append(copy.deepcopy(messages))
        self.offered_tools.append(copy.deepcopy(tools))
        return next(self.answers)


def call(query='lost card'):
    return {'role': 'assistant', 'content': '', 'tool_calls': [
        {'function': {'name': 'retrieve_handbook', 'arguments': {'query': query}}}]}


class ProtocolTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.store = Store(Path(self.temp.name) / 'chat.sqlite')
        self.user = User.create(name='Fictional Ada')
        self.chat = Conversation.create(owner=self.user, title='Test')

    def tearDown(self):
        self.store.close()
        self.temp.cleanup()

    def retrieve(self, query):
        return [{'id': 'test-p1-c1', 'page': 1, 'text': 'Fictional test passage.', 'score': 0.9}]

    def test_real_dispatch_history_reaches_next_call_and_isolates(self):
        model = ScriptedModel([call(), {'role': 'assistant', 'content': 'Example [test-p1-c1]'},
                               call('follow-up'), {'role': 'assistant', 'content': 'Next [test-p1-c1]'}])
        bot = Bot(self.store, model, self.retrieve)
        bot.ask(self.user.id, self.chat.id, 'First question')
        bot.ask(self.user.id, self.chat.id, 'What about that?')
        self.assertIn({'role': 'user', 'content': 'First question'}, model.requests[2])
        self.assertTrue(any(m['role'] == 'tool' for m in model.requests[1]))
        self.assertTrue(model.offered_tools[0])
        self.assertEqual(model.offered_tools[1], [])
        self.assertEqual(len(self.store.history(self.user.id, self.chat.id)), 4)
        second = Conversation.create(owner=self.user, title='Isolated')
        isolated = ScriptedModel([call(), {'role': 'assistant', 'content': 'Other [test-p1-c1]'}])
        Bot(self.store, isolated, self.retrieve).ask(self.user.id, second.id, 'New')
        self.assertNotIn('First question', str(isolated.requests))

    def test_missing_tool_bad_citation_and_failed_retrieval_do_not_save(self):
        for message in [{'role': 'assistant', 'content': 'Invented answer'},
                        {'role': 'assistant', 'content': 'Invented [unknown]'}]:
            with self.subTest(message=message):
                with self.assertRaises(ModelError):
                    Bot(self.store, ScriptedModel([call(), message]), self.retrieve).ask(
                        self.user.id, self.chat.id, 'Question')
        def broken(query):
            raise OSError('Index unavailable')
        with self.assertRaises(OSError):
            Bot(self.store, ScriptedModel([call()]), broken).ask(self.user.id, self.chat.id, 'Question')
        self.assertEqual(self.store.history(self.user.id, self.chat.id), [])

    def test_missing_tool_cannot_be_saved_as_a_grounded_answer(self):
        model = ScriptedModel([{'role': 'assistant', 'content': 'Guess [test-p1-c1]'}])
        with self.assertRaises(ModelError):
            Bot(self.store, model, self.retrieve).ask(self.user.id, self.chat.id, 'Question')
        self.assertEqual(self.store.history(self.user.id, self.chat.id), [])

    def test_unsupported_refusal_has_no_invented_citation(self):
        model = ScriptedModel([call(), {'role': 'assistant', 'content': 'I cannot answer from these sources.'}])
        result = Bot(self.store, model, self.retrieve).ask(self.user.id, self.chat.id, 'Unknown')
        self.assertEqual(result['citations'], [])

    def test_tool_loop_is_bounded(self):
        with self.assertRaises(ModelError):
            Bot(self.store, ScriptedModel([call()] * 4), self.retrieve).ask(
                self.user.id, self.chat.id, 'Loop')
        self.assertEqual(self.store.history(self.user.id, self.chat.id), [])

    def test_vectors_reject_wrong_space_and_bad_numbers(self):
        # Algorithm-only synthetic coordinates; never used as a teaching embedding fixture.
        bundle = {'encoder': {'name': 'test-only', 'digest': 'test', 'dimension': 2},
                  'source': {'title': 'Synthetic unit test', 'year': 'none', 'url': 'test:', 'sha256': 'test'},
                  'chunks': [{'id': 'a', 'page': 1, 'text': 'first', 'vector': [1., 0.]},
                             {'id': 'b', 'page': 2, 'text': 'second', 'vector': [0., 1.]}]}
        index = VectorIndex(bundle)
        self.assertEqual(index.search_vector([0., 1.], bundle['encoder'])[0]['id'], 'b')
        with self.assertRaises(ValueError):
            index.search_vector([0., 1.], {**bundle['encoder'], 'digest': 'other'})
        with self.assertRaises(ValueError):
            index.search_vector([float('nan'), 0.], bundle['encoder'])


if __name__ == '__main__':
    unittest.main()

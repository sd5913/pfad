"""Behavior checks; model doubles are not evidence of live generation."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from models import Store, User, Conversation, Message, IntegrityError


class StoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / 'chat.sqlite'
        self.store = Store(self.path)
        self.user = User.create(name='Ada')
        self.chat = Conversation.create(owner=self.user, title='Handbook')

    def tearDown(self):
        self.store.close()
        self.tmp.cleanup()

    def test_restart_reconstructs_ordered_related_objects(self):
        self.store.append_turn(self.user.id, self.chat.id, 'Hello', 'Hi')
        query = self.store.history_query(self.user.id, self.chat.id)
        sql, params = query.sql()
        self.assertIn('ORDER BY', sql)
        self.assertIn(self.chat.id, params)
        self.store.close()
        code = ('from models import Store; import json; s=Store(__import__("sys").argv[1]); '
                'print(json.dumps(s.history(1,1))); s.close()')
        result = subprocess.run([sys.executable, '-c', code, str(self.path)],
                                cwd=Path(__file__).parent, capture_output=True, text=True, check=True)
        self.assertEqual(json.loads(result.stdout), [
            {'role': 'user', 'content': 'Hello'}, {'role': 'assistant', 'content': 'Hi'}])

    def test_ownership_and_conversation_isolation(self):
        other = User.create(name='Bo')
        second = Conversation.create(owner=self.user, title='Other')
        self.store.append_turn(self.user.id, self.chat.id, 'secret', 'stored')
        self.assertEqual(self.store.history(self.user.id, second.id), [])
        with self.assertRaises(PermissionError):
            self.store.history(other.id, self.chat.id)

    def test_unknown_conversation_has_a_recoverable_error(self):
        with self.assertRaisesRegex(ValueError, 'Conversation not found'):
            self.store.owned_conversation(self.user.id, 999999)

    def test_constraints_and_atomic_rollback(self):
        with self.assertRaises(IntegrityError):
            Message.create(conversation=999, role='user', content='orphan')
        with self.assertRaises(IntegrityError):
            self.store.append_turn(self.user.id, self.chat.id, 'ok', '')
        self.assertEqual(self.store.history(self.user.id, self.chat.id), [])
        with self.assertRaises(IntegrityError):
            Message.create(conversation=self.chat, role='system', content='invalid')
        with self.assertRaises(IntegrityError):
            User.create(name='Ada')

    def test_update_survives_reload_and_index_exists(self):
        self.chat.title = 'Lost card'
        self.chat.save()
        self.assertEqual(Conversation.get_by_id(self.chat.id).title, 'Lost card')
        indexes = self.store.db.execute_sql("PRAGMA index_list('message')").fetchall()
        self.assertTrue(any('conversation_id' in row[1] for row in indexes))

    def test_history_window_keeps_complete_pairs(self):
        for i in range(5):
            self.store.append_turn(self.user.id, self.chat.id, str(i), str(i))
        history = self.store.history(self.user.id, self.chat.id, turns=2)
        self.assertEqual([m['content'] for m in history], ['3', '3', '4', '4'])


if __name__ == '__main__':
    unittest.main()

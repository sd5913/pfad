"""Typed handbook CLI. Requires a verified index and an installed local chat model."""
import argparse
import json
from pathlib import Path

from agent import Bot
from handbook import VectorIndex
from local_model import LlamaServer
from models import Conversation, Store, User
from speech import play, synthesize


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bundle', default='fixtures/handbook.json')
    parser.add_argument('--db', default='out/chat.sqlite')
    parser.add_argument('--user', default='Ada')
    parser.add_argument('--conversation', type=int)
    parser.add_argument('--model', default='handbook-local')
    parser.add_argument('--text-only', action='store_true', help='Labeled fallback: skips speech')
    parser.add_argument('--question', help='One turn, then exit; omit for typed conversation')
    parser.add_argument('--trace', default='out/last-turn.json', help='Fictional exercise trace destination')
    args = parser.parse_args()
    store = None
    try:
        index = VectorIndex.load(args.bundle)
        from encoder import Encoder
        encoder = Encoder()
        if encoder.identity != index.encoder:
            raise ValueError('Sentence encoder does not match this index.')
        def vector(text):
            return encoder.encode([text])[0]
        def retrieve(query):
            return index.search_vector(vector(query), index.encoder)
        model = LlamaServer(args.model)
        model.identity()
        store = Store(args.db)
        user, _ = User.get_or_create(name=args.user)
        chat = (store.owned_conversation(user.id, args.conversation) if args.conversation
                else Conversation.create(owner=user, title='Handbook'))
        print(f'Conversation {chat.id}; user {user.name}. Last 4 complete turns enter each call.')
        print('These fictional local profiles are ownership checks, not authenticated accounts.')
        bot = Bot(store, model, retrieve)
        while True:
            question = args.question or input('Question (empty to stop): ')
            if not question.strip():
                break
            result = bot.ask(user.id, chat.id, question)
            print('TOOL TRACE', json.dumps(result['tools'], ensure_ascii=False, indent=2))
            print('ANSWER', result['answer'])
            trace = Path(args.trace)
            trace.parent.mkdir(parents=True, exist_ok=True)
            trace.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding='utf-8')
            print(f'Saved turn; inspect selected history/tool messages in {trace}.')
            if args.text_only:
                result['speech'] = {'status': 'skipped_text_only'}
                print('TEXT-ONLY FALLBACK: speech was not attempted.')
            else:
                try:
                    result['speech'] = synthesize(result['answer'], 'out/reply.wav')
                    print('SYNTHESIS', result['speech'])
                    result['speech']['playback'] = play('out/reply.wav')
                    result['speech']['audibility'] = 'requires_listener'
                    print('PLAYBACK', result['speech']['playback'])
                except (OSError, RuntimeError, ValueError) as error:
                    result['speech']['error'] = str(error)
                    print(f'SPEECH FAILED: {error}; displayed answer remains saved.')
            trace.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding='utf-8')
            if args.question:
                break
    except (OSError, RuntimeError, ValueError, PermissionError) as error:
        parser.exit(1, f'Bot stopped: {error}\n')
    except (KeyboardInterrupt, EOFError):
        print('\nStopped.')
    finally:
        if store:
            store.close()


if __name__ == '__main__':
    main()

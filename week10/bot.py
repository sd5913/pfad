"""Typed handbook CLI. Requires a verified index and an installed local chat model."""
import argparse
import json
from pathlib import Path

from agent import Bot
from handbook import VectorIndex
from local_model import Ollama
from models import Conversation, Store, User
from speech import play, synthesize


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bundle', default='fixtures/handbook.json')
    parser.add_argument('--db', default='out/chat.sqlite')
    parser.add_argument('--user', default='Ada')
    parser.add_argument('--conversation', type=int)
    parser.add_argument('--model', default='qwen3:4b')
    parser.add_argument('--encoder-path', help='Local cached CLIP snapshot matching the bundle')
    parser.add_argument('--text-only', action='store_true', help='Labeled fallback: skips speech')
    parser.add_argument('--question', help='One turn, then exit; omit for typed conversation')
    args = parser.parse_args()
    store = None
    try:
        index = VectorIndex.load(args.bundle)
        if index.encoder.get('kind') == 'clip-pooler':
            if not args.encoder_path:
                raise ValueError('This CLIP index needs --encoder-path to its local matching snapshot.')
            from prepare_index import ClipEncoder
            encoder = ClipEncoder(args.encoder_path)
            def vector(text):
                return encoder.encode([text])[0]
            if encoder.identity != index.encoder:
                raise ValueError('CLIP snapshot/weights/tokenizer do not match the bundle.')
        else:
            embedding = Ollama(index.encoder['name'])
            def vector(text):
                return embedding.embed(text, index.encoder)
        def retrieve(query):
            return index.search_vector(vector(query), index.encoder)
        model = Ollama(args.model)
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
            Path('out').mkdir(exist_ok=True)
            Path('out/last-turn.json').write_text(json.dumps(result, indent=2, ensure_ascii=False),
                                                  encoding='utf-8')
            print('Saved turn; inspect selected history/tool messages in out/last-turn.json.')
            if args.text_only:
                print('TEXT-ONLY FALLBACK: speech was not attempted.')
            else:
                try:
                    print('SYNTHESIS', synthesize(result['answer'], 'out/reply.wav'))
                    print('PLAYBACK', play('out/reply.wav'))
                except (OSError, RuntimeError, ValueError) as error:
                    print(f'SPEECH FAILED: {error}; displayed answer remains saved.')
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

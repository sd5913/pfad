"""Run seed, inspect and rename as separate processes to expose persistence."""
import argparse
import json

from models import Conversation, IntegrityError, Message, Store, User


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['seed', 'inspect', 'rename', 'invalid'])
    parser.add_argument('--db', default='out/chat.sqlite')
    args = parser.parse_args()
    store = Store(args.db)
    try:
        if args.action == 'seed':
            with store.db.atomic():
                user, _ = User.get_or_create(name='Ada')
                chat, created = Conversation.get_or_create(owner=user, title='Handbook')
                if created:
                    store.append_turn(user.id, chat.id, 'My project is a game.',
                                      'Prepared storage example; no model was called.')
            print(f'user={user.id} conversation={chat.id}; fictional seed, not live generation')
        elif args.action == 'inspect':
            print('ROWS', list(User.select().dicts()), list(Conversation.select().dicts()))
            for chat in Conversation.select():
                query = store.history_query(chat.owner_id, chat.id)
                print('SQL + parameters', query.sql())
                print('ROWS', list(query.dicts()))
                print('MODEL MESSAGES', json.dumps(store.history(chat.owner_id, chat.id)))
            print('INDEXES', store.db.execute_sql("PRAGMA index_list('message')").fetchall())
        elif args.action == 'rename':
            chat = Conversation.get_by_id(1)
            chat.title = 'My game questions'
            chat.save()
            print(f'conversation={chat.id} title={chat.title}')
        else:
            try:
                Message.create(conversation=999999, role='user', content='orphan')
            except IntegrityError as error:
                print('EXPECTED rejection:', error)
            else:
                raise RuntimeError('Foreign-key protection failed.')
    finally:
        store.close()


if __name__ == '__main__':
    main()

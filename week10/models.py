"""The bot's related records. Data survives; these methods stay in Python."""
from pathlib import Path

from peewee import (Check, ForeignKeyField, IntegrityError, Model,
                    SqliteDatabase, TextField)

database = SqliteDatabase(None, pragmas={'foreign_keys': 1})


class Record(Model):
    class Meta:
        database = database


class User(Record):
    name = TextField(unique=True, constraints=[Check("length(trim(name)) > 0")])


class Conversation(Record):
    owner = ForeignKeyField(User, backref='conversations', on_delete='RESTRICT')
    title = TextField()


class Message(Record):
    conversation = ForeignKeyField(Conversation, backref='messages', on_delete='RESTRICT')
    role = TextField(constraints=[Check("role IN ('user', 'assistant')")])
    content = TextField(constraints=[Check("length(trim(content)) > 0")])

    class Meta:
        indexes = ((('conversation', 'id'), False),)


class Store:
    """One SQLite file per process; this classroom CLI has one active writer."""

    def __init__(self, path):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        database.init(str(path))
        database.connect(reuse_if_open=True)
        database.create_tables([User, Conversation, Message])
        self.db = database

    def owned_conversation(self, owner_id, conversation_id):
        chat = Conversation.get_or_none(Conversation.id == conversation_id)
        if chat is None:
            raise ValueError('Conversation not found. Use the printed ID or start a new conversation.')
        if chat.owner_id != owner_id:
            raise PermissionError('This conversation belongs to another user.')
        return chat

    def history_query(self, owner_id, conversation_id):
        self.owned_conversation(owner_id, conversation_id)
        return (Message.select().where(Message.conversation == conversation_id)
                .order_by(Message.id))

    def history(self, owner_id, conversation_id, turns=4):
        if not 1 <= turns <= 20:
            raise ValueError('History window must be 1 to 20 complete turns.')
        query = self.history_query(owner_id, conversation_id)
        # Select the newest bounded window, then restore chronological order.
        rows = list(query.order_by(Message.id.desc()).limit(turns * 2))
        return [{'role': row.role, 'content': row.content} for row in reversed(rows)]

    def append_turn(self, owner_id, conversation_id, question, answer):
        with self.db.atomic():
            self.owned_conversation(owner_id, conversation_id)
            Message.create(conversation=conversation_id, role='user', content=question)
            Message.create(conversation=conversation_id, role='assistant', content=answer)

    def close(self):
        if not self.db.is_closed():
            self.db.close()

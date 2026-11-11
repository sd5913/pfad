PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS user (
  id INTEGER PRIMARY KEY, name TEXT NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS conversation (
  id INTEGER PRIMARY KEY, owner_id INTEGER NOT NULL REFERENCES user(id),
  title TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS message (
  id INTEGER PRIMARY KEY, conversation_id INTEGER NOT NULL REFERENCES conversation(id),
  role TEXT NOT NULL CHECK(role IN ('user', 'assistant')),
  content TEXT NOT NULL CHECK(length(trim(content)) > 0)
);
CREATE INDEX IF NOT EXISTS message_conversation_id ON message(conversation_id, id);
INSERT OR IGNORE INTO user VALUES (1, 'Ada');
INSERT OR IGNORE INTO conversation VALUES (1, 1, 'Handbook');
INSERT OR IGNORE INTO message VALUES (1, 1, 'user', 'Where is my saved conversation?');
INSERT OR IGNORE INTO message VALUES (2, 1, 'assistant', 'This is prepared storage data; no model was called.');

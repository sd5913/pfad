"""Boundary checks: real local HTTP protocol doubles; no model-quality claims."""
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
from pathlib import Path
import sqlite3
import tempfile
import unittest

from handbook import VectorIndex
from qdrant_index import QdrantIndex
from pip_adapter import PipModel
from agent import Bot
from models import Store, User, Conversation, Message


class Bridges(unittest.TestCase):
    def test_pip_transport_tool_loop_preserves_history_and_qdrant_evidence(self):
        requests = []
        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args): pass
            def do_GET(self):
                self.send({'data': [{'id': 'test-local'}]})
            def do_POST(self):
                body = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
                requests.append((self.path, body))
                if body['tools']:
                    self.send({'choices': [{'message': {'role': 'assistant', 'tool_calls': [{
                        'id': 'call-1', 'type': 'function', 'function': {
                            'name': 'retrieve_handbook', 'arguments': '{"query":"lost card"}'}}]}}]})
                else:
                    self.send({'choices': [{'message': {'role': 'assistant', 'content': json.dumps({
                        'answer': 'Test protocol answer', 'source_ids': ['chunk-1']})}}]})
            def send(self, value):
                data = json.dumps(value).encode()
                self.send_response(200); self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(data))); self.end_headers(); self.wfile.write(data)
        server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        thread = Thread(target=server.serve_forever, daemon=True);thread.start()
        self.addCleanup(server.server_close);self.addCleanup(server.shutdown)
        with tempfile.TemporaryDirectory() as tmp:
            store = Store(Path(tmp) / 'history.sqlite')
            self.addCleanup(store.close)
            user=User.create(name='Ada');chat=Conversation.create(owner=user,title='Test')
            store.append_turn(user.id,chat.id,'Earlier question','Earlier answer')
            model=PipModel('test-local',f'http://127.0.0.1:{server.server_port}/v1')
            self.assertEqual(model.identity(),'test-local')
            def retrieve(query):
                self.assertEqual(query,'lost card')
                return [{'id':'chunk-1','text':'Test passage','page':1,'score':.8}]
            result=Bot(store,model,retrieve).ask(user.id,chat.id,'What about it?')
            self.assertTrue(result['saved']);self.assertEqual(Message.select().count(),4)
            self.assertEqual(requests[0][0],'/v1/chat/completions')
            self.assertEqual(requests[0][1]['messages'][1]['content'],'Earlier question')
            self.assertIn('Test passage',requests[1][1]['messages'][-1]['content'])
            self.assertEqual(result['citations'],['chunk-1'])
            def unavailable(query):raise RuntimeError('Qdrant stopped')
            with self.assertRaisesRegex(RuntimeError,'Qdrant stopped'):
                Bot(store,model,unavailable).ask(user.id,chat.id,'Retry')
            self.assertEqual(Message.select().count(),4)

    def test_qdrant_rejects_mismatched_encoder_before_network(self):
        idx=VectorIndex.load(Path(__file__).parent/'fixtures/handbook.json')
        remote=QdrantIndex(idx)
        with self.assertRaisesRegex(ValueError,'Encoder identity'):
            remote.search_vector(idx.queries[0]['vector'],{'dimension':384})
        with self.assertRaises(ValueError):
            remote.search_vector(idx.queries[0]['vector'],idx.encoder,limit=9)

    def test_d1_schema_join_constraints_and_repeat_seed(self):
        db=sqlite3.connect(':memory:');self.addCleanup(db.close)
        schema=(Path(__file__).parent/'d1/schema.sql').read_text()
        db.executescript(schema);db.executescript(schema)
        rows=db.execute('SELECT message.content FROM message JOIN conversation '
                        'ON message.conversation_id=conversation.id WHERE conversation.id=?1 '
                        'ORDER BY message.id',(1,)).fetchall()
        self.assertEqual(len(rows),2)
        with self.assertRaises(sqlite3.IntegrityError):
            db.execute("INSERT INTO message VALUES (3,999,'user','orphan')")
        self.assertEqual(db.execute('SELECT count(*) FROM message').fetchone()[0],2)


if __name__=='__main__':unittest.main()

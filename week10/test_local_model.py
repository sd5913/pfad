"""Loopback protocol checks; this fake HTTP reply is not live model evidence."""
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import threading
import unittest

from agent import TOOL
from local_model import LlamaServer


class AdapterTests(unittest.TestCase):
    def test_retrieval_phase_requires_a_tool_and_answer_phase_offers_none(self):
        received = []

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def do_POST(self):
                received.append(json.loads(self.rfile.read(int(self.headers['Content-Length']))))
                data = received[-1]
                content = ('Protocol test' if data['tools'] else json.dumps({
                    'answer': 'Example statement', 'source_ids': [] if
                    data['messages'][-1]['content'] == 'Unknown' else ['test-p1']}))
                body = json.dumps({'choices': [{'message': {
                    'role': 'assistant', 'content': content}}]}).encode()
                self.send_response(200)
                self.send_header('Content-Length', str(len(body)))
                self.end_headers()
                self.wfile.write(body)

        server = HTTPServer(('127.0.0.1', 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            model = LlamaServer(port=server.server_port)
            model.chat([{'role': 'user', 'content': 'Question'}], [TOOL])
            messages = [{'role': 'tool', 'tool_name': 'retrieve_handbook',
                         'content': json.dumps([{'id': 'test-p1'}])},
                        {'role': 'user', 'content': 'Question'}]
            answer = model.chat(messages, [])
            refusal = model.chat([*messages, {'role': 'user', 'content': 'Unknown'}], [])
            self.assertEqual(received[0]['tool_choice'], 'required')
            self.assertEqual(received[1]['tools'], [])
            self.assertNotEqual(received[1]['tool_choice'], 'required')
            self.assertIn('response_format', received[1])
            self.assertEqual(answer['content'], 'Example statement [test-p1]')
            self.assertEqual(refusal['content'], 'I cannot answer from these sources.')
        finally:
            server.shutdown()
            server.server_close()
            thread.join()


if __name__ == '__main__':
    unittest.main()

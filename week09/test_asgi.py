"""Exercise actual FastAPI routes in memory. This does not test TCP or a browser.

The tiny ASGI driver feeds events directly because the authoring sandbox cannot
open sockets. Awaited input is stepped explicitly; no event loop is simulated.
"""

import json
import unittest

from server import create_app


class Incoming:
    def __await__(self):
        return (yield self)


class Session:
    def __init__(self, app, kind, path, method="GET"):
        self.sent = []
        self.done = False
        scope = {"type": kind, "path": path, "raw_path": path.encode(),
                 "root_path": "", "query_string": b"", "scheme": "http",
                 "headers": [(b"host", b"127.0.0.1:8009"),
                             (b"content-type", b"application/json")],
                 "client": ("127.0.0.1", 1234), "server": ("127.0.0.1", 8009),
                 "asgi": {"version": "3.0", "spec_version": "2.4"},
                 "method": method, "http_version": "1.1", "subprotocols": []}

        async def receive():
            return await Incoming()

        async def send(message):
            self.sent.append(message)

        self.call = app(scope, receive, send)
        self.feed(None)

    def feed(self, event):
        try:
            waiting = self.call.send(event)
            assert isinstance(waiting, Incoming), f"Unexpected await: {waiting}"
        except StopIteration:
            self.done = True

    def close(self):
        if not self.done:
            self.call.close()

    def messages(self):
        events, self.sent = self.sent, []
        return [json.loads(e["text"]) for e in events if e["type"] == "websocket.send"]


class ASGIRouteTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.sessions = []

    def tearDown(self):
        for session in self.sessions:
            session.close()

    def websocket(self):
        session = Session(self.app, "websocket", "/ws")
        self.sessions.append(session)
        session.feed({"type": "websocket.connect"})
        self.assertEqual(session.sent[0]["type"], "websocket.accept")
        return session

    def http(self, path, data=None):
        session = Session(self.app, "http", path, "POST" if data is not None else "GET")
        self.sessions.append(session)
        if data is not None:
            session.feed({"type": "http.request", "body": data, "more_body": False})
        self.assertTrue(session.done)
        status = next(e["status"] for e in session.sent if e["type"] == "http.response.start")
        body = b"".join(e.get("body", b"") for e in session.sent if e["type"] == "http.response.body")
        return status, json.loads(body)

    def test_one_http_action_is_broadcast_to_two_open_sessions(self):
        a, b = self.websocket(), self.websocket()
        self.assertEqual(a.messages(), b.messages())
        code, ack = self.http("/action", b'{"id":"one","action":"set_x","x":25}')
        self.assertEqual(code, 200)
        self.assertEqual(ack, {"type": "ack", "id": "one", "revision": 1})
        expected = [{"type": "state", "x": 25, "revision": 1}]
        self.assertEqual(a.messages(), expected)
        self.assertEqual(b.messages(), expected)
        self.assertEqual(self.http("/state"), (200, expected[0]))

    def test_websocket_action_ack_and_validation_share_http_rules(self):
        a, b = self.websocket(), self.websocket()
        a.messages(); b.messages()
        a.feed({"type": "websocket.receive", "text": '{"id":"two","action":"set_x","x":100}'})
        self.assertEqual(a.messages(), [{"type": "state", "x": 100, "revision": 1},
                                        {"type": "ack", "id": "two", "revision": 1}])
        self.assertEqual(b.messages(), [{"type": "state", "x": 100, "revision": 1}])
        for payload in ('{oops', '[]', '{"id":"bad","action":"set_x","x":101}'):
            a.feed({"type": "websocket.receive", "text": payload})
            self.assertEqual(a.messages()[0]["type"], "rejected")
            self.assertEqual(b.messages(), [])
        a.feed({"type": "websocket.receive", "bytes": b"binary"})
        self.assertEqual(a.messages()[0]["type"], "rejected")
        self.assertEqual(self.http("/state")[1]["revision"], 1)

    def test_disconnect_cleanup_new_snapshot_and_unobserved_ack(self):
        sender, observer = self.websocket(), self.websocket()
        sender.messages(); observer.messages()
        sender.feed({"type": "websocket.receive", "text": '{"id":"lost","action":"set_x","x":73}'})
        # The sender does not inspect its returned messages before disconnecting.
        sender.feed({"type": "websocket.disconnect", "code": 1000})
        observed = observer.messages()
        self.assertEqual(observed, [{"type": "state", "x": 73, "revision": 1}])
        self.assertEqual(self.websocket().messages(), observed)
        self.http("/action", b'{"id":"next","action":"set_x","x":12}')
        self.assertEqual(observer.messages()[0]["revision"], 2)
        self.assertTrue(sender.done)

    def test_malformed_http_unknown_route_and_rejected_action_leave_state_unchanged(self):
        self.assertEqual(self.http("/action", b"{oops")[0], 400)
        self.assertEqual(self.http("/action", b'{"id":"bad","action":"set_x","x":true}')[0], 422)
        self.assertEqual(self.http("/missing")[0], 404)
        self.assertEqual(self.http("/state"), (200, {"type": "state", "x": 50, "revision": 0}))

    def test_rejections_echo_only_recoverable_valid_ids_on_both_transports(self):
        payload = b'{"id":"invalid-action","action":"set_x","x":101}'
        code, response = self.http("/action", payload)
        self.assertEqual(code, 422)
        self.assertEqual(response.get("id"), "invalid-action")
        client = self.websocket()
        client.messages()
        client.feed({"type": "websocket.receive", "text": payload.decode()})
        self.assertEqual(client.messages()[0].get("id"), "invalid-action")
        for data in (b"{broken", b"[]", b'{"id":42}', b'{"id":""}'):
            with self.subTest(data=data):
                self.assertNotIn("id", self.http("/action", data)[1])
                client.feed({"type": "websocket.receive", "text": data.decode()})
                self.assertNotIn("id", client.messages()[0])


if __name__ == "__main__":
    unittest.main()

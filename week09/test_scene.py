"""Real subprocess/loopback checks; no model, browser or remote account required."""

import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import time
import unittest
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from websockets.sync.client import connect

HERE = Path(__file__).resolve().parent


class SharedSceneTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            with socket.socket():
                pass
        except PermissionError as error:
            raise unittest.SkipTest(f"Live loopback check blocked by host socket policy: {error}")

    def setUp(self):
        with socket.socket() as probe:
            probe.bind(("127.0.0.1", 0))
            self.port = int(os.environ.get("WEEK09_TEST_PORT", probe.getsockname()[1]))
        self.base = f"http://127.0.0.1:{self.port}"
        self.ws = f"ws://127.0.0.1:{self.port}/ws"
        self.start_server()

    def start_server(self):
        self.process = subprocess.Popen(
            [sys.executable, str(HERE / "server.py"), "--port", str(self.port)],
            stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True,
        )
        for _ in range(100):
            if self.process.poll() is not None:
                self.fail(f"Server exited: {self.process.stderr.read()}")
            try:
                self.http("/state")
                return
            except (OSError, URLError):
                time.sleep(0.03)
        self.fail("Server was not ready within three seconds")

    def stop_server(self):
        self.process.terminate()
        self.process.wait(timeout=5)
        self.process.stderr.close()

    def tearDown(self):
        if self.process.poll() is None:
            self.stop_server()

    def http(self, path, data=None):
        request = Request(self.base + path, data=data,
                          headers={"Content-Type": "application/json"})
        try:
            response = urlopen(request, timeout=2)
        except HTTPError as error:
            response = error
        with response:
            return response.status, json.loads(response.read())

    def receive(self, client):
        return json.loads(client.recv(timeout=2))

    def action(self, x=25, message_id="check-1"):
        return {"id": message_id, "action": "set_x", "x": x}

    def test_http_accepts_updates_and_both_clients_observe_same_revision(self):
        with connect(self.ws, proxy=None) as a, connect(self.ws, proxy=None) as b:
            self.assertEqual(self.receive(a), self.receive(b))
            code, result = self.http("/action", json.dumps(self.action()).encode())
            self.assertEqual(code, 200)
            self.assertEqual(result, {"type": "ack", "id": "check-1", "revision": 1})
            first, second = self.receive(a), self.receive(b)
            self.assertEqual(first, second)
            self.assertEqual(first, {"type": "state", "x": 25, "revision": 1})
            self.assertEqual(self.http("/state"), (200, first))
        self.assertEqual(self.http("/missing")[0], 404)

    def test_rejected_http_and_websocket_inputs_do_not_change_state(self):
        initial = self.http("/state")[1]
        invalid = [self.action(-1), self.action(101), self.action(True),
                   self.action("25"), {"action": "set_x", "x": 10},
                   {**self.action(), "extra": 1},
                   {**self.action(), "action": "jump"}, [], None]
        with connect(self.ws, proxy=None) as client:
            self.receive(client)
            for data in invalid:
                with self.subTest(data=data):
                    code, result = self.http("/action", json.dumps(data).encode())
                    self.assertEqual(code, 422)
                    self.assertEqual(result["type"], "rejected")
                    client.send(json.dumps(data))
                    self.assertEqual(self.receive(client)["type"], "rejected")
                    self.assertEqual(self.http("/state")[1], initial)
            client.send("{not json")
            self.assertEqual(self.receive(client)["type"], "rejected")
            client.send(b"binary")
            self.assertEqual(self.receive(client)["type"], "rejected")
            self.assertEqual(self.http("/action", b"{broken")[0], 400)
            self.assertEqual(self.http("/state")[1], initial)

    def test_websocket_disconnect_and_reconnect_receive_fresh_snapshot(self):
        with connect(self.ws, proxy=None) as observer:
            self.receive(observer)
            with connect(self.ws, proxy=None) as sender:
                self.receive(sender)
                sender.send(json.dumps(self.action(80)))
                self.assertEqual(self.receive(sender), self.receive(observer))
                self.assertEqual(self.receive(sender)["type"], "ack")
            code, _ = self.http("/action", json.dumps(self.action(0, "after-close")).encode())
            self.assertEqual(code, 200)
            latest = self.receive(observer)
            self.assertEqual(latest["revision"], 2)
            with connect(self.ws, proxy=None) as reconnected:
                self.assertEqual(self.receive(reconnected), latest)

    def test_missing_observed_ack_does_not_imply_action_failed(self):
        with connect(self.ws, proxy=None) as observer:
            self.receive(observer)
            with connect(self.ws, proxy=None) as sender:
                self.receive(sender)
                sender.send(json.dumps(self.action(73, "unobserved")))
                # Observer proves processing; sender deliberately never reads its acknowledgement.
                changed = self.receive(observer)
                self.assertEqual(changed["x"], 73)
            with connect(self.ws, proxy=None) as reconnected:
                self.assertEqual(self.receive(reconnected), changed)
            self.assertEqual(self.http("/state")[1]["revision"], 1)

    def test_stopped_server_refuses_connection_and_restart_resets_ram(self):
        self.http("/action", json.dumps(self.action(95)).encode())
        self.stop_server()
        with self.assertRaises(URLError):
            self.http("/state")
        self.start_server()
        self.assertEqual(self.http("/state")[1], {"type": "state", "x": 50, "revision": 0})


if __name__ == "__main__":
    unittest.main()

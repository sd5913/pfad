"""Local smoke test: python -m unittest discover -s week09 -p 'test_*.py'."""

import os
import re
import signal
import socket
import subprocess
import sys
import unittest
from pathlib import Path
from selectors import DefaultSelector, EVENT_READ


HERE = Path(__file__).resolve().parent


class EchoSmokeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        try:
            with socket.socket():
                pass
        except PermissionError as error:
            raise unittest.SkipTest(f"TCP check blocked by host socket policy: {error}")

    def test_messages_reconnect_and_stopped_server(self):
        server = subprocess.Popen(
            [sys.executable, "-u", str(HERE / "echo_server.py"), "--port", "0"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        try:
            with DefaultSelector() as selector:
                selector.register(server.stdout, EVENT_READ)
                self.assertTrue(selector.select(timeout=5), "server did not start")
                ready = server.stdout.readline()
            match = re.fullmatch(r"Listening on 127\.0\.0\.1:(\d+)\n", ready)
            self.assertIsNotNone(match, f"server did not listen: {ready!r}")
            port = int(match.group(1))

            # A TCP read is not necessarily one send: frame with newlines.
            with socket.create_connection(("127.0.0.1", port), timeout=3) as connection:
                connection.settimeout(3)
                connection.sendall(b"red\nblue\n")
                with connection.makefile("rb") as replies:
                    self.assertEqual(replies.readline(), b"red\n")
                    self.assertEqual(replies.readline(), b"blue\n")
                    connection.sendall(b"or")
                    connection.sendall(b"ange\n")
                    self.assertEqual(replies.readline(), b"orange\n")
            with socket.create_connection(("127.0.0.1", port), timeout=3) as connection:
                connection.settimeout(3)
                connection.sendall(b"green\n")
                with connection.makefile("rb") as replies:
                    self.assertEqual(replies.readline(), b"green\n")

            client = subprocess.run(
                [sys.executable, str(HERE / "echo_client.py"), "--port", str(port)],
                capture_output=True, text=True, timeout=12,
            )
            self.assertEqual(client.returncode, 0, client.stderr)
            self.assertLess(client.stdout.index("received: red"), client.stdout.index("received: blue"))
            self.assertLess(client.stdout.index("received: blue"), client.stdout.index("received: green"))
            self.assertIn("reconnected", client.stdout)

            paused = subprocess.Popen(
                [sys.executable, "-u", str(HERE / "echo_client.py"),
                 "--port", str(port), "--pause-before-blue"],
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                text=True,
            )
            try:
                with DefaultSelector() as selector:
                    selector.register(paused.stdout, EVENT_READ)
                    output = b""
                    while b"received: red\n" not in output:
                        self.assertTrue(selector.select(timeout=5), "paused client did not receive red")
                        output += os.read(paused.stdout.fileno(), 4096)
                server.send_signal(signal.SIGINT)
                self.assertEqual(server.wait(timeout=5), 0, server.stderr.read())
                remaining, errors = paused.communicate(input="\n", timeout=8)
                self.assertNotEqual(paused.returncode, 0)
                self.assertIn("No reply", errors)
                self.assertNotIn("received: blue", output.decode() + remaining)
            finally:
                if paused.poll() is None:
                    paused.kill()
                    paused.communicate(timeout=5)

            failed = subprocess.run(
                [sys.executable, str(HERE / "echo_client.py"), "--port", str(port)],
                capture_output=True, text=True, timeout=8,
            )
            self.assertNotEqual(failed.returncode, 0)
            self.assertIn("No reply", failed.stderr)
            self.assertNotIn("received:", failed.stdout)
        finally:
            if server.poll() is None:
                server.kill()
                server.wait(timeout=5)
            server.stdout.close()
            server.stderr.close()


if __name__ == "__main__":
    unittest.main()

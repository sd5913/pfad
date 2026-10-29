"""No-process fault injection for the CLI's request/cleanup failure precedence."""
import contextlib
import io
import sys
import unittest
from unittest.mock import patch

import mcp_client


@contextlib.contextmanager
def failed_close(body_error=None):
    cleanup_error = RuntimeError("injected cleanup failure")

    class Transport:
        def request(self, method, params=None):
            if method == "initialize":
                return {"protocolVersion":"2024-11-05", "capabilities":{"tools":{}},
                        "serverInfo":{"name":"fault-injection", "version":"1.0"}}
            if method == "tools/list":
                if body_error is not None:
                    raise body_error
                return {"tools":[]}
            raise AssertionError(f"Unexpected request: {method}")

        def send(self, message):
            if message != {"method":"notifications/initialized"}:
                raise AssertionError(f"Unexpected notification: {message}")

        def close(self):
            raise cleanup_error

    stderr = io.StringIO()
    with patch.object(mcp_client, "Session", return_value=Transport()), \
            patch.object(sys, "argv", ["mcp_client.py", "--blender", "list"]), \
            contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(stderr):
        yield cleanup_error, stderr


class ClientStatusTests(unittest.TestCase):
    def test_successful_list_propagates_cleanup_only_failure(self):
        with failed_close() as (cleanup_error, stderr):
            with self.assertRaises(RuntimeError) as caught:
                mcp_client.main()
        self.assertIs(caught.exception, cleanup_error)
        self.assertIn("Bridge cleanup failed: injected cleanup failure", stderr.getvalue())

    def test_request_failure_survives_secondary_cleanup_failure(self):
        body_error = RuntimeError("injected request failure")
        with failed_close(body_error) as (_, stderr):
            with self.assertRaises(RuntimeError) as caught:
                mcp_client.main()
        self.assertIs(caught.exception, body_error)
        self.assertIn("Bridge cleanup failed: injected cleanup failure", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()

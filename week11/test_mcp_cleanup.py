"""Check owned process cleanup, including real community-bridge failures."""
import contextlib
import io
import os
from pathlib import Path
import shutil
import signal
import sys
import tempfile
import threading
import time
import unittest
from unittest.mock import patch

import mcp_client


def running(pid):
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    stat = Path(f"/proc/{pid}/stat")
    return not stat.exists() or stat.read_text().split()[2] != "Z"


def wait_for_pid(path):
    deadline = time.monotonic() + 10
    while time.monotonic() < deadline:
        if path.exists():
            return int(path.read_text())
        time.sleep(0.02)
    raise AssertionError("runtime did not start")


@unittest.skipUnless(os.name == "posix", "POSIX process-group regression")
class CleanupTests(unittest.TestCase):
    def test_close_kills_stubborn_child_after_server_exits(self):
        with tempfile.TemporaryDirectory() as directory:
            pidfile = Path(directory) / "runtime.pid"
            child = ("import os, pathlib, signal, time; "
                     "signal.signal(signal.SIGINT, signal.SIG_IGN); "
                     "signal.signal(signal.SIGTERM, signal.SIG_IGN); "
                     f"pathlib.Path({str(pidfile)!r}).write_text(str(os.getpid())); "
                     "time.sleep(60)")
            server = f"import subprocess, sys; subprocess.Popen([sys.executable, '-c', {child!r}])"
            session = mcp_client.Session([sys.executable, "-c", server])
            pid = wait_for_pid(pidfile)
            closer = threading.Thread(target=session.close, daemon=True)
            try:
                session.process.wait(timeout=5)
                closer.start()
                closer.join(timeout=15)
                self.assertFalse(running(pid), "owned runtime survived the exited server")
                self.assertFalse(closer.is_alive(), "close exceeded its cleanup budget")
            finally:
                if running(pid):
                    os.kill(pid, signal.SIGKILL)
                closer.join(timeout=5)

    @unittest.skipUnless((mcp_client.ROOT / ".tools/godot-mcp/index.ts").exists()
                         and shutil.which("godot") and shutil.which("node"),
                         "install the pinned bridge and Godot for live cleanup checks")
    def test_demo_error_stops_actual_bridge_runtime_and_preserves_error(self):
        for broken_stop in (False, True):
            with self.subTest(broken_stop=broken_stop), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                shutil.copytree(mcp_client.ROOT / "godot", root / "godot",
                                ignore=shutil.ignore_patterns(".godot", "probe.tscn"))
                (root / ".tools").mkdir()
                (root / ".tools/godot-mcp").symlink_to(mcp_client.ROOT / ".tools/godot-mcp",
                                                       target_is_directory=True)
                pidfile = root / "runtime.pid"
                wrapper = root / "godot-headless"
                wrapper.write_text(
                    f"#!{sys.executable}\nimport os, pathlib, sys\n"
                    "if '--version' not in sys.argv and '--headless' not in sys.argv:\n"
                    f"    pathlib.Path({str(pidfile)!r}).write_text(str(os.getpid()))\n"
                    f"os.execv({shutil.which('godot')!r}, ['godot', '--headless', *sys.argv[1:]])\n")
                wrapper.chmod(0o755)
                sessions = []
                stopped_before_close = []

                class FailingSession(mcp_client.Session):
                    def __init__(self, command):
                        super().__init__(command, env={"GODOT_PATH":str(wrapper)})
                        sessions.append(self)

                    def request(self, method, params=None, timeout=120):
                        name = (params or {}).get("name")
                        if name == "get_debug_output":
                            raise RuntimeError("injected post-launch failure")
                        if name == "stop_project" and broken_stop:
                            raise TimeoutError("injected unresponsive stop")
                        return super().request(method, params, timeout)

                    def close(self):
                        if not broken_stop and pidfile.exists():
                            deadline = time.monotonic() + 2
                            while running(int(pidfile.read_text())) and time.monotonic() < deadline:
                                time.sleep(0.02)
                            stopped_before_close.append(not running(int(pidfile.read_text())))
                        super().close()

                try:
                    with patch.object(mcp_client, "ROOT", root), \
                            patch.object(mcp_client, "Session", FailingSession), \
                            patch.object(sys, "argv", ["mcp_client.py", "demo"]), \
                            contextlib.redirect_stdout(io.StringIO()), \
                            contextlib.redirect_stderr(io.StringIO()):
                        with self.assertRaisesRegex(RuntimeError, "injected post-launch failure"):
                            mcp_client.main()
                    pid = wait_for_pid(pidfile)
                    self.assertFalse(running(pid), "actual Godot runtime survived demo failure")
                    self.assertIsNotNone(sessions[0].process.poll())
                    if not broken_stop:
                        self.assertEqual(stopped_before_close, [True],
                                         "stop_project did not stop Godot before transport cleanup")
                finally:
                    if pidfile.exists() and running(int(pidfile.read_text())):
                        os.kill(int(pidfile.read_text()), signal.SIGKILL)


if __name__ == "__main__":
    unittest.main()

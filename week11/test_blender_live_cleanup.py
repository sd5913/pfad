"""Failure-path shutdown checks with a real disposable child process."""
import contextlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import blender_live


class BlenderCleanupTests(unittest.TestCase):
    def run_failed_close(self, body_error=None):
        cleanup_error = RuntimeError("injected bridge cleanup failure")
        real_popen = subprocess.Popen
        processes = []
        logs = []
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output = root / ".output"
            tools = root / ".tools"
            tools.mkdir()
            (tools / "blender-addon.py").touch()
            bridge = tools / "blender-env" / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")
            bridge.parent.mkdir(parents=True)
            bridge.touch()

            def launch_application(command, **kwargs):
                logs.append(kwargs["stdout"])
                script = (
                    "import pathlib, time\n"
                    f"output = pathlib.Path({str(output)!r})\n"
                    "(output / 'blender-live-ready.json').write_text('{}')\n"
                    "while not (output / 'blender-live-stop').exists():\n"
                    "    time.sleep(0.01)\n"
                    "(output / 'application-exited').touch()\n"
                )
                process = real_popen([sys.executable, "-c", script], **kwargs)
                processes.append(process)
                return process

            class Transport:
                def request(self, method, params=None):
                    if method == "initialize":
                        if body_error is not None:
                            raise body_error
                        return {}
                    if method == "tools/list":
                        return {"tools": []}
                    (output / "blender").mkdir(exist_ok=True)
                    (output / "blender/sculpture-live.png").touch()
                    (output / "blender-live-inspection.json").write_text(json.dumps({"scale": [1.5, 1.5, 1.5]}))
                    return {}

                def send(self, message):
                    pass

                def close(self):
                    raise cleanup_error

            stderr = io.StringIO()
            try:
                with patch.object(blender_live, "ROOT", root), \
                        patch.object(blender_live, "OUTPUT", output), \
                        patch.object(blender_live, "Session", return_value=Transport()), \
                        patch.object(blender_live.subprocess, "run", return_value=subprocess.CompletedProcess([], 0)), \
                        patch.object(blender_live.subprocess, "Popen", side_effect=launch_application), \
                        patch.object(sys, "argv", ["blender_live.py", "--verify"]), \
                        contextlib.redirect_stderr(stderr):
                    with self.assertRaises(RuntimeError) as caught:
                        blender_live.main()
                self.assertTrue((output / "blender-live-stop").exists())
                self.assertTrue((output / "application-exited").exists())
                self.assertEqual(processes[0].poll(), 0)
                self.assertTrue(logs[0].closed)
                self.assertTrue((output / "blender-live-trace.json").is_file())
                self.assertIs(caught.exception, body_error if body_error is not None else cleanup_error)
                self.assertIn("Bridge cleanup failed:", stderr.getvalue())
            finally:
                for process in processes:
                    if process.poll() is None:
                        process.terminate()
                    process.wait(timeout=5)
                for log in logs:
                    log.close()

    def test_bridge_cleanup_failure_still_stops_application(self):
        self.run_failed_close()

    def test_request_failure_survives_bridge_cleanup_failure(self):
        self.run_failed_close(RuntimeError("injected request failure"))


if __name__ == "__main__":
    unittest.main()

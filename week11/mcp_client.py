"""Small human-directed MCP stdio client, not an autonomous model agent."""
import argparse
import json
import os
from pathlib import Path
import queue
import signal
import subprocess
import sys
import threading
import time

ROOT = Path(__file__).resolve().parent


class Session:
    def __init__(self, command, env=None):
        environment = {**os.environ, "XDG_DATA_HOME":str(ROOT / ".output/data"), **(env or {})}
        self.process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE, text=True, env=environment,
                                        start_new_session=os.name == "posix")
        self.messages = queue.Queue()
        self.errors = []
        def read_messages():
            for line in self.process.stdout:
                try:
                    self.messages.put(json.loads(line))
                except ValueError:
                    self.messages.put({"invalid_stdout":line})
        self.reader = threading.Thread(target=read_messages, daemon=True)
        self.error_reader = threading.Thread(target=lambda:self.errors.extend(self.process.stderr), daemon=True)
        self.reader.start()
        self.error_reader.start()
        self.number = 0

    def send(self, message):
        self.process.stdin.write(json.dumps({"jsonrpc":"2.0", **message}) + "\n")
        self.process.stdin.flush()

    def request(self, method, params=None, timeout=120):
        self.number += 1
        number = self.number
        self.send({"id":number, "method":method, "params":params or {}})
        deadline = time.monotonic() + timeout
        for _ in range(100):
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise TimeoutError(f"{method}: no matching response before deadline")
            try:
                message = self.messages.get(timeout=remaining)
            except queue.Empty as error:
                raise TimeoutError(f"{method}: no matching response before deadline") from error
            if message.get("id") == number:
                if "error" in message:
                    raise RuntimeError(message["error"])
                return message["result"]
        raise RuntimeError("no response with the request ID")

    def close(self):
        # The bridge's SIGINT handler stops Godot; EOF/SIGTERM alone do not.
        # Own a separate group so fallback cleanup also reaches orphaned children.
        if os.name == "posix":
            for sig in (signal.SIGINT, signal.SIGTERM, signal.SIGKILL):
                try:
                    os.killpg(self.process.pid, sig)
                except ProcessLookupError:
                    break
                deadline = time.monotonic() + 2
                while time.monotonic() < deadline:
                    self.process.poll()
                    try:
                        os.killpg(self.process.pid, 0)
                    except ProcessLookupError:
                        break
                    time.sleep(0.02)
                else:
                    continue
                break
        elif self.process.poll() is None:
            # Keep the server alive until taskkill can identify its descendants.
            try:
                subprocess.run(["taskkill", "/PID", str(self.process.pid), "/T", "/F"],
                               capture_output=True, timeout=5, check=False)
            except (OSError, subprocess.TimeoutExpired) as error:
                print(f"Process-tree cleanup: {error}", file=sys.stderr)
        try:
            self.process.stdin.close()
        except OSError:
            pass
        try:
            self.process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            self.process.kill()
            self.process.wait(timeout=2)
        self.reader.join(timeout=1)
        self.error_reader.join(timeout=1)
        # Closing a pipe while another thread reads it can block indefinitely.
        for reader, stream in ((self.reader, self.process.stdout),
                               (self.error_reader, self.process.stderr)):
            if not reader.is_alive():
                stream.close()
            else:
                print("Cleanup: a bridge output pipe remains open", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tool", nargs="?", default="list")
    parser.add_argument("arguments", nargs="?", default="{}")
    parser.add_argument("--blender", action="store_true", help="Use the course-owned Blender CLI adapter")
    args = parser.parse_args()
    entry = ROOT / ".tools/godot-mcp/index.ts"
    if not args.blender and not entry.exists():
        raise SystemExit("Install the pinned third-party bridge first; see README / MCP setup.")
    command = ["python", str(ROOT / "blender_tools.py")] if args.blender else ["node", str(entry)]
    session = Session(command)
    launch_attempted = False
    try:
        print(json.dumps({"initialize":session.request("initialize", {"protocolVersion":"2024-11-05", "capabilities":{}, "clientInfo":{"name":"pfad-human-client", "version":"1.0"}})}))
        session.send({"method":"notifications/initialized"})
        if args.tool == "list":
            print(json.dumps(session.request("tools/list"), indent=2))
        elif args.tool == "demo":
            project = str(ROOT / "godot")
            calls = [("get_project_info", {"projectPath":project}),
                ("create_scene", {"projectPath":project, "scenePath":"probe.tscn", "rootNodeType":"Node2D"}),
                ("add_node", {"projectPath":project, "scenePath":"probe.tscn", "parentNodePath":".", "nodeType":"Node2D", "nodeName":"Marker"}),
                ("add_node", {"projectPath":project, "scenePath":"probe.tscn", "parentNodePath":".", "nodeType":"Label", "nodeName":"Caption", "properties":{"text":"THREE LIGHTS"}}),
                ("run_project", {"projectPath":project}), ("get_debug_output", {})]
            for name, arguments in calls:
                if name == "run_project":
                    launch_attempted = True
                result = session.request("tools/call", {"name":name, "arguments":arguments})
                print(json.dumps({"tool":name, "arguments":arguments, "result":result}))
                if result.get("isError"):
                    raise RuntimeError(result)
                if name == "run_project":
                    time.sleep(2)
        else:
            result = session.request("tools/call", {"name":args.tool, "arguments":json.loads(args.arguments)})
            print(json.dumps(result, indent=2))
            if result.get("isError"):
                raise SystemExit(1)
    finally:
        if launch_attempted:
            try:
                result = session.request("tools/call", {"name":"stop_project", "arguments":{}}, timeout=5)
                print(json.dumps({"tool":"stop_project", "result":result}))
                if result.get("isError"):
                    print(f"Project cleanup failed: {result}", file=sys.stderr)
            except Exception as error:
                print(f"Project cleanup failed: {error}", file=sys.stderr)
        try:
            session.close()
        except Exception as error:
            print(f"Bridge cleanup failed: {error}", file=sys.stderr)


if __name__ == "__main__":
    main()

"""Small human-directed MCP stdio client, not an autonomous model agent."""
import argparse
import json
import os
from pathlib import Path
import queue
import subprocess
import threading

ROOT = Path(__file__).resolve().parent


class Session:
    def __init__(self, command):
        environment = {**os.environ, "XDG_DATA_HOME":str(ROOT / ".output/data")}
        self.process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE, text=True, env=environment)
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

    def request(self, method, params=None):
        self.number += 1
        number = self.number
        self.send({"id":number, "method":method, "params":params or {}})
        for _ in range(100):
            message = self.messages.get(timeout=120)
            if message.get("id") == number:
                if "error" in message:
                    raise RuntimeError(message["error"])
                return message["result"]
        raise RuntimeError("no response with the request ID")

    def close(self):
        self.process.stdin.close()
        try:
            self.process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.process.terminate()
            self.process.wait(timeout=5)
        self.reader.join(timeout=1)
        self.error_reader.join(timeout=1)
        self.process.stdout.close()
        self.process.stderr.close()


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
                ("run_project", {"projectPath":project}), ("get_debug_output", {}), ("stop_project", {})]
            for name, arguments in calls:
                result = session.request("tools/call", {"name":name, "arguments":arguments})
                print(json.dumps({"tool":name, "arguments":arguments, "result":result}))
        else:
            result = session.request("tools/call", {"name":args.tool, "arguments":json.loads(args.arguments)})
            print(json.dumps(result, indent=2))
            if result.get("isError"):
                raise SystemExit(1)
    finally:
        session.close()


if __name__ == "__main__":
    main()

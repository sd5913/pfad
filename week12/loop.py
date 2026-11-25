"""Bounded host for human-selected tools. It never chooses a repair or calls a model."""
import argparse
import hashlib
import json
from pathlib import Path
import time

import world

SESSION = world.OUTPUT / "session.json"


class Session:
    def __init__(self, path=SESSION, clock=time.time):
        self.path = Path(path)
        self.clock = clock

    def read(self):
        if not self.path.exists():
            raise ValueError("start a session first: uv run python loop.py start")
        return json.loads(self.path.read_text())

    def save(self, state):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(state, indent=2) + "\n")

    def start(self):
        if self.path.exists() and self.read()["status"] == "active":
            raise ValueError("session is active; stop it before starting another")
        state = {"route": "human-directed local tools; no model client", "started": self.clock(),
                 "status": "active", "actions": 0, "mutations": 0, "events": [],
                 "limits": {"actions": 8, "mutations": 4, "elapsed_seconds": 180}}
        self.save(state)
        return state

    def stop(self, reason):
        state = self.read()
        state["status"] = "stopped"
        state["stop_reason"] = reason
        self.save(state)
        return state

    def run(self, action, key=None, value=None):
        state = self.read()
        if state["status"] != "active":
            raise ValueError(f"session {state['status']}; no further tool action")
        if action not in ("inspect", "set", "check"):
            raise ValueError("only inspect, set and check are bounded tools")
        if self.clock() - state["started"] > 180:
            raise ValueError("session time limit reached; stop and ask a person for help")
        if state["actions"] >= 8:
            raise ValueError("session action limit reached; stop")
        if action == "set" and state["mutations"] >= 4:
            raise ValueError("session mutation limit reached; stop")
        state["actions"] += 1
        if action == "set":
            state["mutations"] += 1
        event = {"action": action, "key": key, "value": value, "time": self.clock()}
        event["config_sha256_before"] = hashlib.sha256(world.CONFIG.read_bytes()).hexdigest()
        # Reserve the action before execution, so a failed tool still consumes budget.
        state["events"].append(event)
        self.save(state)
        try:
            if action == "inspect":
                result = world.inspect()
            elif action == "set":
                result = world.update_config(world.CONFIG, key, value)
            else:
                result = world.check()
            event["observation"] = result
            if action == "check" and "checks" not in result:
                raise RuntimeError("engine returned no structured WORLD_CHECK observation; stop and inspect its errors")
            if action == "check" and result["passed"]:
                state["status"] = "passed"
                state["stop_reason"] = "behavior checks passed; stop edits, inspect evidence before capture"
        except (OSError, ValueError, RuntimeError) as error:
            event["error"] = str(error)
            state["status"] = "blocked"
            state["stop_reason"] = "tool error; inspect the error with a person"
            self.save(state)
            raise
        event["config_sha256_after"] = hashlib.sha256(world.CONFIG.read_bytes()).hexdigest()
        self.save(state)
        return {"observation": result, "status": state["status"], "actions": state["actions"],
                "mutations": state["mutations"]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["start", "inspect", "set", "check", "status", "stop"])
    parser.add_argument("key", nargs="?")
    parser.add_argument("value", nargs="?", type=float)
    args = parser.parse_args()
    session = Session()
    try:
        if args.action == "start":
            result = session.start()
        elif args.action == "status":
            result = session.read()
        elif args.action == "stop":
            result = session.stop(args.key or "human requested stop")
        else:
            result = session.run(args.action, args.key, args.value)
        print(json.dumps(result, indent=2))
        if args.action == "check" and not result["observation"]["passed"]:
            raise SystemExit(1)
    except (OSError, ValueError, RuntimeError) as error:
        parser.exit(2, f"tool stopped: {error}\n")


if __name__ == "__main__":
    main()

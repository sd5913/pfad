"""Read the supplied recorded model observations. Never executes tools or calls a model."""
import json
from pathlib import Path


def main():
    episode = json.loads(Path(__file__).with_name("model-episode.json").read_text())
    print(episode["kind"])
    print(json.dumps(episode["provenance"], indent=2))
    for record in episode["records"]:
        print(f"\n{record['time']}  {record['step']}")
        print("MODEL REASON:", record["model_selected_reason"])
        if "command" in record:
            print("RECORDED ACTION:", " ".join(record["command"]))
            print("RECORDED EXIT:", record["returncode"])
            print("RECORDED STDOUT:", record["stdout"], end="")
            if record["stderr"]:
                print("RECORDED STDERR:", record["stderr"])
        else:
            print(json.dumps({key: value for key, value in record.items()
                              if key not in ("time", "step", "model_selected_reason")}, indent=2))
    print("\nCURRENT EVIDENCE LIMIT:", json.dumps(episode["gate"]))


if __name__ == "__main__":
    main()

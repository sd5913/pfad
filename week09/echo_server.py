"""One-laptop TCP echo service. Newline ends each message; Ctrl+C stops it."""

import argparse
import socket
import sys


HOST = "127.0.0.1"  # Loopback only: never accept connections from other computers.
DEFAULT_PORT = 8765
MAX_LINE = 256


def main(port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
            listener.bind((HOST, port))
            listener.listen()
            print(f"Listening on {HOST}:{listener.getsockname()[1]}", flush=True)
            while True:
                connection, _address = listener.accept()
                with connection:
                    try:
                        connection.settimeout(10)
                        with connection.makefile("rb") as lines:
                            while True:
                                line = lines.readline(MAX_LINE + 1)
                                if not line:  # The client closed this connection.
                                    break
                                if len(line) > MAX_LINE or not line.endswith(b"\n"):
                                    print("Dropped incomplete or oversized message", flush=True)
                                    break
                                connection.sendall(line)
                    except OSError:
                        print("Client disconnected or timed out", flush=True)
    except KeyboardInterrupt:
        print("Stopped")
    except OSError as error:
        print(f"Server unavailable on {HOST}:{port}: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    sys.exit(main(parser.parse_args().port))

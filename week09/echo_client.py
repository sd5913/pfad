"""Send two invented messages, close, reconnect, and send one more."""

import argparse
import socket
import sys


HOST = "127.0.0.1"
DEFAULT_PORT = 8765


def send_and_check(connection, reply_lines, text):
    connection.sendall(text.encode("ascii") + b"\n")
    print(f"sent: {text}", flush=True)
    reply = reply_lines.readline(257)
    if reply != text.encode("ascii") + b"\n":
        raise ConnectionError("missing or unexpected echo")
    print(f"received: {text}", flush=True)


def main(port, pause_before_blue=False):
    try:
        with socket.create_connection((HOST, port), timeout=3) as connection:
            connection.settimeout(3)
            print(f"connected to {HOST}:{port}")
            with connection.makefile("rb") as replies:
                send_and_check(connection, replies, "red")
                if pause_before_blue:
                    input("Pause after red: stop the server, then press Enter to send blue. ")
                send_and_check(connection, replies, "blue")
        print("closed first connection")
        with socket.create_connection((HOST, port), timeout=3) as connection:
            connection.settimeout(3)
            print(f"reconnected to {HOST}:{port}")
            with connection.makefile("rb") as replies:
                send_and_check(connection, replies, "green")
        print("closed second connection")
    except EOFError:
        print("No input: run --pause-before-blue in an interactive terminal.", file=sys.stderr)
        return 1
    except OSError as error:
        print(
            f"No reply ({error}). Server stopped or unreachable; an unanswered "
            "message's delivery is unknown. Start the server and run the client "
            "again to make a new connection.",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--pause-before-blue", action="store_true")
    args = parser.parse_args()
    sys.exit(main(args.port, args.pause_before_blue))

"""The Python rules shared by the HTTP and WebSocket handlers."""


class Scene:
    def __init__(self):
        self.x = 50
        self.revision = 0

    def snapshot(self):
        return {"type": "state", "x": self.x, "revision": self.revision}

    def apply(self, message):
        if not isinstance(message, dict) or set(message) != {"id", "action", "x"}:
            raise ValueError("Send exactly id, action and x.")
        if not isinstance(message["id"], str) or not 1 <= len(message["id"]) <= 48:
            raise ValueError("id must be a string of 1 to 48 characters.")
        if message["action"] != "set_x":
            raise ValueError("action must be set_x.")
        if type(message["x"]) is not int or not 0 <= message["x"] <= 100:
            raise ValueError("x must be a whole number from 0 to 100.")
        self.x = message["x"]
        self.revision += 1
        return {"type": "ack", "id": message["id"], "revision": self.revision}

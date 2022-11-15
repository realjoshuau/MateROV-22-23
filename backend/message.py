import json, msgpack

class JSONMessage:
    def __init__(self, message):
        if isinstance(message, bytes):
            data = msgpack.unpackb(message, raw=False)
        else:
            data = json.loads(message)
        self.command = data["cmd"]
        self.role = data["role"]
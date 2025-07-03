import json


class Task:
    def __init__(self, message):
        self.queue, item = message[0], json.loads(message[1])
        self.id = item["id"]
        self.args = item["args"]
        self.kwargs = item["kwargs"]

    @property
    def json(self):
        return json.dumps(
            {
                "id": self.id,
                "args": self.args,
                "kwargs": self.kwargs,
            }
        )

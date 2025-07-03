import json


class Task:
    def __init__(self, queue, message):
        self.queue = queue
        self.id = message["id"]
        self.args = message["args"]
        self.kwargs = message["kwargs"]

    @classmethod
    def load(cls, queue, json_str):
        message = json.loads(json_str)
        return cls(queue, message)

    @property
    def json(self):
        return json.dumps(
            {
                "id": self.id,
                "args": self.args,
                "kwargs": self.kwargs,
            }
        )

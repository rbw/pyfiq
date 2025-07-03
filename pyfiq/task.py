import json


class Task:
    def __init__(self, queue, message):
        self.queue = queue
        self.path = message["path"]
        self.args = message["args"]
        self.kwargs = message["kwargs"]

    @classmethod
    def load(cls, queue, json_str):
        message = json.loads(json_str)
        message["args"] = tuple(message["args"])
        return cls(queue, message)

    @property
    def json(self):
        return json.dumps(
            {
                "path": self.path,
                "args": self.args,
                "kwargs": self.kwargs,
            }
        )

    def __repr__(self):
        return f"<Task path={self.path} args={self.args} kwargs={self.kwargs}>"

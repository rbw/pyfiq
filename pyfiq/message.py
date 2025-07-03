import json
from dataclasses import dataclass, asdict


@dataclass
class Message:
    fqn: str
    args: tuple
    kwargs: dict

    @property
    def json_str(self):
        return json.dumps(asdict(self))

    @classmethod
    def load(cls, json_str):
        data = json.loads(json_str)
        return cls(**data)

    def __repr__(self):
        return (
            f"<Message path={self.fqn} "
            f"args={self.args} kwargs={self.kwargs}>"
        )

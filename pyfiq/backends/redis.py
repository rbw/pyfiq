import json
import redis

from ._base import QueueBackend


class RedisQueueBackend(QueueBackend):
    def __init__(self, redis_url="redis://localhost"):
        self.redis = redis.Redis.from_url(redis_url)

    def push(self, queue_name, task):
        self.redis.rpush(queue_name, json.dumps(task))

    def pop(self, queue_name, timeout=1):
        item = self.redis.blpop(queue_name, timeout=timeout)
        return json.loads(item[1]) if item else None

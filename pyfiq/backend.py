import logging

import redis

from .task import Task

log = logging.getLogger("pyfiq.backend")


class RedisQueueBackend:  # @TODO: Proper subclassing
    def __init__(self, redis_url="redis://localhost"):
        self.redis_url = redis_url
        self.redis = redis.Redis.from_url(redis_url)

    def push(self, queue_name, task):
        self.redis.rpush(queue_name, task.json_str)

    def pop(self, queue_name, timeout=1):
        if result := self.redis.blpop(queue_name, timeout=timeout):
            return Task.load(result[1])

        return None

    def __repr__(self):
        return f"RedisQueueBackend({self.redis_url})"


class AsyncRedisQueueBackend:
    pass

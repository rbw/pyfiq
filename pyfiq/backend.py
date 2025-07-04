import logging

import redis

from .task import Task

log = logging.getLogger("pyfiq.backend")


class RedisQueueBackend:  # @TODO: Proper subclassing
    def __init__(self, redis_url="redis://localhost"):
        self.redis_url = redis_url
        self.redis = redis.Redis.from_url(redis_url)

    def pop(self, queue, timeout=1):
        if result := self.redis.blpop(queue, timeout=timeout):
            return Task.load(result[1])

        return None

    def rpush(self, queue, task):
        self.redis.rpush(queue, task.json_str)

    def lpush(self, queue, task):
        self.redis.lpush(queue, task.json_str)

    def incr(self, key, ttl=3600):
        value = self.redis.incr(key)
        self.redis.expire(key, ttl)
        return value

    def delete(self, key):
        self.redis.delete(key)

    def __repr__(self):
        return f"RedisQueueBackend({self.redis_url})"


class AsyncRedisQueueBackend:
    pass

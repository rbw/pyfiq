import logging

import redis

from .task import Task

log = logging.getLogger("pyfiq.producer")


class RedisQueueBackend:  # @TODO: Subclass Redis instead of from_url
    def __init__(self, redis_url="redis://localhost"):
        self.redis_url = redis_url
        self.redis = redis.Redis.from_url(redis_url)

    def push(self, queue_name, task):
        log.debug(f"Enqueue {task}")
        self.redis.rpush(queue_name, task.json)

    def pop(self, queue_name, timeout=1):
        if message := self.redis.blpop(queue_name, timeout=timeout):
            task = Task.load(*message)
            log.debug(f"Dequeue {task}")
            return task

        return None

    def __repr__(self):
        return f"RedisQueueBackend({self.redis_url})"

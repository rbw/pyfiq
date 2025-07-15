import time
import json
import logging

import redis

from .task import Task

log = logging.getLogger("pyfiq.redis")


class RedisStreamsBackend:
    redis = None

    def __init__(self, url="redis://localhost", group="pyfiq", consumer=None):
        self.url = url
        self.redis = redis.Redis.from_url(url, decode_responses=True)
        self.group = group
        self.consumer = consumer or f"consumer-{time.time_ns()}"

    def schedule_retry(self, queue, task, delay):
        retry_time = time.time() + delay
        self.redis.zadd(f"{queue}:retries", {task.json_str: retry_time})

    def process_due_retries(self, queue):
        now = time.time()
        due_tasks = self.redis.zrangebyscore(f"{queue}:retries", 0, now)
        for task_json in due_tasks:
            task = Task.load(task_json)
            self.enqueue(queue, task)
            self.redis.zrem(f"{queue}:retries", task_json)

    def incr(self, key, ttl=10):
        value = self.redis.incr(key)
        self.redis.expire(key, ttl)
        return value

    def delete(self, key):
        self.redis.delete(key)

    def enqueue(self, queue, task):
        self.redis.xadd(queue, {
            "fqn": task.fqn,
            "args": json.dumps(task.args),
            "kwargs": json.dumps(task.kwargs),
        })
        log.debug(f"Enqueued {task}")

    def dequeue(self, queue, block=1000):
        try:
            # Read one entry from the stream for this consumer
            result = self.redis.xreadgroup(
                groupname=self.group,
                consumername=self.consumer,
                streams={queue: '>'},
                count=1,
                block=block  # Block for this many ms if no messages
            )

            if result:
                _, entries = result[0]
                entry_id, fields = entries[0]

                # Parse task
                task = Task(
                    fqn=fields["fqn"],
                    args=json.loads(fields["args"]),
                    kwargs=json.loads(fields["kwargs"]),
                )

                # Fetch delivery count (how many times this entry was delivered)
                pending_info = self.redis.xpending(queue, self.group)
                for entry in pending_info["consumers"]:
                    if entry["name"] == self.consumer:
                        delivery_count = entry["pending"]
                        break
                else:
                    delivery_count = 1  # Fallback: assume first delivery

                log.debug(f"Dequeued {task} (queue={queue}, entry_id={entry_id})")
                return entry_id, task, delivery_count

        except redis.exceptions.ResponseError as e:
            if "NOGROUP" in str(e):
                log.warning(f"Consumer group '{self.group}' not found. Creating it for queue '{queue}'.")
                self.redis.xgroup_create(queue, self.group, id="$", mkstream=True)
                return self.dequeue(queue, block)

            raise

        return None

    def ack(self, queue, entry_id):
        self.redis.xack(queue, self.group, entry_id)

    def __repr__(self):
        return f"{self.__class__.__name__} (url={self.url}, group={self.group})"

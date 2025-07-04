import functools
import logging

from .backend import RedisQueueBackend
from .workers import threaded_worker
from .manager import mgr
from .task import Task

log = logging.getLogger("pyfiq.producer")


def fifo(queue, on_success=None, on_error=None, max_retries=0):
    def decorator(func):
        b = mgr.bindings.add(func, queue, max_retries, on_success, on_error)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            t = Task(fqn=b.fqn, args=args, kwargs=kwargs)
            mgr.backend.rpush(queue, t)
            log.debug(f"Enqueued {t} (queue={queue})")

        return wrapper

    return decorator

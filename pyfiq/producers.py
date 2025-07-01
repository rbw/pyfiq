import functools
import logging

from . import registry
from .manager import mgr

log = logging.getLogger("pyfiq.producer")


def fifo(queue_name):
    def decorator(func):
        registry.register(func, queue_name)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            task = {
                "func": func.__name__,
                "args": args,
                "kwargs": kwargs,
            }
            task_id = mgr.backend.push(queue_name, task)
            log.debug(f"Enqueued {task} (task_id={task_id})")

        return wrapper

    return decorator

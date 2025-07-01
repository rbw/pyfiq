import functools
import logging
import uuid

from . import registry
from .manager import mgr

log = logging.getLogger("pyfiq.producer")


def fifo(queue):
    def decorator(func):
        registry.register(func, queue)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            task = {
                "id": str(uuid.uuid4()),
                "func": func.__name__,
                "args": args,
                "kwargs": kwargs,
            }
            log.debug(f"Enqueue {task['func']} (id={task['id']}])")
            mgr.backend.push(queue, task)

        return wrapper

    return decorator

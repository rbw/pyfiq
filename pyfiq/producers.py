import functools
import logging
import uuid

from .manager import mgr

log = logging.getLogger("pyfiq.producer")


def fifo(queue):
    def decorator(func):
        qri = mgr.registry.add_func(func, queue)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            task = {
                "id": qri.id,
                "args": args,
                "kwargs": kwargs,
            }
            log.debug(f"Enqueue {qri.id} (args={args}, kwargs={kwargs})")
            mgr.backend.push(qri.queue, task)

        return wrapper

    return decorator

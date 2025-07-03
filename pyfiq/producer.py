import functools

from .manager import mgr
from .task import Task


def fifo(queue):
    def decorator(func):
        qri = mgr.registry.add_func(func, queue)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            task = Task(queue, {
                "path": qri.path,
                "args": args,
                "kwargs": kwargs,
            })
            mgr.backend.push(task.queue, task)

        return wrapper

    return decorator

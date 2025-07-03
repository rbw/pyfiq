import functools

from .manager import mgr
from .message import Message

from .workers import threaded_worker
from .backend import RedisQueueBackend
from .utils import get_python_fqn


def fifo(queue):
    def decorator(func):
        b = mgr.bindings.add(func, queue)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            msg = Message(fqn=b.fqn, args=args, kwargs=kwargs)
            mgr.backend.push(queue, msg)

        return wrapper

    return decorator

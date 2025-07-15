import time
import functools
import logging

from .workers import ThreadedWorker
from .manager import QueueManager
from .task import Task

log = logging.getLogger("pyfiq.producer")


def fifo(queue, on_success=None, on_error=None, max_retries=3, retry_wait=10):
    def decorator(func):
        b = QueueManager.add_binding(func, queue, max_retries, retry_wait, on_success, on_error)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if QueueManager.backend is None:
                log.info("Backend is not initialized yet. Retrying indefinitely...")
                time.sleep(10)
                return wrapper(*args, **kwargs)

            t = Task(fqn=b.fqn, args=args, kwargs=kwargs)
            return QueueManager.backend.enqueue(queue, t)

        return wrapper

    return decorator

import logging

from .backend import RedisStreamsBackend
from .bindings import registry, FifoBinding

log = logging.getLogger("pyfiq.manager")


class QueueManager:
    backend: RedisStreamsBackend = None

    @classmethod
    def get_queues(cls):
        queues = []
        for binding in registry.values():
            queues.append(binding.queue)

        return set(queues)

    @classmethod
    def add_binding(cls, func, queue, max_retries, retry_wait, on_success=None, on_error=None) -> FifoBinding:
        return FifoBinding(func, queue, max_retries, retry_wait, on_success, on_error)

    @classmethod
    def get_binding(cls, fqn) -> FifoBinding:
        return registry.get(fqn)

    @classmethod
    def init(cls, backend: RedisStreamsBackend):
        cls.backend = backend
        log.debug(f"Backend configured: {cls.backend}")

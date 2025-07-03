import logging

from .backend import RedisQueueBackend
from .registry import QueueRegistry

log = logging.getLogger("pyfiq.manager")


class QueueManager:
    _backend: RedisQueueBackend = None

    def __init__(self):
        self.registry = QueueRegistry()

    @property
    def backend(self):
        return self._backend

    @backend.setter
    def backend(self, backend: RedisQueueBackend):
        self._backend = backend
        log.debug(f"Backend configured: {self._backend}")


mgr = QueueManager()

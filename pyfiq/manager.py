import logging

from .backend import RedisQueueBackend
from .registry import BindingsMap

log = logging.getLogger("pyfiq.manager")


class TaskManager:
    _backend: RedisQueueBackend = None

    def __init__(self):
        self.bindings = BindingsMap()

    @property
    def backend(self):
        return self._backend

    @backend.setter
    def backend(self, backend: RedisQueueBackend):
        self._backend = backend
        log.debug(f"Backend configured: {self._backend}")


mgr = TaskManager()

import logging

from .backends import QueueBackend
from .registry import QueueRegistry

log = logging.getLogger("pyfiq.manager")


class QueueManager:
    _backend: QueueBackend = None

    def __init__(self):
        self.registry = QueueRegistry()

    @property
    def backend(self):
        return self._backend

    @backend.setter
    def backend(self, backend: QueueBackend):
        self._backend = backend
        log.debug(f"Backend configured: {self._backend}")


mgr = QueueManager()

import logging

from .backends import QueueBackend

log = logging.getLogger("pyfiq.manager")


class QueueManager:
    _backend: QueueBackend = None

    @property
    def backend(self):
        return self._backend

    @backend.setter
    def backend(self, backend: QueueBackend):
        self._backend = backend
        log.info(f"Backend configured: {self._backend}")


mgr = QueueManager()

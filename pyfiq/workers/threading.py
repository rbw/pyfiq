import threading
import logging

from pyfiq.registry import get_registry
from pyfiq.manager import mgr
from pyfiq.backends import QueueBackend, RedisQueueBackend
from pyfiq.consumer import consume_queue

log = logging.getLogger("pyfiq.worker")


def threaded_worker(backend: QueueBackend = RedisQueueBackend()):
    log.debug("Starting threaded worker")
    mgr.backend = backend
    registry = get_registry()

    log.debug(f"Loaded tasks: {registry}")
    queues = {entry["queue"] for entry in registry.values()}

    for queue in queues:
        thread = threading.Thread(target=consume_queue, args=(queue,), daemon=True)
        thread.start()

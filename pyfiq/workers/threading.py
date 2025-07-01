import threading
import logging

from pyfiq.registry import get_registry
from pyfiq.manager import mgr
from pyfiq.backends import QueueBackend, RedisQueueBackend
from pyfiq.consumer import queue_consumer

log = logging.getLogger("pyfiq.worker")


def threaded_worker(backend: QueueBackend = RedisQueueBackend()):
    log.info("Starting worker")
    mgr.backend = backend
    registry = get_registry()

    log.info(f"Loaded tasks: {registry}")
    queues = {entry["queue"] for entry in registry.values()}

    for queue in queues:
        thread = threading.Thread(target=queue_consumer, args=(queue,), daemon=True)
        thread.start()

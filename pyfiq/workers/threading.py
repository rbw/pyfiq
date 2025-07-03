import threading
import logging

from pyfiq.manager import mgr
from pyfiq.backend import RedisQueueBackend
from pyfiq.consumer import consume_queue

log = logging.getLogger("pyfiq.worker")


def threaded_worker(backend: RedisQueueBackend = RedisQueueBackend()):
    log.debug("Starting threaded worker")
    mgr.backend = backend

    for queue in mgr.registry.queues:
        log.debug(f"Initializing worker thread for queue: {queue}")
        thread = threading.Thread(target=consume_queue, args=(queue,), daemon=True)
        thread.start()

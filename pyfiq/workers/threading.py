import threading
import signal
import logging

from pyfiq.backend import RedisStreamsBackend
from pyfiq.manager import QueueManager
from pyfiq.consumer import consume_queue

log = logging.getLogger("pyfiq.worker")


class ThreadedWorker(threading.Thread):
    def __init__(self, redis_url):
        super().__init__(name="pyfiq-worker", daemon=True)
        QueueManager.init(backend=RedisStreamsBackend(url=redis_url))
        self.stop_event = threading.Event()
        self.threads = []

    def run(self):
        log.info(f"Starting threaded worker")

        for queue in QueueManager.get_queues():
            log.debug(f"Initializing worker thread for queue: {queue}")
            thread = threading.Thread(target=self._worker_loop, args=(queue,), daemon=True)
            thread.start()
            self.threads.append(thread)

        if threading.current_thread() is threading.main_thread():
            signal.signal(signal.SIGINT, self._handle_shutdown)
            signal.signal(signal.SIGTERM, self._handle_shutdown)

    def _handle_shutdown(self, signum, frame):
        log.info(f"Received signal {signum}, stopping workers...")
        self.stop()

    def _worker_loop(self, queue):
        log.debug(f"Worker started for queue: {queue}")
        consume_queue(QueueManager.backend, queue, stop_event=self.stop_event)
        log.debug(f"Worker thread terminated (queue={queue})")

    def stop(self):
        log.debug("Stopping threaded worker...")
        self.stop_event.set()
        for thread in self.threads:
            thread.join()

        self.join()

        log.info("All worker threads stopped cleanly.")

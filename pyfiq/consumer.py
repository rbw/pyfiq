import logging
import time

from .registry import get_registry
from .manager import mgr

log = logging.getLogger("pyfiq.consumer")


def queue_consumer(queue):
    log.info(f"Starting consumer for queue: {queue}")

    while True:
        task = mgr.backend.pop(queue)
        log.info(f"Consuming message {task} of {queue}")
        if task:
            func_name = task["func"]
            entry = get_registry().get(func_name)
            if entry:
                retval = entry["func"](*task["args"], **task["kwargs"])
                log.info(f"Executed task {task["func"]}: {retval}")
        else:
            time.sleep(0.1)

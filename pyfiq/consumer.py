import logging
import time

from .manager import mgr

log = logging.getLogger("pyfiq.consumer")


def consume_queue(queue_name):
    log.debug(f"Starting consumer for queue: {queue_name}")

    while True:
        task = mgr.backend.pop(queue_name)
        if task:
            log.debug(f"Dequeue {task['id']} from {queue_name}")
            entry = mgr.registry.get_func(task["id"])

            if entry:
                retval = entry.func(*task["args"], **task["kwargs"])
                log.debug(f"Execute {entry.id}): {retval}")
        else:
            time.sleep(0.1)

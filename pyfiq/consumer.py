import logging
import time

from .registry import get_registry
from .manager import mgr

log = logging.getLogger("pyfiq.consumer")


def consume_queue(queue_name):
    log.debug(f"Starting consumer for queue: {queue_name}")

    while True:
        task = mgr.backend.pop(queue_name)
        if task:
            log.debug(f"Dequeue {task['func']} (id={task['id']})")
            entry = get_registry().get(task["func"])
            if entry:
                retval = entry["func"](*task["args"], **task["kwargs"])
                log.debug(f"Execute {task['func']} (id={task['id']}): {retval}")
        else:
            time.sleep(0.1)

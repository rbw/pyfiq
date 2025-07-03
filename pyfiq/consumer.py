import logging
import time

from .manager import mgr

log = logging.getLogger("pyfiq.consumer")


def consume_queue(queue_name):
    log.debug(f"Starting consumer for queue: {queue_name}")

    while True:
        task = mgr.backend.pop(queue_name)
        if task:
            log.debug(f"Dequeue {task}")
            qri = mgr.registry.get_func(task.id)

            if qri:
                retval = qri.func(*task.args, **task.kwargs)
                log.debug(f"Execute {qri.id}: {retval}")
        else:
            time.sleep(0.1)

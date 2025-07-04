import logging
import time

from .manager import mgr

log = logging.getLogger("pyfiq.consumer")


def consume_queue(queue):
    log.debug(f"Starting consumer for queue: {queue}")

    while True:
        if task := mgr.backend.pop(queue):
            log.debug(f"Dequeued {task} (queue={queue})")
            binding = mgr.bindings.get(task.fqn)

            if binding:
                try:
                    log.debug(f"Executing {task} (queue={queue})")
                    retval = binding.func(*task.args, **task.kwargs)
                    binding.on_success(retval, task, binding)
                except Exception as exc:
                    binding.on_error(exc, task, binding)
        else:
            time.sleep(0.1)

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
                retry_key = f"retry:{queue}:{task.fqn}"

                try:
                    log.debug(f"Executing {task} (queue={queue})")
                    retval = binding.func(*task.args, **task.kwargs)
                    binding.on_success(retval, task, binding)
                except Exception as exc:
                    retries = mgr.backend.incr(retry_key)

                    log.warning(
                        f"Task failed (retry {retries}/{binding.max_retries}): {task} (queue={queue})",
                        exc_info=exc
                    )

                    if retries < binding.max_retries:
                        log.info(f"Retrying {task}")
                        time.sleep(2)
                        mgr.backend.lpush(queue, task)
                        continue
                    else:
                        log.warning(f"Max retries reached for {task}")
                        mgr.backend.delete(retry_key)
                        binding.on_error(exc, task, binding)

        else:
            time.sleep(0.1)

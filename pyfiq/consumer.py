import logging
import time

from .manager import QueueManager

log = logging.getLogger("pyfiq.consumer")


def consume_queue(backend, queue, stop_event=None):
    log.debug(f"Starting consumer for queue: {queue}")

    while not (stop_event and stop_event.is_set()):
        result = backend.dequeue(queue)

        if not result:
            if stop_event and stop_event.wait(timeout=0.1):
                log.info(f"Stopping consumer for queue: {queue}")
                break
            time.sleep(0.2)
            continue

        entry_id, task, delivery_count = result
        binding = QueueManager.get_binding(task.fqn)

        if not binding:
            log.error(f"No binding found for {task.fqn}. Acknowledging to skip.")
            backend.ack(queue, entry_id)
            continue

        try:
            log.debug(f"Executing {task} (queue={queue})")
            retval = binding.func(*task.args, **task.kwargs)
            backend.ack(queue, entry_id)
            binding.on_success(retval, task, binding)

        except Exception as exc:
            retry_key = f"retry:{queue}:{task.fqn}"
            retries = backend.incr(retry_key)

            log.warning(
                f"Task failed (retry {retries}/{binding.max_retries}): {task}, entry_id={entry_id}",
                exc_info=exc
            )

            if binding.max_retries == -1:  # Blocking
                log.info(f"Retrying {task} after {binding.retry_wait}s (blocking mode)")
                if stop_event and stop_event.wait(timeout=binding.retry_wait):
                    break  # No ack
            else:
                if retries < binding.max_retries:
                    log.info(f"Retrying {task} after {binding.retry_wait}s")
                    if stop_event and stop_event.wait(timeout=binding.retry_wait):
                        break

                    backend.ack(queue, entry_id)
                    backend.enqueue(queue, task)
                else:
                    log.error(f"Max retries reached for {task}, entry_id={entry_id}, invoking on_error.")
                    backend.delete(retry_key)
                    backend.ack(queue, entry_id)
                    binding.on_error(exc, task, binding)

    log.debug(f"Consumer loop exited for queue: {queue}")

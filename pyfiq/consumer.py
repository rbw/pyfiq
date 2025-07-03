import logging
import time

from .manager import mgr

log = logging.getLogger("pyfiq.consumer")


def consume_queue(queue_name):
    log.debug(f"Starting consumer for queue: {queue_name}")

    while True:
        if msg := mgr.backend.pop(queue_name):
            binding = mgr.bindings.get(msg.fqn)

            if binding:
                retval = binding.func(*msg.args, **msg.kwargs)
                log.debug(f"Execute {msg.fqn} (result={retval})")
        else:
            time.sleep(0.1)

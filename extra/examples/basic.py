import time
import logging
import requests

from pyfiq import fifo, threaded_worker, RedisQueueBackend

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logging.getLogger("urllib3").setLevel(logging.INFO)
log = logging.getLogger("pyfiq-example")


def handle_success(retval, task, _):
    log.info(f"Task succeeded ({task}): {retval}")


def handle_error(exc, task, _):
    log.exception(f"Task failed ({task})", exc_info=exc)


@fifo(queue="google-https", on_success=handle_success, on_error=handle_error)
def fetch_google_successfully():
    return requests.get("https://google.com")


@fifo(queue="google-https", on_success=handle_success, on_error=handle_error)
def fetch_google_fail():
    raise Exception("Simulated failure!")


@fifo(queue="microsoft-https", on_success=handle_success, on_error=handle_error)
def fetch_microsoft():
    return requests.get("https://microsoft.com")


def run_worker_loop():
    threaded_worker(
        backend=RedisQueueBackend("redis://localhost")
    )

    while True:
        fetch_google_successfully()
        fetch_google_fail()
        fetch_microsoft()

        time.sleep(10)


run_worker_loop()

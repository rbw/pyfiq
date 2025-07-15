import time
import logging

import requests

from pyfiq import fifo, ThreadedWorker


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


@fifo(queue="google-http", on_success=handle_success, on_error=handle_error)
def fetch_google_successfully():
    return requests.get("https://google.com")


@fifo(queue="google-http", on_error=handle_error, max_retries=2, retry_wait=2)
def fetch_google_fail(asdf):
    raise Exception("Simulated failure!")


@fifo(queue="microsoft-http", on_success=handle_success)
def fetch_microsoft():
    return requests.get("https://microsoft.com")


def run_example():
    worker = ThreadedWorker(redis_url="redis://localhost")
    worker.start()

    try:
        while True:
            fetch_google_fail("duh!")
            fetch_google_successfully()
            fetch_microsoft()
            time.sleep(10)

    except KeyboardInterrupt:
        log.info("Shutting down...")
        worker.stop()


run_example()

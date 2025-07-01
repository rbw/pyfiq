# pyfiq

`pyfiq` is a minimal task queue for Python. It runs background functions in FIFO order--without Celery, brokers, or boilerplate.  
Perfect for I/O-bound tasks like HTTP requests, syncing with external systems, or sending webhooks.

Currently, only Redis is supported, but `pyfiq` is designed with modularity in mind.

## Quick start

### Bootstrap the worker

This should run once on application startup, typically in your main thread or service entrypoint:

```python
from pyfiq import threaded_worker, RedisQueueBackend

worker = threaded_worker(
    backend=RedisQueueBackend("redis://localhost")
)
```

This starts a background worker thread that consumes tasks from Redis.

### Decorate your functions

Decorate the functions you want to be processed asynchronously in a FIFO queue:

```python
import requests
from pyfiq import fifo

@fifo(queue="http-requests")
def fetch_google():
    requests.get("https://google.com")

@fifo(queue="http-requests")
def fetch_microsoft():
    requests.get("https://microsoft.com")
```

You can now call these functions normally from multiple application instances--without worrying about execution order.

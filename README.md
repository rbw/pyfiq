# pyfiq

`pyfiq` is a minimal Redis-backed FIFO task queue for Python. It lets you decorate functions with `@fifo(...)`, and they'll be queued for execution in 
strict order processed by threaded background workers utilizing Redis BLPOP.

It's for I/O-bound tasks like HTTP requests, webhook dispatching, or syncing with third-party APIs--especially when execution order matters, but you don't want the 
complexity of Celery or external workers.

#### Unlike:
- **Celery**, which requires brokers, workers, and doesn't preserve ordering by default 
- **AWS Lambda**, which don't guarantee FIFO unless using with SQS FIFO + extra setup

#### pyfiq is:
- Embedded: runs inside your application process (no separate worker service)
- Application-scaled \& distributed: queues are processed wherever your app runs
- Order-preserving: per-queue FIFO with one active consumer per queue
- Zero-config: no external orchestrators, brokers, or setup required

It's designed to be very simple, and only provide ordered execution of tasks. The code is rudimentary right now, and there's a lot of room for improvement.

### Important #1

This library is intended only for I/O-bound tasks.
Using it with CPU-bound code is not recommended, as it runs in a background thread and would block execution.

### Important #2

This project is in its early stages of development.


## Quick start

### Installing

```
$ pip install pyfiq
```

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

@fifo(queue="http-requests1")
def fetch_google():
    requests.get("https://google.com")

@fifo(queue="http-requests1")
def fetch_microsoft():
    requests.get("https://microsoft.com")

@fifo(queue="http-requests2")
def fetch_github():
    requests.get("https://github.com")
```

## Todo

### Redis / pyfiq Core Logic
- Graceful shutdown: Ensure background thread stops cleanly (e.g. via signal handlers or context managers)
- Error handling & logging: Catch and log exceptions inside task execution without crashing the worker
- Retry support: Optional retries on failure, ideally with configurable delay or retry queue
- Task deduplication (optional): Prevent duplicate enqueues via Redis keys or hashes
- Task expiration / TTL: Option to discard stale tasks (use Redis TTL or ZSET-based queues if needed)
- Custom serialization support: Allow override of default JSON serializer (e.g., for datetime, Decimal)
- Connection pool support: Reuse Redis connections across queues and workers
- Support for async decorators (optional): Allow @fifo to be used on async def functions (using asyncio.to_thread etc.)

### Testing & Reliability

- Unit tests: Cover queue backend, task dispatch, decorator behavior
- Simulate concurrent enqueuers across instances

### CI/CD Pipeline

- GitHub Actions
- Run tests on push & PR
- PyPI publishing on version push tag
- Automatic PyPI publish (publish.yml GA):

class QueueBackend:
    def push(self, queue_name, task):
        raise NotImplementedError

    def pop(self, queue_name, timeout=1):
        raise NotImplementedError

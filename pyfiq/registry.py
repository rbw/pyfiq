_registry = {}


def register(func, queue):
    _registry[func.__name__] = dict(
        func=func,
        queue=queue,
    )


def get_registry():
    return _registry

_qri_registry = {}


class QueueRegistryItemMeta(type):
    """Implements func_id multiton (on func_id)"""

    def __call__(cls, func, queue):
        func_id = f"{func.__module__}.{func.__qualname__}"
        if func in _qri_registry:
            return _qri_registry[func_id]

        instance = super().__call__(func, queue)
        instance.path = func_id
        _qri_registry[func_id] = instance
        return instance


class QueueRegistryItem(metaclass=QueueRegistryItemMeta):
    """Creates and registers a registry item if it isn't registered already"""

    id = None

    def __init__(self, func, queue):
        self.func = func
        self.queue = queue


class QueueRegistry:
    """Registry facade around qri registry"""

    @property
    def funcs(self):
        for fn, qri in _qri_registry.items():
            yield {qri.path: (qri.func, qri.queue)}

    @property
    def queues(self):
        for qri in _qri_registry.values():
            yield qri.queue

    @classmethod
    def add_func(cls, func, queue):
        return QueueRegistryItem(func, queue)

    @classmethod
    def get_func(cls, func_id):
        return _qri_registry[func_id]

    def __setitem__(self, func, queue):
        self.add_func(func, queue)

    def __getitem__(self, func):
        return self.get_func(func)

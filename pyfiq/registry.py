import json
import logging

from .utils import get_python_fqn

log = logging.getLogger("pyfiq.registry")


class FifoBindingMeta(type):
    """Implements binding multiton (on fqn / fully-qualified name)"""

    def __call__(cls, func, queue):
        fqn = get_python_fqn(func)
        if binding := BindingsMap.get(fqn):
            # Binding for `func` already exists.
            # This guarantees that any given function is bound only once.
            # Support for multiple queues and workers for the same function can be
            # added here in the future by broadening this constraint.
            log.warning(f"Function {func} already bound to {queue}")

            # For now, we'll just return the existing binding
            return binding

        # Create new binding
        binding = super().__call__(func, queue)
        BindingsMap.registry[fqn] = binding
        log.debug(f"Added binding: {binding}")

        return binding


class FifoBinding(metaclass=FifoBindingMeta):
    """Creates and registers a FIFO binding"""

    def __init__(self, func, queue):
        self.fqn = get_python_fqn(func)
        self.func = func
        self.queue = queue

    def __repr__(self):
        return f"FifoBinding({self.fqn}, {self.queue})"


class BindingsMap:
    """Facade around bindings"""

    registry = {}

    @property
    def queues(self):
        for binding in self.registry.values():
            yield binding.queue

    @classmethod
    def add(cls, func, queue):
        binding = FifoBinding(func, queue)
        log.debug(f"Created binding for {binding.fqn} (queue={binding.queue})")
        return binding

    @classmethod
    def get(cls, fqn):
        return cls.registry.get(fqn)

    def __dict__(self):
        return self.registry

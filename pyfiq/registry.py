import logging

from .utils import get_python_fqn

log = logging.getLogger("pyfiq.registry")


def noop(*args, **kwargs):
    pass


class FifoBindingMeta(type):
    """Implements binding multiton (on fqn / fully-qualified name)"""

    def __call__(cls, func, queue, on_success, on_error):
        fqn = get_python_fqn(func)
        if binding := TaskRegistry.get(fqn):
            # Binding for `func` already exists.
            # This guarantees that any given function is bound only once.
            # Support for multiple queues and workers for the same function can be
            # added here in the future by broadening this constraint.
            log.warning(f"Function {func} already bound to {queue}")

            # For now, we'll just return the existing binding
            return binding

        # Create new binding
        binding = super().__call__(func, queue, on_success, on_error)
        TaskRegistry.bindings[fqn] = binding
        log.debug(f"Added binding: {binding}")

        return binding


class FifoBinding(metaclass=FifoBindingMeta):
    """Creates and registers a new FIFO binding and binds response handlers"""

    def __init__(self, func, queue, on_success, on_error):
        self.fqn = get_python_fqn(func)
        self.func = func
        self.queue = queue
        self.on_success = on_success if callable(on_success) else noop
        self.on_error = on_error if callable(on_error) else noop

    def __repr__(self):
        return f"FifoBinding({self.fqn}<->{self.queue} :: on_success={self.on_success}, on_error={self.on_error})"


class TaskRegistry:
    """Facade around bindings"""

    bindings = {}

    @property
    def queues(self):
        for binding in self.bindings.values():
            yield binding.queue

    @classmethod
    def add(cls, func, queue, on_success=None, on_error=None):
        return FifoBinding(func, queue, on_success, on_error)

    @classmethod
    def get(cls, fqn):
        return cls.bindings.get(fqn)

    def __dict__(self):
        return self.bindings

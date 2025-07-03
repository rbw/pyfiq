def get_python_fqn(fn):
    return f"{fn.__module__}.{fn.__qualname__}"

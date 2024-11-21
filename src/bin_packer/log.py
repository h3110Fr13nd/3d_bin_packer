# log.py

is_log_enabled = False

def enable_log(enable: bool = True) -> None:
    """Enable or disable logging functionality."""
    global is_log_enabled
    is_log_enabled = enable

def create_logger(namespace: str = '3d-bin-packing'):
    """Create a logger function with a specific namespace."""
    def logger(*args):
        return log(namespace, *args)
    return logger

def log(namespace: str, *args) -> None:
    """Log messages with namespace if logging is enabled."""
    if is_log_enabled:
        print(f"DEBUG: {namespace}", *args)
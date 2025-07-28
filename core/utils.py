import time
from functools import wraps
from core.logger import logger  

def retry(retries=3, delay=2):
    """Retry decorator that retries a function if it raises an exception."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exc = e
                    logger.warning(f"Attempt {attempt} failed: {e}")
                    time.sleep(delay)
            logger.error(f"All {retries} attempts failed.")
            if last_exc is not None:
                raise last_exc
            else:
                raise Exception("All attempts failed, but no exception was captured.")
        return wrapper
    return decorator
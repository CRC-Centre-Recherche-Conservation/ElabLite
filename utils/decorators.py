import psutil
import functools


def limit_ram_usage(threshold_percent: int):
    """Wrapper decorator to stop the process in case of memory overconsumption
    :threshold_percent: int, percent memory limit usage
    """
    def wrapper(func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            ram_percent = psutil.virtual_memory().percent

            if ram_percent > threshold_percent:
                raise MemoryError(f"RAM usage ({ram_percent}%) exceeds threshold ({threshold_percent}%)")
            else:
                return func(*args, **kwargs)

        return wrapped

    return wrapper

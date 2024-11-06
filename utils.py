import random
import string
import time
from functools import wraps

from loguru import logger


def measure_time(use=1):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if use != 1:
                return await func(*args, **kwargs)
            start_time = time.time()
            result = await func(*args, **kwargs)
            end_time = time.time()
            elapsed_time = end_time - start_time
            logger.info(f"Время выполнения {func.__name__}: {elapsed_time:.4f} секунд")
            return result

        return wrapper

    return decorator


def generate_x_o3_fp_ozon():
    return "1." + ''.join(random.choices(string.hexdigits[:16].lower(), k=16))

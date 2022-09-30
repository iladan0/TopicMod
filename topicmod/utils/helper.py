from functools import wraps
import time


def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(">>> Elapsed time for: {} is: {}".format(func.__name__, (end - start)))
        # "s. Args: {} and kwargs: {}".format(func.__name__, (end - start), args, kwargs))
        return result

    return wrapper
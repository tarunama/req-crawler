import time
from functools import wraps


def time_it(func):
    def wrap(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        return time.time() - start_time
    return wrap
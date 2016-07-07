# -*- coding: utf-8 -*-
import time


def log_process_time(func):
    def wrap(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        print('method_name {0} ## {1}'.format(func.__name__,
                                              time.time() - start_time))
        return result
    return wrap

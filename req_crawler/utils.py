# -*- coding: utf-8 -*-
import time

from logger import process_logger


def log_process_time(func):
    def wrap(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        msg = 'method_name {0} ## {1}'.format(func.__name__,
                                              time.time() - start_time)
        process_logger.info(msg)
        return result
    return wrap

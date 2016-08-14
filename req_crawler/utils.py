# -*- coding: utf-8 -*-
import time

from logger import logger


def log_process_time(func):
    def wrap(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        logger.info('method_name {0} ## {1}'.format(func.__name__,
                                                    time.time() - start_time))
        return result
    return wrap

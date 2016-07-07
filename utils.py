# -*- coding: utf-8 -*-
import time


def time_it(func):
    def wrap(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        return time.time() - start_time
    return wrap
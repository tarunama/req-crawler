# -*- coding: utf-8 -*-
import logging
from subprocess import call


class Logger(object):

    def __init__(self, log_type):
        self.log_type  = log_type
        self.name      = ('req_crawler.log' if log_type == 'main' else
                          'task.log')
        self.file_name = '../log/{}'.format(self.name)

    def create(self):
        name   = 'req_crawler:{}'.format(self.log_type)
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        handler = self.create_file_handler()
        formatter = \
            logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def create_file_handler(self):
        try:
            handler = logging.FileHandler(filename=self.file_name)
        except FileNotFoundError:
            touch_command = 'touch {}'.format(self.file_name)
            call(touch_command)
            handler = logging.FileHandler(filename=self.file_name)
        return handler


logger = Logger('main')
process_logger = Logger('task')

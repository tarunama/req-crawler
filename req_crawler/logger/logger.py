# -*- coding: utf-8 -*-
import logging
from subprocess import call

from req_crawler.settings.base import APP_ROOT_PATH


class Logger(object):

    def __init__(self, log_type):
        self.__log_type  = log_type
        self.__name      = ('req_crawler.log' if log_type == 'main' else
                            'task.log')
        self.__file_name = '{app_root_path}/log/{file_name}'.format(
            app_root_path=APP_ROOT_PATH,
            file_name=self.__name
        )

    def create(self):
        name   = 'req_crawler:{}'.format(self.__log_type)
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
            handler = logging.FileHandler(filename=self.__file_name)
        except FileNotFoundError:
            touch_command = 'touch {}'.format(self.__file_name)
            call(touch_command)
            handler = logging.FileHandler(filename=self.__file_name)
        return handler


logger = Logger('main').create()
process_logger = Logger('task').create()

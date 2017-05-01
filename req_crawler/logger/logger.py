# -*- coding: utf-8 -*-
import logging
from subprocess import call


def create_file_handler(log_type):
    log_name = ('req_crawler.log' if log_type == 'main' else
                'task.log')
    file_name = '../log/{}'.format(log_name)

    try:
        handler = logging.FileHandler(filename=file_name)
    except FileNotFoundError:
        touch_command = 'touch {}'.format(file_name)
        call(touch_command)
        handler = logging.FileHandler(filename=file_name)

    return handler


def create_logger():
    logger = logging.getLogger('req_crawler')
    logger.setLevel(logging.INFO)
    handler = create_file_handler('main')
    formatter = \
        logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

logger = create_logger()


def create_process_logger():
    task_logger = logging.getLogger('req_crawler:process')
    task_logger.setLevel(logging.INFO)
    handler = create_file_handler('task')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
    handler.setFormatter(formatter)
    task_logger.addHandler(handler)
    return task_logger


process_logger = create_process_logger()

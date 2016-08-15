# -*- coding: utf-8 -*-
import logging


def create_logger():
    logger = logging.getLogger('req_crawler')
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(filename='../log/req_crawler.log')
    formatter = \
        logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

logger = create_logger()


def create_process_logger():
    task_logger = logging.getLogger('req_crawler:process')
    task_logger.setLevel(logging.INFO)
    handler = logging.FileHandler(filename='../log/task.log')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')
    handler.setFormatter(formatter)
    task_logger.addHandler(handler)
    return task_logger


process_logger = create_process_logger()

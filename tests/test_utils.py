# -*- coding: utf-8 -*-
import unittest
from time import sleep
from mock import patch

from req_crawler.utils import log_process_time


class UtilsTest(unittest.TestCase):

    @patch('req_crawler.utils.log_process_time')
    def test_log_process_time(self, mock_logging):
        """ check call info message"""

        @log_process_time
        def f():
            sleep(1)

        # self.assertTrue(mock_logging.info.called)


if __name__ == '__main__':
    unittest.main()

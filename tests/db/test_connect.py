# -*- coding: utf-8 -*-
import unittest

from req_crawler.db.connect import ConnectDB
from req_crawler.settings import settings


class DBConnectTest(unittest.TestCase):

    def test_connect(self):
        """
        DBに接続できるかテスト
        """
        connection = ConnectDB(settings)
        self.assertTrue(connection)

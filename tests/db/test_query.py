# -*- coding: utf-8 -*-

import unittest

from req_crawler.db.query import Query
from req_crawler.db.connect import ConnectDB
from req_crawler.settings import settings


class QueryTest(unittest.TestCase):

    def setUp(self):
        # Establish DB connection
        self.connect_db = ConnectDB(settings)
        self.query = Query(self.connect_db, settings)

        # Start transaction
        self.query.cursor.execute('BEGIN')

        # Drop tables for test
        is_exist_table = self.query.cursor.execute('SHOW TABLES')

        if is_exist_table:
            tables = settings.DB_TABLES
            for table_name in tables:
                sql = 'DROP TABLE {}'.format(table_name)
                self.query.cursor.execute(sql)

    def test_create_init_table(self):
        self.query.create_init_table()
        table_count = self.query.cursor.execute('SHOW TABLES')

        self.assertTrue(0 < table_count)

    def tearDown(self):
        # Rollback all executions
        self.query.cursor.execute('ROLLBACK')

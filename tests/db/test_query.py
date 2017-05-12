# -*- coding: utf-8 -*-

import unittest

from req_crawler.db.query import Query
from req_crawler.db.connect import ConnectDB
from req_crawler.settings import settings


class QueryTest(unittest.TestCase):

    def setUp(self):
        self.company_list = {'foo', 'bar', 'baz'}
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
        table_count_first_time = self.query.cursor.execute('SHOW TABLES')

        self.assertTrue(0 < table_count_first_time)

        # Can not create table when created table already
        self.query.create_init_table()
        table_count_second_time = self.query.cursor.execute('SHOW TABLES')

        self.assertTrue(table_count_first_time == table_count_second_time)

    def test_create_cols(self):
        # Create table for test
        self.query.create_init_table()

        for table_name in settings.DB_TABLES:
            sql = 'DESCRIBE {}'.format(table_name)
            self.query.cursor.execute(sql)

            # String for create INSERT query
            table_cols = [row_info['Field'] for row_info
                          in self.query.cursor.fetchall()
                          if row_info['Field'] != 'id']

            table_cols_str = ','.join(table_cols)
            self.assertTrue(self.query.create_cols(table_name) == table_cols_str)

    def test_insert(self):
        # Create table for test
        self.query.create_init_table()
        self.query.insert(self.company_list, commit=True)
        table     = 'requirement'
        row_count = self.query.cursor.execute('SELECT *'
                                              'FROM {}'.format(table))
        self.assertTrue(row_count == 3)

    def tearDown(self):
        # Rollback all executions
        self.query.cursor.execute('ROLLBACK')

# -*- coding: utf-8 -*-
import datetime

from req_crawler.logger import logger
from req_crawler.utils import log_process_time


class Query(object):
    """
    Query for DB actions
    """
    def __init__(self, connect_db, settings):
        self.conn = connect_db.connection
        self.cursor = connect_db.connection.cursor()
        self._tables = settings.DB_TABLES
        self._db_rows = settings.DB_ROWS
        self._db_settings = settings.DB_SETTINGS
        self.cursor.execute('use {0}'.format(self._db_settings.get('db')))
        self.value_str = "('python', '{0}', 'Wantedly', '{1}', '{1}')"

    def create_init_table(self) -> None:
        """
        If there are not tables, create table
        """
        is_exist_table = self.cursor.execute('show tables')

        if is_exist_table:
            return None

        for table in self._tables:
            try:
                cols = self._db_rows.get(table)
                cols_str = ','.join(cols)
                sql = "CREATE TABLE {0}({1});".format(table, cols_str)
                self.cursor.execute(sql)
            except Exception as e:
                logger.exception(e)
                self.close()

    def create_cols(self, table_name: str) -> str:
        """
        Create string for INSERT query
        """
        table_rows = self._db_rows[table_name]
        return ','.join([s.split(' ')[0] for s in table_rows if s[:2] != 'id'])

    @log_process_time
    def select(self) -> set:
        """
        Get company names from tables for checking diff
        """
        for table in self._tables:
            sql = "SELECT * FROM {0};".format(table)
            self.cursor.execute(sql)

        return set(c['company_name'] for c in self.cursor.fetchall())

    @log_process_time
    def insert(self, company_list: set, commit=False) -> None:
        """
        Execute INSERT query
        """
        dt = datetime.datetime.now()
        values = ''
        for i, company in enumerate(company_list):
            value_str = self.value_str.format(company, str(dt).split('.')[0])
            if i == len(company_list) - 1:
                values += value_str + ';'
            else:
                values += value_str + ','

        for table in self._tables:
            cols = self.create_cols(table)
            sql = "INSERT INTO {0} ({1}) VALUES {2}".format(table, cols, values)
            logger.info(sql)
            logger.info(self.cursor.execute(sql))

        if commit:
            self.conn.commit()

    def close(self) -> None:
        """
        Close connection, when it happens exception
        """
        try:
            self.cursor.close()
            self.conn.close()
        except Exception as e:
            logger.info(e)
            exit()

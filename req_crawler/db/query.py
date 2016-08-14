# -*- coding: utf-8 -*-
import datetime
import logging

from req_crawler.utils import log_process_time


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Query(object):
    """
    Queryを定義しているクラス
    """
    def __init__(self, connect_db, settings):
        self.conn = connect_db.connection
        self.cursor = connect_db.connection.cursor()
        self._tables = settings.DB_TABLES
        self._db_rows = settings.DB_ROWS
        self._db_settings = settings.DB_SETTINGS
        self.cursor.execute('use {0}'.format(self._db_settings.get('db')))
        self.value_str = "('python', '{0}', 'Wantedly', '{1}', '{1}')"

    def create_init_table(self):
        """
        テーブルがない場合、作成する
        """
        table_count = self.cursor.execute('show tables')

        if table_count == 0:
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
        テーブルのカラムを取得する
        """
        table_rows = self._db_rows[table_name]
        return ','.join([s.split(' ')[0] for s in table_rows if s[:2] != 'id'])

    @log_process_time
    def select(self) -> set:
        """
        テーブルから会社名を取得する
        """
        for table in self._tables:
            sql = "SELECT * FROM {0};".format(table)
            self.cursor.execute(sql)

        return set(c['company_name'] for c in self.cursor.fetchall())

    @log_process_time
    def insert(self, company_list: set, commit=False) -> None:
        """
        データをテーブルに挿入する
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

    def close(self):
        """
        例外処理が発生した場合、接続を閉じる
        """
        try:
            self.cursor.close()
            self.conn.close()
        except Exception as e:
            logger.info(e)
            exit()

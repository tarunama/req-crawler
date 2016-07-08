# -*- coding: utf-8 -*-
import datetime

import pymysql

from req_crawler.utils import log_process_time

from settings.develop import DB_SETTINGS, DB_TABLES, DB_ROWS


class ConnectDB:

    def __init__(self, settings=DB_SETTINGS):
        self._connection = pymysql.connect(**settings)
        self._tables = DB_TABLES
        self.cursor = self._connection.cursor()
        self.cursor.execute('use {0}'.format(DB_SETTINGS.get('db')))
        self.value_str = "('python', '{0}', 'Wantedly', '{1}', '{1}')"

    def create_init_table(self):
        table_count = self.cursor.execute('show tables')

        if table_count == 0:
            return None

        for table in self._tables:
            try:
                cols = DB_ROWS.get(table)
                cols_str = ','.join(cols)
                sql = "CREATE TABLE {0}({1});".format(table, cols_str)
                self.cursor.execute(sql)
            except Exception as e:
                print(e)
                self.close()

    def create_cols(self):
        table = DB_TABLES[0]
        table_rows = DB_ROWS[table]
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
    def insert(self, company_list:set, commit=True) -> None:
        dt = datetime.datetime.now()
        # 言語とメディアを変数にする
        values = ''
        for i, company in enumerate(company_list):
            _value_str = self.value_str.format(company, str(dt).split('.')[0])
            if i == len(company_list) - 1:
                values += _value_str + ';'
            else:
                values += _value_str + ','

        cols = self.create_cols()

        for table in self._tables:
            sql = "INSERT INTO {0} ({1}) VALUES {2}".format(table, cols, values)
            self.cursor.execute(sql)

        if commit:
            self._connection.commit()

    def close(self):
        try:
            self.cursor.close()
            self._connection.close()
        except:
            raise Exception


if __name__ == '__main__':
    c = ConnectDB()
    c.select()
    c.close()

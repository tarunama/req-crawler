# -*- coding: utf-8 -*-
import pymysql

from settings.develop import DB_SETTINGS, DB_TABLES


class ConnectDB:

    def __init__(self, settings=DB_SETTINGS):
        self._connection = pymysql.connect(**settings)
        self._tables = DB_TABLES

if __name__ == '__main__':
    c = ConnectDB()
    print(c._connection)

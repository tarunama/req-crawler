# -*- coding: utf-8 -*-
import pymysql


class ConnectDB:
    """
    DBとの接続を確立する
    """
    def __init__(self, settings):
        self.connection = pymysql.connect(**getattr(settings, 'DB_SETTINGS'))
        self.tables = getattr(settings, 'DB_TABLES')

# -*- coding: utf-8 -*-
import pymysql


class ConnectDB:
    """
    Establish Connection
    """
    def __init__(self, settings):
        self.connection = pymysql.connect(**settings.DB_SETTINGS)
        self.tables = settings.DB_TABLES

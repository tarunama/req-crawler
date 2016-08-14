# -*- coding: utf-8 -*-
import pymysql


CRAWLED_URLS = [
    'https://www.wantedly.com/search?q=python'
]

DB_SETTINGS = {
    'host': 'localhost',
    'user': 'req',
    'password': 'req',
    'db': 'req',
    'charset': 'utf8',
    'cursorclass': pymysql.cursors.DictCursor
}

DB_TABLES = [
    'requirement'
]

DB_ROWS = {
    'requirement': [
        'id int',
        'language varchar(64)',
        'company_name varchar(255)',
        'media varchar(255)',
        'create_at datetime',
        'update_at datetime',
    ]
}

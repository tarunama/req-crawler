# -*- coding: utf-8 -*-

from os.path import abspath, dirname

import pymysql


APP_ROOT_PATH = dirname( dirname( dirname( abspath(__file__) ) ) )

CRAWLED_URLS = [
    'https://www.wantedly.com/search?q=python'
]

CRAWLED_SITE_INFO = {
    'www.wantedly.com': {
        'pagination_url':
            'https://www.wantedly.com/search?page={0}&q=python&t=projects',
        'crawl_tag': 'p',
        'crawl_class': 'company-name'
    }
}

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

# -*- coding: utf-8 -*-
from db import ConnectDB, Query
from logger import logger
from settings import settings
from crawler import RequirementCrawler


def main():
    urls = getattr(settings, 'CRAWLED_URLS', [])
    if not urls:
        logger.error('CRAWLED_URLSを設定してください')
        exit()

    connect_db = ConnectDB(settings)
    query = Query(connect_db, settings)

    for url in urls:
        req_crawler = RequirementCrawler('GET', url)
        company_list = req_crawler.get_company_list()
        exist_company_list = query.select()
        if company_list - exist_company_list:
            query.insert(company_list)

if __name__ == '__main__':
    logger.info('process start')
    main()
    logger.info('process finished')

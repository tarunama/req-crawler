# -*- coding: utf-8 -*-
import certifi
import urllib3
from urllib.parse import urlparse

from bs4 import BeautifulSoup

from req_crawler.settings import settings
from req_crawler.utils import log_process_time


class RequirementCrawler(object):

    #HACK: reduce attribute
    def __init__(self, method='GET', url=None):
        self.method = method
        self.url = url
        self.http = urllib3.PoolManager(ca_certs=certifi.where())
        self.request = self.http.request(self.method, self.url)
        self.soup = BeautifulSoup(self.request.data, 'lxml')
        self.page_num = 1
        self.crawl_tag = ''
        self.crawl_class = ''
        self.pagination_url = ''
        self.set_init_attr()

    def set_init_attr(self) -> None:
        parse_result = urlparse(self.url)
        domain = parse_result.netloc
        site_info = settings.CRAWLED_SITE_INFO[domain]
        self.crawl_tag = site_info['crawl_tag']
        self.crawl_class = site_info['crawl_class']
        self.pagination_url = site_info['pagination_url']

    def get_pagination_url(self) -> str:
        self.page_num += 1
        return self.pagination_url.format(self.page_num)

    def get_next_soup(self, pagination_url):
        request = self.http.request(self.method, pagination_url)
        bs = BeautifulSoup(request.data, 'lxml')
        return bs.find_all(self.crawl_tag, class_=self.crawl_class)

    @log_process_time
    def get_company_list(self) -> set:
        company_list = set()
        soup = self.soup.find_all(self.crawl_tag, class_=self.crawl_class)

        while soup:
            for company_name in soup:
                _company_name = company_name.string.strip()
                if len(_company_name) != 0:
                    company_list.add(_company_name)

            pagination_url = self.get_pagination_url()
            soup           = self.get_next_soup(pagination_url)

        return company_list

# -*- coding: utf-8 -*-
import certifi
import urllib3

from bs4 import BeautifulSoup

from utils import log_process_time


class RequirementCrawler(object):

    def __init__(self, method=None, url=None):
        self.method = method or 'GET'
        self.url = url
        self.http = urllib3.PoolManager(ca_certs=certifi.where())
        self.request = self.http.request(self.method, self.url)
        self.soup = BeautifulSoup(self.request.data, 'lxml')
        self.page_num = 1

    def get_pagination_url(self):
        self.page_num += 1
        return ("https://www.wantedly.com/search?page={0}&q=python&t=projects"
                .format(self.page_num))

    def get_next_soup(self, pagination_url, http_method=None):
        http_method = http_method if http_method else 'GET'
        request = self.http.request(http_method, pagination_url)
        bs = BeautifulSoup(request.data, 'lxml')
        return bs.find_all('p', class_='company-name')

    @log_process_time
    def get_company_list(self) -> set:
        company_list = set()
        soup = self.soup.find_all('p', class_='company-name')

        while soup:
            for company_name in soup:
                _company_name = company_name.string.strip()
                if len(_company_name) != 0:
                    company_list.add(_company_name)

            pagination_url = self.get_pagination_url()
            soup = self.get_next_soup(pagination_url)

        return company_list



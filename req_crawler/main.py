# -*- coding: utf-8 -*-
import certifi
import urllib3

from settings import base

from bs4 import BeautifulSoup

from db.connect import ConnectDB
from req_crawler.utils import log_process_time


class RequirementCrawler(object):

    def __init__(self, method=None, url=None):
        self.method = method or 'GET'
        self.url = url
        self.http = urllib3.PoolManager(ca_certs=certifi.where())
        self.request = self.http.request(self.method, self.url)
        self.soap = BeautifulSoup(self.request.data, 'lxml')

    def get_pagination_url(self):
        return "https://www.wantedly.com/search?page={0}&q=python&t=projects"

    def get_next_soap(self, http_method, pagination_url):
        request = self.http.request(http_method, pagination_url)
        return BeautifulSoup(request.data, 'lxml')

    @log_process_time
    def get_company_list(self) -> set:
        page_number = 1
        company_list = set()
        pagination_url = self.get_pagination_url()
        request_data = self.request.data.decode('utf-8')

        while True:
            if ('company-name' not in request_data) or (50 < page_number):
                break

            for company_name in self.soap.find_all("p", class_="company-name"):
                _company_name = company_name.string.strip()
                if len(_company_name) != 0:
                    company_list.add(_company_name)

            self.soap = self.get_next_soap('GET',
                                           pagination_url.format(page_number))
            page_number += 1
        return company_list


def main():
    urls = getattr(base, 'CRAWLED_URLS', [])
    if not urls:
        exit()

    conn = ConnectDB()

    for url in urls:
        req_crawler = RequirementCrawler('GET', url)
        company_list = req_crawler.get_company_list()
        exist_company_list = conn.select()
        if company_list - exist_company_list:
            conn.insert(company_list)

if __name__ == '__main__':
    main()
    print('process finished')

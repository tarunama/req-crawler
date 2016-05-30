import certifi
import lxml
import urllib3

from settings import base

from bs4 import BeautifulSoup


class RequirementCrawler(object):

    def __init__(self, method=None, url=None):
        self.method = method or 'GET'
        self.url = url
        self.http = urllib3.PoolManager(ca_certs=certifi.where())
        self.request = self.http.request(self.method, self.url)
        self.soap = BeautifulSoup(self.request.data, 'lxml')

    def get_pagination_url(self):
        return "https://www.wantedly.com/search?page={0}&q=python&t=projects"

    def get_company_list(self) -> set:
        i = 1
        company_names = set()
        pagination_url = self.get_pagination_url()
        while True:
            has_company_name = ('company-name' not in str(self.request.data))
            if has_company_name or 50 < i:
                break

            for company_name in self.soap.find_all("p", class_="company-name"):
                _company_name = company_name.string.strip()
                if len(_company_name) != 0:
                    company_names.add(_company_name)

            request = self.http.request('GET', pagination_url.format(i))
            self.soap = BeautifulSoup(request.data, 'lxml')
            i += 1
        return company_names


if __name__ == '__main__':
    urls = getattr(base, 'CRAWLED_URLS', [])
    if not urls:
        exit()
    else:
        for url in urls:
            req_crawler = RequirementCrawler('GET', url)
            company_list = req_crawler.get_company_list()
            print(company_list)

import pytest
import requests
from scrapy import Spider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy import signals
from scrapy.signalmanager import dispatcher
from urllib.parse import urljoin, urlparse


class LinksSpider(Spider):
    name = "links"
    start_urls = ['https://www.silicondata.com']

    def __init__(self, *args, **kwargs):
        super(LinksSpider, self).__init__(*args, **kwargs)
        self.visited_links = set()
        self.allowed_domain = 'www.silicondata.com'
        self.max_depth = 3

    def parse(self, response):
        current_depth = response.meta.get('depth', 0)
        links = response.css('a::attr(href)').getall()
        for link in links:
            absolute_link = urljoin(response.url, link)

            print(f"Found link: {absolute_link}")
            if self.is_same_domain(absolute_link):
                if absolute_link not in self.visited_links:
                    self.visited_links.add(absolute_link)
                    if self.is_valid_link(absolute_link):
                        yield {'link': absolute_link}

                yield response.follow(absolute_link, self.parse, meta={'depth': current_depth + 1})
            elif current_depth < self.max_depth:
                if absolute_link not in self.visited_links:
                    self.visited_links.add(absolute_link)
                    if self.is_valid_link(absolute_link):
                        yield {'link': absolute_link}

                yield response.follow(absolute_link, self.parse, meta={'depth': current_depth + 1})

    def is_same_domain(self, url):
        parsed_url = urlparse(url)
        return parsed_url.netloc == self.allowed_domain

    def is_valid_link(self, url):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }

            response = requests.head(url, allow_redirects=True, timeout=10, headers=headers)

            if response.status_code == 200:
                return True
            else:
                print(f"Invalid link: {url} (Status Code: {response.status_code})")
                return False
        except requests.RequestException as e:
            print(f"Error accessing {url}: {e}")
            return False


@pytest.fixture(scope="module")
def run_spider():
    process = CrawlerProcess(get_project_settings())
    result = []
    def signal_handler(signal, sender, item, spider):
        if isinstance(item, dict) and 'link' in item:
            result.append(item['link'])

    dispatcher.connect(signal_handler, signal=signals.item_scraped)

    process.crawl(LinksSpider)
    process.start()
    return result

@pytest.mark.order(1)
def test_get_all_links(run_spider):
    links = run_spider
    unique_links = set(links)
    print("======================\n")
    print(unique_links)
    return
    assert len(unique_links) > 0, "No links found on the page"
    broken_link = []
    for link in unique_links:
        status_code = requests.head(link, allow_redirects=True).status_code
        if status_code != 200: #201 204
            broken_link.append(link)
    assert len(broken_link) > 0, f"Broken links {broken_link}"

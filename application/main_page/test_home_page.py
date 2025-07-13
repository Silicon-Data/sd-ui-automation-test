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
    start_urls = ['https://www.silicondata.com']  # Scrapy 会从这里开始抓取

    def __init__(self, *args, **kwargs):
        super(LinksSpider, self).__init__(*args, **kwargs)
        self.visited_links = set()  # 用于存储去重后的链接
        self.allowed_domain = 'www.silicondata.com'  # 主站域名
        self.max_depth = 2  # 外部链接的最大递归深度

    def parse(self, response):
        # 获取当前页面的深度
        current_depth = response.meta.get('depth', 0)

        # 提取页面中的所有 <a> 标签并抓取它们的链接
        links = response.css('a::attr(href)').getall()

        # 将每个链接去重，并添加到 visited_links 中
        for link in links:
            # 使用 urljoin 确保每个链接都是绝对路径
            absolute_link = urljoin(response.url, link)

            # 打印每个抓取到的链接，查看是否有问题
            print(f"Found link: {absolute_link}")

            # 检查链接是否属于同一个域名
            if self.is_same_domain(absolute_link):
                if absolute_link not in self.visited_links:
                    self.visited_links.add(absolute_link)
                    # 检查链接是否有效
                    if self.is_valid_link(absolute_link):
                        yield {'link': absolute_link}

                # 递归抓取页面中的内部链接
                yield response.follow(absolute_link, self.parse, meta={'depth': current_depth + 1})
            elif current_depth < self.max_depth:
                # 对于外部链接，递归深度不超过 2 层
                if absolute_link not in self.visited_links:
                    self.visited_links.add(absolute_link)
                    # 检查链接是否有效
                    if self.is_valid_link(absolute_link):
                        yield {'link': absolute_link}

                # 对外部链接进行递归抓取，但只递归 2 层
                yield response.follow(absolute_link, self.parse, meta={'depth': current_depth + 1})

    def is_same_domain(self, url):
        """
        检查链接是否属于同一个域名
        """
        parsed_url = urlparse(url)
        return parsed_url.netloc == self.allowed_domain

    import requests

    def is_valid_link(self, url):
        """
        检查链接是否可以访问，返回 True 表示可以访问，False 表示不可访问
        """
        try:
            # 定义常见浏览器的 User-Agent
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }

            # 使用 requests.head 请求时加入 headers 来模仿浏览器
            response = requests.head(url, allow_redirects=True, timeout=10, headers=headers)

            # 如果返回状态码是 200，则该链接有效
            if response.status_code == 200:
                return True
            else:
                print(f"Invalid link: {url} (Status Code: {response.status_code})")
                return False
        except requests.RequestException as e:
            # 请求失败，例如超时或连接错误
            print(f"Error accessing {url}: {e}")
            return False


# 使用 pytest fixture 来启动 Scrapy 爬虫
@pytest.fixture(scope="module")
def run_spider():
    # 创建 Scrapy 爬虫的实例
    process = CrawlerProcess(get_project_settings())

    # 存储抓取到的链接
    result = []

    # 捕捉爬虫的信号来存储抓取的链接
    def signal_handler(signal, sender, item, spider):
        if isinstance(item, dict) and 'link' in item:
            result.append(item['link'])

    # 连接信号到 Crawler
    dispatcher.connect(signal_handler, signal=signals.item_scraped)

    # 启动爬虫（传递蜘蛛类，而不是实例）
    process.crawl(LinksSpider)  # Scrapy 会自动使用 start_urls 来开始抓取
    process.start()
    return result

def test_get_all_links(run_spider):
    links = run_spider
    unique_links = set(links)
    assert len(unique_links) > 0, "No links found on the page"
    broken_link = []
    for link in unique_links:
        status_code = requests.head(link, allow_redirects=True).status_code
        if status_code != 200:
            broken_link.append(link)
    assert len(broken_link) > 0, f"Broken links {broken_link}"

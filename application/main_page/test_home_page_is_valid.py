import pytest
import requests
from urllib.parse import urljoin, urlparse
from selenium.webdriver.common.by import By


def is_valid_url(url):
    parsed = urlparse(url)
    return parsed.scheme in ("http", "https")


def get_all_links(driver, base_url):
    driver.get(base_url)
    links = set()

    for element in driver.find_elements(By.TAG_NAME, "a"):
        href = element.get_attribute("href")
        if href and is_valid_url(href):
            absolute_url = urljoin(base_url, href)
            links.add(absolute_url)
    return links


@pytest.mark.parametrize("url", ["https://www.silicondata.com"])
def test_link_health(driver, url):
    broken_links = []
    all_links = get_all_links(driver, url)
    assert len(all_links) > 0, "cannot find any links"
    # check all pages
    for link in all_links:
        try:
            response = requests.head(link, allow_redirects=True, timeout=5)
            if response.status_code >= 400:
                broken_links.append((link, response.status_code))
        except Exception as e:
            broken_links.append((link, str(e)))

    assert not broken_links, f"{'\n'.join([f'{url} (reson: {code})' for url, code in broken_links])}"
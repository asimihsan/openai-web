import sys

import retrying
import typing
from boilerpy3 import extractors
from boilerpy3.extractors import Extractor
from playwright.sync_api import sync_playwright
from playwright.sync_api._generated import Playwright, Browser
from bs4 import BeautifulSoup


class Scraper:
    """ Scraper is a context manager that provides a playwright browser instance.
    """
    p: Playwright
    extractor: Extractor = extractors.ArticleExtractor()
    browser: Browser

    def __init__(self):
        self.p = sync_playwright().start()
        self.browser = self.p.firefox.launch(headless=True)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.browser.close()
        self.p.stop()

    @retrying.retry(
        wait_exponential_multiplier=1000,
        wait_exponential_max=10000,
        stop_max_attempt_number=5,
    )
    def get_content(self, url: typing.Any) -> str:
        if isinstance(url, list):
            return "\n".join(self.get_content(url) for url in url)
        if isinstance(url, dict):
            if "urls" in url and isinstance(url["urls"], list):
                return "\n".join(self.get_content(url) for url in url["urls"])
            url = url["url"]
        elif not isinstance(url, str):
            raise TypeError("url must be of type str or dict")

        with self.browser.new_page() as page:
            page.goto(url)
            page.wait_for_load_state("networkidle", timeout=10000)
            content = page.content()
            return self.extract_content(content)

    def extract_content(self, html_content: str) -> str:
        tree = BeautifulSoup(html_content, "html5lib")
        clean_html_content = tree.prettify()
        return self.extractor.get_content(clean_html_content)


if __name__ == "__main__":
    url = sys.argv[1]
    with Scraper() as scraper:
        print(scraper.get_content(url))

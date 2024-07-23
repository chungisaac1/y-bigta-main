import json
import time
from datetime import datetime
from typing import List, Dict
from argparse import ArgumentParser

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

class HanKyungScraper:
    def __init__(self, start_date: str, end_date: str):
        self.start_date = start_date
        self.end_date = end_date
        self.base_url = "https://www.hankyung.com/all-news"
        self.articles = []

        options = Options()
        options.headless = True
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def scrape(self):
        self.driver.get(self.base_url)
        time.sleep(2)

        while True:
            self._load_more_articles()
            if not self._is_more_articles():
                break

        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        article_links = self._extract_article_links(soup)
        for link in article_links:
            self._scrape_article(link)

        self.driver.quit()

    def _load_more_articles(self):
        try:
            more_button = self.driver.find_element(By.CLASS_NAME, "more-btn")
            more_button.click()
            time.sleep(2)
        except Exception:
            pass

    def _is_more_articles(self) -> bool:
        try:
            self.driver.find_element(By.CLASS_NAME, "more-btn")
            return True
        except Exception:
            return False

    def _extract_article_links(self, soup: BeautifulSoup) -> List[str]:
        links = []
        for article in soup.find_all('div', class_='article'):
            date = article.find('span', class_='date').text.strip()
            if self._is_within_date_range(date):
                link = article.find('a', href=True)['href']
                links.append(link)
        return links

    def _is_within_date_range(self, date: str) -> bool:
        article_date = datetime.strptime(date, "%Y.%m.%d %H:%M")
        start_date = datetime.strptime(self.start_date, "%Y%m%d")
        end_date = datetime.strptime(self.end_date, "%Y%m%d")
        return start_date <= article_date <= end_date

    def _scrape_article(self, url: str):
        self.driver.get(url)
        time.sleep(2)
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')

        date = soup.find('span', class_='date-published').text.strip()
        date_edit = soup.find('span', class_='date-modified').text.strip()
        title = soup.find('h1', class_='title').text.strip()
        article = soup.find('div', class_='article-content').text.strip()

        self.articles.append({
            "date": date,
            "date_edit": date_edit,
            "href": url,
            "title": title,
            "article": article
        })

    def save_to_json(self, output_path: str):
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.articles, f, ensure_ascii=False, indent=4)


def create_parser() -> ArgumentParser:
    today = datetime.today().strftime("%Y%m%d")
    parser = ArgumentParser()
    parser.add_argument("-s", "--start_date", type=str, required=True, help="example: 20240504")
    parser.add_argument("-e", "--end_date", type=str, default=today, help=f"example: {today}")
    parser.add_argument("-o", "--output", type=str, default="output.json", help="output json file path")
    return parser


if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()

    scraper = HanKyungScraper(start_date=args.start_date, end_date=args.end_date)
    scraper.scrape()
    scraper.save_to_json(args.output)

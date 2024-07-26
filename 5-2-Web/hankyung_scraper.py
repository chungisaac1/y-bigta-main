import json
import time
import random
from typing import List, Dict, Any
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup, Tag
import logging
from datetime import datetime

# 로그 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class HanKyungScraper:
    def __init__(self, start_date: str, end_date: str, output: str) -> None:
        self.start_date = start_date
        self.end_date = end_date
        self.output = output
        self.articles_data: List[Dict[str, Any]] = []
        self.driver = self.setup_driver()

    def setup_driver(self) -> webdriver.Chrome:
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        service = ChromeService(executable_path=ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)

    def save_to_json(self) -> None:
        with open(self.output, 'w', encoding='utf-8') as f:
            json.dump(self.articles_data, f, ensure_ascii=False, indent=4)

    def is_within_date_range(self, article_date_str: str) -> bool:
        try:
            article_date = datetime.strptime(article_date_str, '%Y.%m.%d')
            start_date = datetime.strptime(self.start_date, '%Y%m%d')
            end_date = datetime.strptime(self.end_date, '%Y%m%d')
            logging.info(f"비교 날짜: 기사 {article_date}, 시작 {start_date}, 종료 {end_date}")
            return start_date <= article_date <= end_date
        except ValueError as e:
            logging.error(f"날짜 파싱 오류: {e}")
            return False

    def random_sleep(self, min_seconds: int = 2, max_seconds: int = 5) -> None:
        time.sleep(random.uniform(min_seconds, max_seconds))

    def click_load_more_until_date(self, target_date: str) -> None:
        while True:
            try:
                html = self.driver.page_source
                soup = BeautifulSoup(html, "html.parser")

                economy_section = soup.select_one('div.box-module-inner.economyDiv.slick-slide.slick-current.slick-active')
                if not economy_section:
                    logging.info("경제 섹션을 찾을 수 없음. 종료.")
                    break

                daily_news = economy_section.select_one('.daily-news')
                if not daily_news:
                    logging.info("daily-news를 찾을 수 없음. 종료.")
                    break

                day_wraps = daily_news.select('.day-wrap')
                for day_wrap in day_wraps:
                    date_element = day_wrap.select_one(".txt-date")
                    if date_element:
                        article_date_str = date_element.text.strip()
                        if article_date_str == target_date:
                            logging.info(f"목표 날짜 {target_date} 도달")
                            return

                logging.info("더보기 버튼 찾기 시도 중...")
                load_more_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="container"]/div[1]/div[2]/div[3]/div/div/div[3]/div[4]/button'))
                )
                logging.info("더보기 버튼 클릭 시도 중...")
                self.driver.execute_script("window.scrollBy(0, -130);")
                self.random_sleep(4, 6)
                load_more_button.click()
                logging.info("더보기 버튼 클릭 성공")
                self.random_sleep(2, 4)
            except Exception as e:
                logging.info("더 이상 '더보기' 버튼을 찾을 수 없음. 종료.")
                logging.error(f"Error: {e}")
                break

    def scrape(self) -> None:
        try:
            logging.info("웹사이트 접속 시도 중...")
            self.driver.get('https://www.hankyung.com/all-news')
            self.random_sleep(10, 15)

            try:
                economy_menu_xpath = WebDriverWait(self.driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="inner"]/header/div/div[3]/nav/ul/li[3]/a'))
                )
                logging.info("경제 메뉴 클릭 중...")
                economy_menu_xpath.click()
                self.random_sleep(10, 15)

                logging.info("경제 뉴스 페이지 로드 시도")
                WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'daily-news')))
                logging.info("경제 뉴스 페이지 로드 완료")

                self.click_load_more_until_date(self.start_date)

                self.driver.execute_script("window.scrollTo(0, 0);")
                self.random_sleep(5, 7)

                while True:
                    html = self.driver.page_source
                    soup = BeautifulSoup(html, "html.parser")

                    economy_section = soup.select_one('div.box-module-inner.economyDiv.slick-slide.slick-current.slick-active')
                    if not economy_section:
                        logging.info("경제 섹션을 찾을 수 없음. 종료.")
                        break

                    daily_news = economy_section.select_one('.daily-news')
                    if not daily_news:
                        logging.info("daily-news를 찾을 수 없음. 종료.")
                        break

                    day_wraps = daily_news.select('.day-wrap')
                    if not day_wraps:
                        logging.info("day-wrap을 찾을 수 없음. 종료.")
                        break

                    for day_wrap in day_wraps:
                        try:
                            date_element = day_wrap.select_one(".txt-date")
                            if not date_element:
                                logging.warning("날짜 요소를 찾을 수 없음")
                                continue

                            article_date_str = date_element.text.strip()
                            logging.info(f"기사 날짜: {article_date_str}")

                            if not self.is_within_date_range(article_date_str):
                                logging.info(f"날짜가 범위에 포함되지 않음: {article_date_str}")
                                continue

                            logging.info(f"유효한 기사 날짜: {article_date_str}")

                            news_list = day_wrap.select_one(".news-list")
                            if not news_list:
                                logging.warning("news-list를 찾을 수 없음")
                                continue

                            articles = news_list.select("li[data-aid]")
                            for article in articles:
                                try:
                                    txt_cont = article.select_one(".txt-cont")
                                    if not txt_cont:
                                        logging.warning("txt-cont를 찾을 수 없음")
                                        continue

                                    img_element = txt_cont.select_one("h3 a img")
                                    if img_element and img_element.get("alt") == "회원":
                                        logging.info("회원 전용 기사, 건너뜀")
                                        continue

                                    title_element = txt_cont.select_one(".news-tit a")
                                    if not title_element:
                                        logging.warning("title_element를 찾을 수 없음")
                                        continue

                                    title = title_element.text.strip()
                                    href = title_element['href']
                                    lead_element = txt_cont.select_one(".lead")
                                    if lead_element is None:
                                        logging.warning("lead_element를 찾을 수 없음")
                                        continue
                                    lead = lead_element.text.strip()
                                    logging.info(f"기사 추출 중: {title}")

                                    if isinstance(href, str):
                                        self.driver.get(href)
                                        self.random_sleep(3, 6)
                                    else:
                                        logging.error("유효하지 않은 href 타입")
                                        continue

                                    html = self.driver.page_source
                                    soup = BeautifulSoup(html, 'html.parser')

                                    timestamp = soup.find(class_='article-timestamp')
                                    if timestamp and isinstance(timestamp, Tag):
                                        datetime_items = timestamp.find_all(class_='txt-date')
                                        date_entered = datetime_items[0].text.strip() if len(datetime_items) > 0 else None
                                        date_edited = datetime_items[1].text.strip() if len(datetime_items) > 1 else None
                                    else:
                                        logging.warning("timestamp를 찾을 수 없음 또는 유효하지 않은 타입")
                                        continue

                                    article_data = {
                                        'date': date_entered,
                                        'date_edit': date_edited,
                                        'href': href,
                                        'title': title,
                                        'article': lead
                                    }
                                    self.articles_data.append(article_data)

                                    self.driver.back()
                                    WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'daily-news')))
                                    self.random_sleep(3, 5)

                                except Exception as e:
                                    logging.error(f"기사 처리 중 오류 발생: {e}")
                                    continue

                        except Exception as e:
                            logging.error(f"day_wrap 처리 중 오류 발생: {e}")
                            continue

            except Exception as e:
                logging.error(f"경제 메뉴 클릭 중 오류 발생: {e}")

        finally:
            self.save_to_json()
            logging.info("크롤링 완료 후 데이터 저장됨.")
            self.driver.quit()
            logging.info("드라이버 종료됨.")


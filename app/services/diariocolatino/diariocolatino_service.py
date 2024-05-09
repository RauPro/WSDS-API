import os

import requests
from bs4 import BeautifulSoup

from ..driver.engine_controller import CustomEngine
from datetime import date
from datetime import datetime


class DiarioColatinoScrapper:
    ## look
    def __init__(self, query='Feminicidio', 
                 date_start: str = datetime.today().strftime('%Y-%m-%d'), 
                 date_end: str = datetime.today().strftime('%Y-%m-%d'),  num_results = 10):
        self.engine = 'WSDS-Colatino'
        self.query = query
        self.date_start = date_start
        self.date_end = date_end
        self.num_results = num_results

    def init_search_urls(self):
        ce = CustomEngine(engine=os.environ.get(self.engine), query=self.query, date_start = self.date_start, date_end= self.date_end ,num=self.num_results)
        return ce.search()

    def get_url_content(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            h1 = soup.find('h1', class_='name post-title entry-title')
            h1 = h1 if h1 and h1.find('span') else None
            article = soup.find('div', class_='entry')
            date_news = soup.find('span', class_='tie-date').text
            paragraphs = article.find_all('p') if article else []
            news_text = ' '.join(paragraph.text for paragraph in paragraphs)
            new = {
                'title': h1.text if h1 else 'No se encontró el título',
                'text': article.text if article else news_text,
                'source':  'diariocolatino.com' if h1 else 'diariocolatino.com',
                'url': url,
                'sheet_id': url,
                'date_news': date_news
            }
            return new


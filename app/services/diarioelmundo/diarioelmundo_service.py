import os

import requests
from bs4 import BeautifulSoup

from ..driver.engine_controller import CustomEngine
from datetime import date
from datetime import datetime



class DiarioElMundoScrapper:
    def __init__(self, query='Feminicidio', 
                 date_start: str = datetime.today().strftime('%Y-%m-%d'), 
                 date_end: str = datetime.today().strftime('%Y-%m-%d'), num_results = 10):
        self.engine = 'WSDS-ElMundo'
        self.query = query
        self.date_start = date_start
        self.date_end = date_end
        self.num_results = num_results

    def init_search_urls(self):
        ce = CustomEngine(engine=os.environ.get(self.engine), query=self.query, date_start = self.date_start, date_end= self.date_end, num=self.num_results)
        return ce.search()

    def get_url_content(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            h1 = soup.find('h1', class_='title-article')
            subtitle = soup.find('div', class_='article-subTitle')
            article = soup.find('div', class_='article-body')
            date_news = soup.find('time', class_='publishing-date')
            date_string= date_news.get_text(strip=True)
            date_final, hora = date_string.rsplit(' - ', 1)
            new = {
                'title': h1.text if h1 else 'No se encontró el título',
                #'subtitle': subtitle.text if subtitle else 'No se encontró el subtítulo',
                'text': article.text if article else 'No se encontró el texto del articulo',
                'source':  'diario.elmundo.sv',
                'url': url,
                'sheet_id': url,
                'date_news': date_final
                }
            return new
if __name__ == '__main__':
    cl = DiarioElMundoScrapper()
    urls = cl.init_search_urls()
    for url in urls:
        print(cl.get_url_content(url))
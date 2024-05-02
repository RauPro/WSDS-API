import os

import requests
from bs4 import BeautifulSoup
from ..driver.engine_controller import CustomEngine


class DiarioElSalvadorScrapper:
    def __init__(self, query='Feminicidio', num_results = 10):
        self.engine = 'WSDS-DiarioElSalvador'
        self.query = query
        self.num_results = num_results
        
    def init_search_urls(self):
        ce = CustomEngine(engine=os.environ.get(self.engine), query=self.query, num=self.num_results)
        return ce.search()


    def get_url_content(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            title = soup.find('h1')
            content = soup.find('div', class_='entry-content')
            paragraphs = content.find_all('p') if content else []
            news_text = ' '.join(paragraph.text for paragraph in paragraphs)
            article_data = {
                'title': title.text.strip() if title else 'No se encontró el título',
                'text': news_text,
                'source':  'diarioelsalvador.com' if title else 'diarioelsalvador.com',
                'url': url,
                'sheet_id': url
            }
            return article_data

if __name__ == '__main__':
    scrapper = DiarioElSalvadorScrapper()
    urls = scrapper.init_search_urls()
    for url in urls:
        content = scrapper.get_url_content(url)
        print(content)

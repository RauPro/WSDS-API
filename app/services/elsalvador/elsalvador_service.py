import json
import os

from bs4 import BeautifulSoup
import requests
from ..driver.engine_controller import CustomEngine

class ElSalvadorScraper:
    def __init__(self, query='Feminicidio', num_results=10):
        self.engine = 'WSDS-ElSalvador'
        self.query = query
        self.num_results = num_results


    def init_search_urls(self):
        ce = CustomEngine(engine = os.environ.get(self.engine), query = self.query, num = self.num_results)
        return ce.search()

    def get_url_content(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            article = soup.find('article', class_='detail')
            h1 = article.find('h1') if article else None
            paragraphs = article.find_all('p') if article else []
            news_text = ' '.join(paragraph.text for paragraph in paragraphs)
            new = {
                'title': h1.text if h1 else 'No se encontró el título',
                'text': news_text}
            return new


if __name__ == '__main__':
    scraper = ElSalvadorScraper("Homicidio")
    urls = scraper.init_search_urls()
    content_urls = []
    for url in urls:
        content_urls.append(scraper.get_url_content(url))
    print(content_urls)
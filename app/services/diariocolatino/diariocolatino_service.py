import requests
from bs4 import BeautifulSoup


class DiarioColatinoScrapper:
    def __init__(self, query='Feminicidio'):
        self.base_url = 'https://www.diariocolatino.com/?s=' + query

    def init_search_urls(self):
        response = requests.get(self.base_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            articles = soup.find_all('article', class_='item-list')
            list_urls = []
            for article in articles:
                link = article.find('a', class_='more-link')
                list_urls.append(link['href'])
            return list_urls

    def get_url_content(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            h1 = soup.find('h1', class_='name post-title entry-title')
            h1 = h1 if h1.find('span') else None
            article = soup.find('div', class_='entry')
            paragraphs = article.find_all('p') if article else []
            news_text = ' '.join(paragraph.text for paragraph in paragraphs)
            new = {
                'title': h1.text if h1 else 'No se encontró el título',
                'text': article.text if article else news_text,
                'source':  'diariocolatino.com' if h1 else 'diariocolatino.com'
            }
            return new


import requests
from bs4 import BeautifulSoup

class DiarioElSalvadorScrapper:
    def __init__(self, query='Feminicidio'):
        self.base_url = 'https://diarioelsalvador.com/?s=' + query
        
    def init_search_urls(self):
        response = requests.get(self.base_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            container = soup.find('div', class_='jeg_block_container')
            articles = container.find_all('article') if container else []
            list_urls = []
            for article in articles:
                link = article.find('a')
                if link and 'href' in link.attrs:
                    list_urls.append(link['href'])
            return list_urls


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
                'text': news_text
            }
            return article_data

if __name__ == '__main__':
    scrapper = DiarioElSalvadorScrapper()
    urls = scrapper.init_search_urls()
    for url in urls:
        content = scrapper.get_url_content(url)
        print(content)

import requests
from bs4 import BeautifulSoup

class DiarioElMundoScrapper:
    def __init__(self, query='Feminicidio'):
        self.base_url = 'https://diario.elmundo.sv/search?query=' + query

    def init_search_urls(self):
        response = requests.get(self.base_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            search_div = soup.find('div', class_='mundo-search-widget')
            articles = search_div.find_all('div', class_="article-title")
            list_urls = []
            for article in articles:
                link = article.find('a')
                list_urls.append(link['href'])
            return list_urls

    def get_url_content(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            h1 = soup.find('h1', class_='title-article')
            subtitle = soup.find('div', class_='article-subTitle')
            article = soup.find('div', class_='article-body')
            new = {
                'title': h1.text if h1 else 'No se encontró el título',
                'subtitle': subtitle.text if subtitle else 'No se encontró el subtítulo',
                'text': article.text if article else 'No se encontró el texto del articulo',}
            return new
if __name__ == '__main__':
    cl = DiarioElMundoScrapper()
    urls = cl.init_search_urls()
    for url in urls:
        print(cl.get_url_content(url))
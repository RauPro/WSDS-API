import json
from bs4 import BeautifulSoup
import requests

class ElSalvadorScraper:
    def __init__(self, query='Feminicidio', num_results=10):
        self.base_url = 'https://cse.google.com/cse/element/v1'
        self.params = {
            'rsz': 'filtered_cse',
            'num': str(num_results),
            'hl': 'es',
            'source': 'gcsc',
            'gss': '.com',
            'cselibv': '8435450f13508ca1',
            'cx': '006989654994863071413:2meag52dzuc',
            'q': query,
            'safe': 'off',
            'cse_tok': 'AB-tC_7a0Ez39zxZ07Ron0rUqUwd:1707012182430',
            'sort': 'date',
            'exp': 'cc',
            'fexp': '72485392,72485391',
            'oq': query,
            'gs_l': 'partner-generic.12...591052.592998.2.600379.11.11.0.0.0.0.129.925.7j4.11.0.csems,nrl=10...0....1.34.partner-generic..37.9.753.tBzSfQsdAWs',
            'callback': 'google.search.cse.api11887',
        }

    def init_search_urls(self):
        response = requests.get(self.base_url, params=self.params)
        raw_ans = response.content.decode('utf-8')
        start = raw_ans.find('{')
        end = raw_ans.rfind('}') + 1
        json_str = raw_ans[start:end]
        json_data = json.loads(json_str)
        search_urls = [element["url"] for element in json_data.get("results", [])]
        return search_urls

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



import os
from typing import List

import requests
from bs4 import BeautifulSoup

from ..driver.engine_controller import CustomEngine


class ElSalvadorScraper:
    """
    A web scraper for extracting news articles related to a specific query from Salvadoran websites.

    Attributes:
        engine (str): The name of the custom search engine to use for searching.
        query (str): The search query to use for finding relevant news articles.
        num_results (int): The number of search results to retrieve.

    Methods:
        __init__(self, query='Feminicidio', num_results=10):
            Initializes a new instance of the ElSalvadorScraper class.

        init_search_urls(self) -> List[str]:
            Initializes the search URLs based on the specified query and number of results.
            Returns a list of search result URLs.

        get_url_content(self, url: str) -> dict:
            Retrieves the content of a specific URL and extracts relevant information.
            Returns a dictionary containing the extracted news article data.

    Example:
        scraper = ElSalvadorScraper("Homicidio")
        urls = scraper.init_search_urls()
        content_urls = []
        for url in urls:
            content_urls.append(scraper.get_url_content(url))
        print(content_urls)
    """

    def __init__(self, query='Feminicidio', num_results=10):
        """
        Initializes a new instance of the ElSalvadorScraper class.

        Args:
            query (str, optional): The search query to use for finding relevant news articles. Defaults to 'Feminicidio'.
            num_results (int, optional): The number of search results to retrieve. Defaults to 10.
        """
        self.engine = 'WSDS-ElSalvador'
        self.query = query
        self.num_results = num_results

    def init_search_urls(self) -> List[str]:
        """
        Initializes the search URLs based on the specified query and number of results.

        Returns:
            List[str]: A list of search result URLs.
        """
        ce = CustomEngine(engine=os.environ.get(self.engine), query=self.query, num=self.num_results)
        return ce.search()

    def get_url_content(self, url: str) -> dict:
        """
        Retrieves the content of a specific URL and extracts relevant information.

        Args:
            url (str): The URL of the news article to extract content from.

        Returns:
            dict: A dictionary containing the extracted news article data.
                - 'title' (str): The title of the news article.
                - 'text' (str): The text content of the news article.
                - 'url' (str): The URL of the news article.
                - 'sheet_id' (str): The sheet ID associated with the news article (same as the URL).
        """
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            article = soup.find('article', class_='detail')
            h1 = article.find('h1') if article else None
            paragraphs = article.find_all('p') if article else []
            news_text = ' '.join(paragraph.text for paragraph in paragraphs)
            new = {
                'title': h1.text if h1 else 'No se encontró el título',
                'text': news_text,
                'url': url,
                'sheet_id': url
            }
            return new


if __name__ == '__main__':
    scraper = ElSalvadorScraper("Homicidio")
    urls = scraper.init_search_urls()
    content_urls = []
    for url in urls:
        content_urls.append(scraper.get_url_content(url))
    print(content_urls)

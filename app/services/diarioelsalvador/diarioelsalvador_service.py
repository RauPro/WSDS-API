import os
import re
from datetime import datetime
from typing import List

import requests
from bs4 import BeautifulSoup

from ..driver.engine_controller import CustomEngine


class DiarioElSalvadorScrapper:
    """
    A web scraper for extracting news articles from the Diario El Salvador website.

    Attributes:
        engine (str): The name of the custom search engine to use for searching.
        query (str): The search query to use for finding relevant news articles.
        date_start (str): The start date for filtering news articles (optional).
        date_end (str): The end date for filtering news articles (optional).
        num_results (int): The number of search results to retrieve.

    Methods:
        __init__(self, query='Feminicidio', date_start='', date_end='', num_results=10):
            Initializes a new instance of the DiarioElSalvadorScrapper class.

        init_search_urls(self) -> List[str]:
            Initializes the search URLs based on the specified query, date range, and number of results.
            Returns a list of search result URLs.

        get_url_content(self, url: str) -> dict:
            Retrieves the content of a specific URL and extracts relevant information.
            Returns a dictionary containing the extracted news article data.

    Example:
        scrapper = DiarioElSalvadorScrapper()
        urls = scrapper.init_search_urls()
        for url in urls:
            content = scrapper.get_url_content(url)
            print(content)
    """

    def __init__(self, query='Feminicidio',
                 date_start: str = "",
                 date_end: str = "", num_results=10, start_from = 0):
        """
        Initializes a new instance of the DiarioElSalvadorScrapper class.

        Args:
            query (str, optional): The search query to use for finding relevant news articles. Defaults to 'Feminicidio'.
            date_start (str, optional): The start date for filtering news articles. Defaults to an empty string.
            date_end (str, optional): The end date for filtering news articles. Defaults to an empty string.
            num_results (int, optional): The number of search results to retrieve. Defaults to 10.
        """
        self.engine = 'WSDS-DiarioElSalvador'
        self.query = query
        self.date_start = date_start
        self.date_end = date_end
        self.num_results = num_results
        self.start_from = start_from

    def init_search_urls(self) -> List[str]:
        """
        Initializes the search URLs based on the specified query, date range, and number of results.

        Returns:
            List[str]: A list of search result URLs.
        """
        ce = CustomEngine(engine=os.environ.get(self.engine), query=self.query, date_start=self.date_start,
                          date_end=self.date_end, num=self.num_results, start_from=self.start_from)
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
                - 'source' (str): The source of the news article.
                - 'url' (str): The URL of the news article.
                - 'sheet_id' (str): The sheet ID associated with the news article (same as the URL).
                - 'date' (str): The publication date of the news article.
        """
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            title = soup.find('h1')
            content = soup.find('div', class_='entry-content')
            paragraphs = content.find_all('p') if content else []
            news_text = ' '.join(paragraph.text for paragraph in paragraphs)

            date_news = soup.find('div', class_='jeg_meta_date')

            if (date_news is not None):
                date_news = date_news.a.get_text(strip=True)
                date_news = date_formate(date_news)
            else:
                date_news = "No se encontro fecha"

            article_data = {
                'title': title.text.strip() if title else 'No se encontró el título',
                'text': news_text,
                'source': 'diarioelsalvador.com' if title else 'diarioelsalvador.com',
                'url': url,
                'sheet_id': url,
                'date': date_news
            }
            return article_data


def date_formate(date_text: str) -> str:
    """
    Formats a date string from the format "day de month de year" to "yyyy-mm-dd".

    Args:
        date_text (str): The date string to be formatted.

    Returns:
        str: The formatted date string in the format "yyyy-mm-dd".
             If the input date string is not in the expected format, returns an error message.

    Example:
        formatted_date = date_formate("15 de junio de 2023")
        print(formatted_date)  # Output: "2023-06-15"
    """
    exp_regular = r'(\d+)\s+de\s+(\w+)\s+de\s+(\d+)'
    match = re.match(exp_regular, date_text)

    if match:
        day = match.group(1)
        month = match.group(2)
        year = match.group(3)
        months = {
            'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4,
            'mayo': 5, 'junio': 6, 'julio': 7, 'agosto': 8,
            'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
        }
        num_month = months[month.lower()]
        date_obj = datetime(int(year), num_month, int(day))

        return date_obj.strftime("%Y-%m-%d")
    else:
        return "No se pudo encontrar una fecha válida en el formato proporcionado. Diario el salvaador"


if __name__ == '__main__':
    scrapper = DiarioElSalvadorScrapper()
    urls = scrapper.init_search_urls()
    for url in urls:
        content = scrapper.get_url_content(url)
        print(content)

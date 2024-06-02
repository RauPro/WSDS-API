import os
import re
from typing import List

import requests
from bs4 import BeautifulSoup

from ..driver.engine_controller import CustomEngine
from datetime import date
from datetime import datetime


class DiarioElMundoScrapper:
    """
    A web scraper for extracting news articles from the Diario El Mundo website.

    Attributes:
        engine (str): The name of the custom search engine to use for searching.
        query (str): The search query to use for finding relevant news articles.
        date_start (str): The start date for filtering news articles (optional).
        date_end (str): The end date for filtering news articles (optional).
        num_results (int): The number of search results to retrieve.

    Methods:
        __init__(self, query='Feminicidio', date_start='', date_end='', num_results=10):
            Initializes a new instance of the DiarioElMundoScrapper class.

        init_search_urls(self) -> List[str]:
            Initializes the search URLs based on the specified query, date range, and number of results.
            Returns a list of search result URLs.

        get_url_content(self, url: str) -> dict:
            Retrieves the content of a specific URL and extracts relevant information.
            Returns a dictionary containing the extracted news article data.

    Example:
        scrapper = DiarioElMundoScrapper()
        urls = scrapper.init_search_urls()
        for url in urls:
            content = scrapper.get_url_content(url)
            print(content)
    """

    def __init__(self, query='Feminicidio',
                 date_start: str = "",
                 date_end: str = "", num_results=10):
        """
        Initializes a new instance of the DiarioElMundoScrapper class.

        Args:
            query (str, optional): The search query to use for finding relevant news articles. Defaults to 'Feminicidio'.
            date_start (str, optional): The start date for filtering news articles. Defaults to an empty string.
            date_end (str, optional): The end date for filtering news articles. Defaults to an empty string.
            num_results (int, optional): The number of search results to retrieve. Defaults to 10.
        """
        self.engine = 'WSDS-ElMundo'
        self.query = query
        self.date_start = date_start
        self.date_end = date_end
        self.num_results = num_results

    def init_search_urls(self):
        """
        Initializes the search URLs based on the specified query, date range, and number of results.

        Returns:
            List[str]: A list of search result URLs.
        """
        ce = CustomEngine(engine=os.environ.get(self.engine), query=self.query, date_start=self.date_start,
                          date_end=self.date_end, num=self.num_results)
        return ce.search()

    def get_url_content(self, url: str) -> List[str]:
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
            h1 = soup.find('h1', class_='title-article')
            subtitle = soup.find('div', class_='article-subTitle')
            article = soup.find('div', class_='article-body')

            raw_date = soup.find('time', class_='publishing-date')
            date_news = ""

            if (raw_date is not None):
                date_news = raw_date.get_text(strip=True).rsplit(' - ', 1)[0]
                date_news = date_formate(date_news)
            else:
                date_news = "No se encontro fecha"

            new = {
                'title': h1.text if h1 else 'No se encontró el título',
                # 'subtitle': subtitle.text if subtitle else 'No se encontró el subtítulo',
                'text': article.text if article else 'No se encontró el texto del articulo',
                'source': 'diario.elmundo.sv',
                'url': url,
                'sheet_id': url,
                'date': date_news,
            }
            return new


if __name__ == '__main__':
    cl = DiarioElMundoScrapper()
    urls = cl.init_search_urls()
    for url in urls:
        print(cl.get_url_content(url))


def date_formate(date_text: str) -> str:
    """
    Formats a date string from the format "day_week day, month year" to "yyyy-mm-dd".

    Args:
        date_text (str): The date string to be formatted.

    Returns:
        str: The formatted date string in the format "yyyy-mm-dd".
             If the input date string is not in the expected format, returns an error message.

    Example:
        formatted_date = date_formate("Lunes 12, junio 2023")
        print(formatted_date)  # Output: "2023-06-12"
    """
    exp_regular = r'(\w+)\s+(\d+),\s+(\w+)\s+(\d+)'
    match = re.match(exp_regular, date_text)

    if match:
        day_week = match.group(1)
        day = match.group(2)
        month = match.group(3)
        year = match.group(4)

        months = {
            'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4,
            'mayo': 5, 'junio': 6, 'julio': 7, 'agosto': 8,
            'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
        }

        num_month = months[month.lower()]

        date_obj = datetime(int(year), num_month, int(day))

        return date_obj.strftime("%Y-%m-%d")
    else:
        return "No se pudo encontrar una fecha válida en el formato proporcionado: Diario EL mundo"

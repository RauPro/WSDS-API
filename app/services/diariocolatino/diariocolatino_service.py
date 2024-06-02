import os
import re
from typing import List

import requests
from bs4 import BeautifulSoup

from ..driver.engine_controller import CustomEngine
from datetime import date
from datetime import datetime


class DiarioColatinoScrapper:
    """
    A web scraper for extracting news articles from the Diario Colatino website.

    Attributes:
        engine (str): The name of the custom search engine to use for searching.
        query (str): The search query to use for finding relevant news articles.
        date_start (str): The start date for filtering news articles (optional).
        date_end (str): The end date for filtering news articles (optional).
        num_results (int): The number of search results to retrieve.

    Methods:
        __init__(self, query='Feminicidio', date_start='', date_end='', num_results=10):
            Initializes a new instance of the DiarioColatinoScrapper class.

        init_search_urls(self) -> List[str]:
            Initializes the search URLs based on the specified query, date range, and number of results.
            Returns a list of search result URLs.

        get_url_content(self, url: str) -> dict:
            Retrieves the content of a specific URL and extracts relevant information.
            Returns a dictionary containing the extracted news article data.

    Example:
        scrapper = DiarioColatinoScrapper()
        urls = scrapper.init_search_urls()
        for url in urls:
            content = scrapper.get_url_content(url)
            print(content)
    """

    def __init__(self, query='Feminicidio',
                 date_start: str = "",
                 date_end: str = "", num_results=10):
        """
        Initializes a new instance of the DiarioColatinoScrapper class.

        Args:
            query (str, optional): The search query to use for finding relevant news articles. Defaults to 'Feminicidio'.
            date_start (str, optional): The start date for filtering news articles. Defaults to an empty string.
            date_end (str, optional): The end date for filtering news articles. Defaults to an empty string.
            num_results (int, optional): The number of search results to retrieve. Defaults to 10.
        """
        self.engine = 'WSDS-Colatino'
        self.query = query
        self.date_start = date_start
        self.date_end = date_end
        self.num_results = num_results

    def init_search_urls(self) -> List[str]:
        """
        Initializes the search URLs based on the specified query, date range, and number of results.

        Returns:
            List[str]: A list of search result URLs.
        """
        ce = CustomEngine(engine=os.environ.get(self.engine), query=self.query, date_start=self.date_start,
                          date_end=self.date_end, num=self.num_results)
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
            h1 = soup.find('h1', class_='name post-title entry-title')
            h1 = h1 if h1 and h1.find('span') else None
            article = soup.find('div', class_='entry')
            date_news = soup.find('span', class_='tie-date')

            if (date_news is not None):
                date_news = date_formate(date_news.text)
            else:
                date_news = "No se encontro fecha"

            paragraphs = article.find_all('p') if article else []
            news_text = ' '.join(paragraph.text for paragraph in paragraphs)
            new = {
                'title': h1.text if h1 else 'No se encontró el título',
                'text': article.text if article else news_text,
                'source': 'diariocolatino.com' if h1 else 'diariocolatino.com',
                'url': url,
                'sheet_id': url,
                'date': date_news
            }
            return new


def date_formate(date_text: str) -> str:
    """
    Formats a date string from the format "day month, year" to "yyyy-mm-dd".

    Args:
        date_text (str): The date string to be formatted.

    Returns:
        str: The formatted date string in the format "yyyy-mm-dd".
             If the input date string is not in the expected format, returns an error message.

    Example:
        formatted_date = date_formate("12 junio, 2023")
        print(formatted_date)  # Output: "2023-06-12"
    """
    exp_regular = r'(\d+)\s+(\w+),\s+(\d+)'
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
        return "No se pudo encontrar una fecha válida en el formato proporcionado: Diario Colatino"

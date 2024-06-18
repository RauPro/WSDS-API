import json
import os
from datetime import datetime
from typing import List

import requests


class CustomEngine:
    """
    A class for performing custom search using the Google Custom Search API.

    Attributes:
        base_url (str): The base URL for the Google Custom Search API.
        params (dict): The parameters for the API request.

    Methods:
        __init__(self, engine: str, query: str, date_start: str = '', date_end: str = '', num: int = 10):
            Initializes a new instance of the CustomEngine class.

        search(self) -> List[str]:
            Performs the custom search and returns a list of URLs from the search results.

    Example:
        os.environ['WSDS-DiarioElSalvador'] = 'key'
        os.environ['WSDS-LaPrensa'] = 'key'
        os.environ['WSDS-ElMundo'] = 'key'
        os.environ['WSDS-ElSalvador'] = 'key'
        os.environ['WSDS-Colatino'] = 'key'

        ce = CustomEngine(engine=os.environ.get('WSDS-ElSalvador'), query="Homicidio")
        urls = ce.search()
        print(urls)
    """

    def __init__(self, engine, query, date_start='', date_end='', num=10, start_from = 0):
        """
        Initializes a new instance of the CustomEngine class.

        Args:
            engine (str): The ID of the custom search engine to use.
            query (str): The search query.
            date_start (str, optional): The start date for filtering search results (format: "YYYY-MM-DD"). Defaults to an empty string.
            date_end (str, optional): The end date for filtering search results (format: "YYYY-MM-DD"). Defaults to an empty string.
            num (int, optional): The number of search results to retrieve. Defaults to 10.
        """
        self.base_url = 'https://customsearch.googleapis.com/customsearch/v1'

        formatted = date_start

        if date_start != '' or date_end != '':
            date_start = datetime.strptime(date_start, "%Y-%m-%d").strftime("%Y%m%d")
            date_end = datetime.strptime(date_end, "%Y-%m-%d").strftime("%Y%m%d")
            formatted = f'date:r:{date_start}:{date_end}'
        else:
            formatted = 'date'

        self.params = {
            'num': str(num),
            'hl': 'es',
            'cx': engine,
            'q': query,
            'safe': 'off',
            'sort': formatted,
            # r:yyyymmdd:yyyymmdd
            'oq': query,
            'key': 'AIzaSyBhAxY8-IuaOF_B9qunF4TZUwpgizi8XuE',
            'start': start_from
        }

    def search(self) -> tuple:
        """
       Performs the custom search and returns a list of URLs from the search results.

       Returns:
           List[str]: A list of URLs from the search results.
       """
        response = requests.get(self.base_url, params=self.params)
        raw_ans = response.content.decode('utf-8')
        json_data = json.loads(raw_ans)
        urls = []
        for element in json_data.get("items", []):
            urls.append(element["link"])
        print(urls)
        print(response.url)
        return urls, json_data.get("searchInformation").get("totalResults", "10")


if __name__ == "__main__":
    os.environ['WSDS-DiarioElSalvador'] = 'f370050651691467b'
    os.environ['WSDS-LaPrensa'] = 'e1db5aa65d1f24626'
    os.environ['WSDS-ElMundo'] = '26488facb20df42f8'
    os.environ['WSDS-ElSalvador'] = '101f8fa79b60b4f47'
    os.environ['WSDS-Colatino'] = 'b34fd545e642d4e3f'

    ce = CustomEngine(engine=os.environ.get('WSDS-ElSalvador'), query="Homicidio")
    ce.search()

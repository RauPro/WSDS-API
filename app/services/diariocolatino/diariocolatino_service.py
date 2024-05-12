import os
import re

import requests
from bs4 import BeautifulSoup

from ..driver.engine_controller import CustomEngine
from datetime import date
from datetime import datetime


class DiarioColatinoScrapper:
    ## look
    def __init__(self, query='Feminicidio', 
                 date_start: str = "", 
                 date_end: str = "",  num_results = 10):
        self.engine = 'WSDS-Colatino'
        self.query = query
        self.date_start = date_start
        self.date_end = date_end
        self.num_results = num_results

    def init_search_urls(self):
        ce = CustomEngine(engine=os.environ.get(self.engine), query=self.query, date_start = self.date_start, date_end= self.date_end, num=self.num_results)
        return ce.search()
        

    def get_url_content(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            h1 = soup.find('h1', class_='name post-title entry-title')
            h1 = h1 if h1 and h1.find('span') else None
            article = soup.find('div', class_='entry')
            date_news = soup.find('span', class_='tie-date')
            
            if(date_news is not None):
                date_news = date_formate(date_news.text)
            else:
                date_news =  "No se encontro fecha"
            
            
            paragraphs = article.find_all('p') if article else []
            news_text = ' '.join(paragraph.text for paragraph in paragraphs)
            new = {
                'title': h1.text if h1 else 'No se encontró el título',
                'text': article.text if article else news_text,
                'source':  'diariocolatino.com' if h1 else 'diariocolatino.com',
                'url': url,
                'sheet_id': url,
                'date_news': date_news
            }
            return new


def date_formate(date_text):
    # Expresión regular para extraer día, mes y año
    exp_regular = r'(\d+)\s+(\w+),\s+(\d+)'
    match = re.match(exp_regular, date_text)

    if match:
        day = match.group(1)
        month = match.group(2)
        year = match.group(3)

        # Mapear el nombre del mes a su número correspondiente
        months = {
            'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4,
            'mayo': 5, 'junio': 6, 'julio': 7, 'agosto': 8,
            'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
        }

        # Obtener el número del mes
        num_month = months[month.lower()]

        # Crear un objeto datetime
        fecha_objeto = datetime(int(year), num_month, int(day))

        # Formatear la fecha en el formato deseado (year-month-day)
        fecha_formateada = fecha_objeto.strftime("%Y-%m-%d")

        return fecha_formateada  # Salida: yyyy-mm-dd
    else:
        return "No se pudo encontrar una fecha válida en el formato proporcionado: Diario Colatino"

import os
import re

import requests
from bs4 import BeautifulSoup

from ..driver.engine_controller import CustomEngine
from datetime import date
from datetime import datetime



class DiarioElMundoScrapper:
    def __init__(self, query='Feminicidio', 
                 date_start: str = datetime.today().strftime('%Y-%m-%d'), 
                 date_end: str = datetime.today().strftime('%Y-%m-%d'), num_results = 10):
        self.engine = 'WSDS-ElMundo'
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
            h1 = soup.find('h1', class_='title-article')
            subtitle = soup.find('div', class_='article-subTitle')
            article = soup.find('div', class_='article-body')
            
            date_news, hour_news = soup.find('time', class_='publishing-date').get_text(strip=True).rsplit(' - ', 1)
            print(date_news)
            date_final = date_formate(date_news)
            print(date_final)
            
            new = {
                'title': h1.text if h1 else 'No se encontró el título',
                #'subtitle': subtitle.text if subtitle else 'No se encontró el subtítulo',
                'text': article.text if article else 'No se encontró el texto del articulo',
                'source':  'diario.elmundo.sv',
                'url': url,
                'sheet_id': url,
                'date_news': date_final
                }
            return new
if __name__ == '__main__':
    cl = DiarioElMundoScrapper()
    urls = cl.init_search_urls()
    for url in urls:
        print(cl.get_url_content(url))
        

def date_formate(date_text):
    # Expresión regular para extraer día, mes y año
    exp_regular = r'(\w+)\s+(\d+),\s+(\w+)\s+(\d+)'
    match = re.match(exp_regular, date_text)

    if match:
        day_week = match.group(1)
        day = match.group(2)
        month = match.group(3)
        year = match.group(4)

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
        return "No se pudo encontrar una fecha válida en el formato proporcionado."

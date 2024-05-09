import os
import re

import requests
from bs4 import BeautifulSoup
from ..driver.engine_controller import CustomEngine
from datetime import date
from datetime import datetime


class DiarioElSalvadorScrapper:
    def __init__(self, query='Feminicidio',  
                 date_start: str = datetime.today().strftime('%Y-%m-%d'), 
                 date_end: str = datetime.today().strftime('%Y-%m-%d'), num_results = 10):
        self.engine = 'WSDS-DiarioElSalvador'
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
            title = soup.find('h1')
            content = soup.find('div', class_='entry-content')   
            paragraphs = content.find_all('p') if content else []
            news_text = ' '.join(paragraph.text for paragraph in paragraphs)
            
            date_news = soup.find('div', class_='jeg_meta_date')       
            date_text = date_news.a.get_text(strip=True)    
            date_final = date_formate(date_text)
            
            article_data = {
                'title': title.text.strip() if title else 'No se encontró el título',
                'text': news_text,
                'source':  'diarioelsalvador.com' if title else 'diarioelsalvador.com',
                'url': url,
                'sheet_id': url,
                'date_news': date_final
            }
            return article_data

def date_formate(date_text):
    # Expresión regular para extraer día, mes y año
    exp_regular = r'(\d+)\s+de\s+(\w+)\s+de\s+(\d+)'
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
        return "No se pudo encontrar una fecha válida en el formato proporcionado."

if __name__ == '__main__':
    scrapper = DiarioElSalvadorScrapper()
    urls = scrapper.init_search_urls()
    for url in urls:
        content = scrapper.get_url_content(url)
        print(content)

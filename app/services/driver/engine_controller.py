import json
from datetime import datetime
import requests
import os

class CustomEngine:
    def __init__(self, engine, query , date_start ='', date_end='', num = 10,):
        self.base_url = 'https://customsearch.googleapis.com/customsearch/v1'
        formatted = date_start
        if date_start != '' or date_end != '':
            formatted = f'date:r:{date_start}:{date_end}'
        else:
            formatted = 'date'
        self.params = {
            'num': str(num),
            'hl': 'es',
            'cx': engine,
            'q': query,
            'safe': 'off',
            'sort': formatted,  # r:yyyymmdd:yyyymmdd
            'oq': query,
            'key': 'AIzaSyBhAxY8-IuaOF_B9qunF4TZUwpgizi8XuE'
        }
    def search(self):
        response = requests.get(self.base_url, params=self.params)
        raw_ans = response.content.decode('utf-8')
        json_data = json.loads(raw_ans)
        urls = []
        for element in json_data.get("items", []):
            urls.append(element["link"])
        print(urls)
        print(response.url)
        return urls

if __name__ == "__main__":
    os.environ['WSDS-DiarioElSalvador'] = 'f370050651691467b'
    os.environ['WSDS-LaPrensa'] = 'e1db5aa65d1f24626'
    os.environ['WSDS-ElMundo'] = '26488facb20df42f8'
    os.environ['WSDS-ElSalvador'] = '101f8fa79b60b4f47'
    os.environ['WSDS-Colatino'] = 'b34fd545e642d4e3f'


    ce = CustomEngine(engine = os.environ.get('WSDS-ElSalvador'), query = "Homicidio")
    ce.search()
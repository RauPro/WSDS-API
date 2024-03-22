from fastapi import FastAPI

from app.controllers.notices_controller import test_create_notice
from services.diariocolatino import DiarioColatinoScrapper
from services.elsalvador import ElSalvadorScraper
from services.diarioelmundo import DiarioElMundoScrapper
from services.diarioelsalvador import DiarioElSalvadorScrapper
from services.driver import classify_new
from env import env

app = FastAPI()

env.set_env()

@app.get("/poc")
async def poc(search: str = ""):
    scraper = ElSalvadorScraper(search)
    urls = scraper.init_search_urls()
    content_urls = []
    for url in urls:
        content_urls.append(scraper.get_url_content(url))
    return content_urls

@app.get("/colatino")
async def poc(search: str = ""):
    scraper = DiarioColatinoScrapper(search)
    urls = scraper.init_search_urls()
    content_urls = []
    for url in urls:
        content_urls.append(scraper.get_url_content(url))
    return content_urls

@app.get("/diarioelmundo")
async def poc(search: str = ""):
    scraper = DiarioElMundoScrapper(search)
    urls = scraper.init_search_urls()
    content_urls = []
    for url in urls:
        content_urls.append(scraper.get_url_content(url))
    return content_urls


@app.get("/diarioelsalvador")
async def poc(search: str = "Feminicidio"):
    scraper = DiarioElSalvadorScrapper(search)
    urls = scraper.init_search_urls()
    content_urls = []
    for url in urls:
        content_urls.append(scraper.get_url_content(url))
    return content_urls

@app.get("/global")
async def poc(search: str = "Feminicidio"):
    scraperDiarioElSalvadorScrapper = DiarioElSalvadorScrapper(search)
    scraperDiarioColatinoScrapper = DiarioColatinoScrapper(search)
    scraperDiarioElMundoScrapper = DiarioElMundoScrapper(search)
    urlsDiarioElSalvadorScrapper = scraperDiarioElSalvadorScrapper.init_search_urls()
    content_urls = []
    for url in urlsDiarioElSalvadorScrapper:
        content_urls.append(scraperDiarioElSalvadorScrapper.get_url_content(url))

    urlsDiarioColatinoScrapper = scraperDiarioColatinoScrapper.init_search_urls()
    content_urls = []
    for url in urlsDiarioColatinoScrapper:
        content_urls.append(scraperDiarioColatinoScrapper.get_url_content(url))

    urlsDiarioElMundoScrapper = scraperDiarioElMundoScrapper.init_search_urls()
    content_urls = []
    for url in urlsDiarioElMundoScrapper:
        content_urls.append(scraperDiarioElMundoScrapper.get_url_content(url))

    for i in range(len(content_urls)):
        content_urls[i]['tag'] = classify_new(content_urls[i]['text'])

    return content_urls




if __name__ == '__main__':
    test_create_notice()
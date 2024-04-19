from fastapi import FastAPI

##from app.controllers.notices_controller import test_create_notice
from .services.diariocolatino import DiarioColatinoScrapper
from .services.elsalvador import ElSalvadorScraper
from .services.diarioelmundo import DiarioElMundoScrapper
from .services.diarioelsalvador import DiarioElSalvadorScrapper
from .services.driver import classify_new
from .env import env
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

env.set_env()

origins = [
    "http://127.0.0.1:8000",
    "http://localhost:4200"
]

app.add_middleware(CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/poc")
async def poc(search: str = ""):
    scraper = ElSalvadorScraper(search)
    urls = scraper.init_search_urls()
    content_urls = []
    for url in urls:
        content_urls.append(scraper.get_url_content(url))
    return content_urls

@app.get("/colatino")
async def colatino(search: str = ""):
    scraper = DiarioColatinoScrapper(search)
    urls = scraper.init_search_urls()
    content_urls = []
    for url in urls:
        content_urls.append(scraper.get_url_content(url))
    return content_urls

@app.get("/diarioelmundo")
async def diarioelmundo(search: str = ""):
    scraper = DiarioElMundoScrapper(search)
    urls = scraper.init_search_urls()
    content_urls = []
    for url in urls:
        content_urls.append(scraper.get_url_content(url))
    return content_urls


@app.get("/diarioelsalvador")
async def diarioelsalvador(search: str = "Feminicidio"):
    scraper = DiarioElSalvadorScrapper(search)
    urls = scraper.init_search_urls()
    content_urls = []
    for url in urls:
        content_urls.append(scraper.get_url_content(url))
    return content_urls

@app.get("/global")
async def global_search(search: str = "Feminicidio"):
    scraperDiarioElSalvadorScrapper = DiarioElSalvadorScrapper(search)
    scraperDiarioColatinoScrapper = DiarioColatinoScrapper(search)
    scraperDiarioElMundoScrapper = DiarioElMundoScrapper(search)
    urlsDiarioElSalvadorScrapper = scraperDiarioElSalvadorScrapper.init_search_urls()
    content_urls = []
    for url in urlsDiarioElSalvadorScrapper:
        content_urls.append(scraperDiarioElSalvadorScrapper.get_url_content(url))
    print(len(content_urls))
    urlsDiarioColatinoScrapper = scraperDiarioColatinoScrapper.init_search_urls()
    #content_urls = []
    for url in urlsDiarioColatinoScrapper:
        content_urls.append(scraperDiarioColatinoScrapper.get_url_content(url))
    print(len(content_urls))
    urlsDiarioElMundoScrapper = scraperDiarioElMundoScrapper.init_search_urls()
    #content_urls = []
    for url in urlsDiarioElMundoScrapper:
        content_urls.append(scraperDiarioElMundoScrapper.get_url_content(url))
    print(len(content_urls))
    for i in range(len(content_urls)):
        content_urls[i]['tag'] = classify_new(content_urls[i]['text'])
    print(len(content_urls))
    return content_urls


def global_search_static(search: str = "Feminicidio"):
    scraperDiarioElSalvadorScrapper = DiarioElSalvadorScrapper(search)
    scraperDiarioColatinoScrapper = DiarioColatinoScrapper(search)
    scraperDiarioElMundoScrapper = DiarioElMundoScrapper(search)
    urlsDiarioElSalvadorScrapper = scraperDiarioElSalvadorScrapper.init_search_urls()
    content_urls = []
    for url in urlsDiarioElSalvadorScrapper:
        content_urls.append(scraperDiarioElSalvadorScrapper.get_url_content(url))
    print(len(content_urls))
    urlsDiarioColatinoScrapper = scraperDiarioColatinoScrapper.init_search_urls()
    #content_urls = []
    for url in urlsDiarioColatinoScrapper:
        content_urls.append(scraperDiarioColatinoScrapper.get_url_content(url))
    print(len(content_urls))
    urlsDiarioElMundoScrapper = scraperDiarioElMundoScrapper.init_search_urls()
    #content_urls = []
    for url in urlsDiarioElMundoScrapper:
        content_urls.append(scraperDiarioElMundoScrapper.get_url_content(url))
    print(len(content_urls))
    for i in range(len(content_urls)):
        content_urls[i]['tag'] = classify_new(content_urls[i]['text'])
    print(len(content_urls))
    return content_urls
@app.get("/model_gemma")
async def model_gemma(search: str = "Feminicidio"):
    return test_create_notice(global_search_static())

if __name__ == '__main__':
    print("TEST JOIN")
    #test_create_notice()
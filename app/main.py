# Importing necessary libraries for web application setup
import random

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importing specific scrapping services
from app.controllers.notices_controller import test_create_notice
from .services.diariocolatino import DiarioColatinoScrapper
from .services.elsalvador import ElSalvadorScraper
from .services.diarioelmundo import DiarioElMundoScrapper
from .services.diarioelsalvador import DiarioElSalvadorScrapper
from .env import env
from app.services.db_service import DatabaseService

# Initializing FastAPI application
app = FastAPI()

@app.on_event("startup")
def startup_event():
    DatabaseService.initialize()

# Setting up environment variables
env.set_env()

# Defining origins for CORS
origins = [
    "http://127.0.0.1:8000",
    "http://localhost:4200"
]

# Configuring CORS middleware
app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],
                   )


# Helper function to perform scraping
async def perform_scraping(scraper):
    urls = scraper.init_search_urls()
    content_urls = [scraper.get_url_content(url) for url in urls]
    return content_urls


# Route for proof of concept using ElSalvadorScraper
@app.get("/poc")
async def poc(search: str = ""):
    scraper = ElSalvadorScraper(search)
    return await perform_scraping(scraper)


# Route for Diario Colatino scraper
@app.get("/colatino")
async def colatino(search: str = ""):
    scraper = DiarioColatinoScrapper(search)
    return await perform_scraping(scraper)


# Route for Diario El Mundo scraper
@app.get("/diarioelmundo")
async def diarioelmundo(search: str = ""):
    scraper = DiarioElMundoScrapper(search)
    return await perform_scraping(scraper)


# Route for Diario El Salvador scraper
@app.get("/diarioelsalvador")
async def diarioelsalvador(search: str = "Feminicidio"):
    scraper = DiarioElSalvadorScrapper(search)
    return await perform_scraping(scraper)


# Route for global search across multiple sources
@app.get("/global")
async def global_search(search: str = "Feminicidio"):
    scrapers = [
        DiarioElSalvadorScrapper(search),
        DiarioColatinoScrapper(search),
        DiarioElMundoScrapper(search)
    ]
    content_urls = []
    for scraper in scrapers:
        scraper_urls = await perform_scraping(scraper)
        for url_content in scraper_urls:
            if url_content != None:
                url_content['tag'] = search
        content_urls.extend(scraper_urls)
    content_urls = [url for url in content_urls if url is not None]
    random.shuffle(content_urls)
    return content_urls


# Simplified static global search for demonstration purposes
def global_search_static(search: str = "Feminicidio"):
    scrapers = [
        DiarioElSalvadorScrapper(search),
        DiarioColatinoScrapper(search),
        DiarioElMundoScrapper(search)
    ]
    content_urls = []
    for scraper in scrapers:
        scraper_urls = [scraper.get_url_content(url) for url in scraper.init_search_urls()]
        for url_content in scraper_urls:
            url_content['tag'] = search
        content_urls.extend(scraper_urls)
    return content_urls


# Route to integrate with a hypothetical model for creating notices
@app.get("/model_gemma")
async def model_gemma(search: str = "Feminicidio"):
    return test_create_notice(global_search_static())


# Entry point when run as a main program
if __name__ == '__main__':
    print("TEST JOIN")

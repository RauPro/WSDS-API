# Importing necessary libraries for web application setup
import json
import random
import time
from datetime import datetime
from typing import Generator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse
from fastapi_pagination import Page, add_pagination, paginate
from datetime import date

from app.controllers import indicators_controller, news_controller
# Importing specific scrapping services
from app.controllers.notices_controller import test_create_notice
from app.services.db_service import DatabaseService
from app.services.driver.news_crud import create_new
from .services.diariocolatino import DiarioColatinoScrapper
from .services.elsalvador import ElSalvadorScraper
from .services.diarioelmundo import DiarioElMundoScrapper
from .services.diarioelsalvador import DiarioElSalvadorScrapper
from .env import env

# Initializing FastAPI application
app = FastAPI()

#INIT DATABASE
DatabaseService()

# Setting up environment variables
env.set_env()

# Defining origins for CORS
origins = [
    "http://127.0.0.1:8000",
    "http://localhost:4200"
]
add_pagination(app)
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
async def global_search(search: str = "Feminicidio") -> StreamingResponse:
    scrapers = [
        DiarioElSalvadorScrapper(search),
        DiarioColatinoScrapper(search),
        DiarioElMundoScrapper(search)
    ]
    scrapersName = [
        "Diario El Salvador",
        "Diario Colatino",
        "Diario El mundo"
    ]
    async def event_stream() -> Generator[str, None, None]:
        content_urls = []
        for i, scraper in enumerate(scrapers):
            scraper_urls = await perform_scraping(scraper)
            for url_content in scraper_urls:
                if url_content is not None:
                    url_content['tag'] = search
                    url_content['date'] = datetime.today().strftime('%Y-%m-%d')
                    saved = create_new(url_content)
                    yield f"data: {json.dumps({'saved': saved, 'scraper': scrapersName[i]})}\n\n"
                    yield f"data: {json.dumps({'status': 'starting', 'scraper': scrapersName[i]})}\n\n"
            content_urls.extend(scraper_urls)
            yield f"data: {json.dumps({'status': 'completed', 'scraper': scrapersName[i], 'results': [url for url in scraper_urls if url is not None]})}\n\n"

        random.shuffle(content_urls)
        content_urls = [url for url in content_urls if url is not None]
        yield f"data: {json.dumps({'status': 'final', 'results': content_urls})}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")



def global_search_static(search: str = "Feminicidio", date_param: str = None):
    if date_param is None:
        date_param = date.today().isoformat()
    scrapers = [
        DiarioElSalvadorScrapper(search),
        DiarioColatinoScrapper(search),
        DiarioElMundoScrapper(search)
    ]
    content_urls = []
    for scraper in scrapers:
        scraper_urls = [scraper.get_url_content(url) for url in scraper.init_search_urls()]
        for url_content in scraper_urls:
            if url_content is not None:
                url_content['tag'] = search
                url_content['date'] = date_param
        content_urls.extend(scraper_urls)
    return content_urls


mocked_list = [
        {
            "title": "*6El Salvador feminicido",
            "text": "\n\nCompartir\n\n Facebook\n Twitter\n Google +\n\n\n\n\n\nArtículos relacionados\n\n\n\n\n\n \n\n\nSesiona la nueva legislatura 2024-2027 \n1 mayo, 2024\n\n\n\n\n \n\n\nColombia rompimiento de relaciones diplomáticas con Israel\n1 mayo, 2024\n\n\n\n\n \n\n\nFranceses marchan en día de los trabajadores, reportan arrestos\n1 mayo, 2024\n\n\n\n\n\n",
            "source": "diariocolatino.com",
            "url": "https://www.diariocolatino.com/historia-universal-un-vistazo-al-pasado-desde-la-causa-popular/6el-salvador-feminicido/",
            "tag": "Feminicido",
            "date": "2024-05-05"
        },
    {
            "title": "Hombre enamorado de una mujer ficticia confiesa el asesinato de su compañera en Francia",
            "text": "Un joven adulto fue acusado el miércoles en Francia de haber asesinado a su compañera, con el fin de vivir una relación con una supuesta mujer de quien se había enamorado en internet y que resultó ser un estafador sentimental. El individuo nacido en 1994, empleado técnico de una alcaldía, reconoció haber planeado el crimen para poder «concretar» su relación virtual y afirmó que «lamentaba»  su acción, señaló en un comunicado la Fiscalía de Boulogne-sur-Mer (norte). La víctima, enfermera en una residencia de ancianos, nacida en 1995, fue hallada muerta el 28 de enero en el domicilio de la pareja, en la localidad de Beussent, con «heridas en el torso». Fue su propio compañero quien llamó a los gendarmes, asegurando que todo había ocurrido cuando se ausentó para ir a comprar pan, probablemente con fines de robo dada la desaparición de una alcancía. Pero la investigación descartó esa hipótesis y acusó al hombre, que «mantenía una relación afectiva en internet» con una persona de la cual ignoraba su verdadera identidad. Según el diario Le Parisien, que reveló el caso, esa pasión virtual se presentaba con el nombre de Béatrice Leroux, comerciante en la ciudad de Brest. La supuesta amante resultó ser un personaje ficticio creado por un estafador emocional, probablemente basado en Costa de Marfil, que había logrado que su enamorado le enviase 2.200 euros (unos 2.400 dólares). Numerosas bandas criminales que operan desde África occidental se especializan en estafas por internet, muchas veces creando fuertes vínculos afectivos con las personas contactadas. Francia registra en promedio un feminicidio cada tres días. El año pasado se contabilizaron 94.",
            "source": "diarioelsalvador.com",
            "url": "fake_url",
            "tag": "Feminicido",
            "date": "2024-05-05"
    }
    ]


@app.get("/model_gemma")
async def model_gemma(search: str = "Feminicidio", gemma_mode: str = "accurate"):
    #return test_create_notice(global_search_static())
    return StreamingResponse(test_create_notice(mocked_list, gemma_mode), media_type="text/event-stream")

app.include_router(indicators_controller.router)
app.include_router(news_controller.router)
add_pagination(app)

if __name__ == '__main__':
    print("TEST JOIN")

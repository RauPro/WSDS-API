# Importing necessary libraries for web application setup
import json
import random
import time
from datetime import datetime
from typing import Generator, Optional

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse
from fastapi_pagination import Page, add_pagination, paginate
from datetime import date

from app.controllers import indicators_controller, news_controller, sheets_controller, indicatorsEntry_controller, \
    global_setting_controller
#from app.controllers import sheets_controller
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

# INIT DATABASE
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
async def colatino(search: str = "", date: str = ""):
    scraper = DiarioColatinoScrapper(search)
    return await perform_scraping(scraper)


# Route for Diario El Mundo scraper
@app.get("/diarioelmundo")
async def diarioelmundo(search: str = "", date_start: str = "", date_end: str = ""):
    if date_start is None:
        date_start = date.today().isoformat()
        date_end= date.today().isoformat()
    
    scraper = DiarioElMundoScrapper(search, date_start, date_end)
    return await perform_scraping(scraper)


# Route for Diario El Salvador scraper
@app.get("/diarioelsalvador")
async def diarioelsalvador(search: str = "Feminicidio", date: str = ""):
    scraper = DiarioElSalvadorScrapper(search)
    return await perform_scraping(scraper)


# Route for global search across multiple sources
@app.get("/global")
async def global_search(search: str = "Feminicidio"
                        # , date: str = datetime.today()
                        ) -> StreamingResponse:
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


def global_search_static(search: str = "Feminicidio",  date_start: str = "", date_end: str = ""):
    if date_start is None:
        date_start = date.today().isoformat()
        date_end= date.today().isoformat()

    scrapers = [
        DiarioElSalvadorScrapper(search, date_start, date_end),
        DiarioColatinoScrapper(search, date_start, date_end),
        DiarioElMundoScrapper(search, date_start, date_end)
    ]
    content_urls = []
    for scraper in scrapers:
        scraper_urls = [scraper.get_url_content(url) for url in scraper.init_search_urls()]
        for url_content in scraper_urls:
            if url_content is not None:
                url_content['tag'] = search
                #url_content['date'] = date_start
        content_urls.extend(scraper_urls)
    return content_urls


mocked_list = [

               {'title': 'Suspenden hasta nuevo aviso juicio por feminicidio de Yancy Urbina',
                'text': '\n        El Juzgado Especializado de Sentencia para una Vida Libre de Violencia y Discriminación de San Salvador suspendió hasta nuevo aviso el juicio contra Peter Wachowski, quien es enjuiciado del feminicidio de su exesposa, Yancy Urbina, la exdiputado del FMLN. \rSegún fuentes judiciales, el juicio entró en receso el pasado viernes 12 abril debido a que la jueza solicitó una prueba "para mejor proveer". \rEl juicio se reanudará una vez la prueba sea incorporada, y será hasta ese momento procesal que la jueza notificará a las partes la nueva fecha para reanudar el juicio. \rLa vista pública continuará con la presentación de los alegatos finales, donde la Fiscalía General de la República solicitará la sentencia condenatoria y la defensa solicitará sus argumentos para obtener la sentencia absolutoria. \rSon alrededor de 26 testigos tanto de cargo como de descargo los que han declarado durante la vista pública, entre ellos, peritos e investigadores. \rLa defensa sostiene que espera obtener una sentencia absolutoria, debido a que la Fiscalía no cuenta con los elementos de prueba para sostener la acusación contra Wachowski. \rLa exdiputada Yanci Urbina murió el pasado 29 de mayo del 2022, en su casa de habitación, en Antiguo Cuscatlán, departamento de La Libertad, aparentemente en un accidente, luego de una caída que posteriormente le habría provocado un paro cardíaco. \rLa Fiscalía sostiene que la muerte de la exdiputada se trató de un acto de violencia de género y no de un accidente por una caída. \rEn el transcurso del proceso, la Fiscalía ha manifestado que el cuerpo de Urbina tenía múltiples moretones, un golpe con objeto contundente y el tabique nasal quebrado. \rEl juicio inició el 3 de abril, inicialmente estaba programado para hacerse en dos días, pero debido a la cantidad de testigos se alargó.\n                \n\n\n\n',
                'source': 'diario.elmundo.sv',
                'url': 'https://diario.elmundo.sv/nacionales/suspenden-hasta-nuevo-aviso-juicio-por-feminicidio-de-yancy-urbina',
                'sheet_id': 'https://diario.elmundo.sv/nacionales/suspenden-hasta-nuevo-aviso-juicio-por-feminicidio-de-yancy-urbina',
                'tag': 'Feminicidio', 'date': '2024-05-05'},
               {'title': 'Programan juicio contra acusado del feminicidio de Fernanda Nájera',
                'text': '\n        El Juzgado Especializado de Sentencia para una Vida Libre de Violencia y Discriminación para las Mujeres de San Salvador ha programado para el próximo 22 de abril el juicio en contra de Michael Alejandro Castillo Murga, acusado del feminicidio agravado de Melvi Fernanda Nájera Quezada y el homicidio tentado de su hijo. \rEn un principio el caso era conocido por un juzgado especializado de Santa Ana, sin embargo, por una resolución de una Cámara de lo Penal se trasladó el caso hacia San Salvador. \rEs la segunda programación del caso, ya que el pasado 14 de febrero se suspendió, debido a la incomparecencia de la Fiscalía General de la República, ya que eran parte del escrutinio final de las elecciones presidenciales y de diputados 2024. \rSegún la acusación de la Fiscalía, Fernanda Nájera de 23 años, fue encontrada muerta con múltiples lesiones ocasionadas con arma blanca, el 1 de febrero, en el kilómetro 99 de la carretera que de Ahuachapán conduce a Sonsonate, en la jurisdicción del cantón El Molino, del municipio de Concepción de Ataco. \rEl hijo de la víctima, de un año y siete meses, fue encontrado el 4 de febrero en un cafetal en estado de abandono y deshidratado. \rSegún el relato de la madre de Nájera, Michael Alejandro Castillo Murgas llegó a su casa el 31 de enero de 2019 a traer a su hija y a su nieto, supuestamente se dirigían a una diligencia para otorgarle su apellido al menor, sin embargo, nunca regresaron. \rLa Fiscalía General de la República acusó inicialmente a cinco personas por este caso, a Castillo Murgas por el delito de feminicidio agravado y homicidio tentado en perjuicio del hijo de la víctima. \rCastillo Murgas fue declarado rebelde y sobre él pesa una orden de captura internacional. El proceso lo enfrenta en calidad de reo ausente. Sobre el resto de procesados se desconoce en qué etapa avanzan el proceso penal.\n                \n\n\n\n',
                'source': 'diario.elmundo.sv',
                'url': 'https://diario.elmundo.sv/nacionales/programan-juicio-contra-acusado-del-feminicidio-de-fernanda-najera',
                'sheet_id': 'https://diario.elmundo.sv/nacionales/programan-juicio-contra-acusado-del-feminicidio-de-fernanda-najera',
                'tag': 'Feminicidio', 'date': '2024-05-05'}]


@app.get("/model_gemma")
async def model_gemma(search: str = "Feminicidio", gemma_mode: str = "accurate",
                      date_start: str = "",
                      date_end: str = ""
                      ):
    news = global_search_static(search, date_start, date_end)
    return StreamingResponse(test_create_notice(news, gemma_mode), media_type="text/event-stream")


app.include_router(indicators_controller.router)
app.include_router(news_controller.router)
app.include_router(sheets_controller.router)
app.include_router(global_setting_controller.router)
app.include_router(indicatorsEntry_controller.router)

add_pagination(app)

if __name__ == '__main__':
    print("TEST JOIN")

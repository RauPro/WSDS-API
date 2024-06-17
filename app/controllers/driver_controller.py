import json
from datetime import date, datetime
import random
from typing import Generator
from fastapi import HTTPException, APIRouter
from starlette.responses import StreamingResponse
from app.controllers import create_news_gemma
from app.services import ElSalvadorScraper, DiarioColatinoScrapper, DiarioElSalvadorScrapper, DiarioElMundoScrapper
from app.services.driver.news_crud import create_new

router = APIRouter()

async def perform_scraping(scraper) -> list:
    """
    Perform web scraping using the provided scraper.

    Args:
        scraper: The web scraper instance.

    Returns:
        list: A list of scraped content URLs.
    """
    urls = scraper.init_search_urls()
    content_urls = [scraper.get_url_content(url) for url in urls]
    return content_urls

@router.get("/colatino")
async def colatino(search: str = "", date: str = "") -> list:
    """
    Route for Diario Colatino scraper.

    Args:
        search (str): The search term (default: "").
        date (str): The date (default: "").

    Returns:
        list: A list of scraped content URLs.
    """
    scraper = DiarioColatinoScrapper(search)
    return await perform_scraping(scraper)

@router.get("/diarioelmundo")
async def diarioelmundo(search: str = "", date_start: str = "", date_end: str = "") -> list:
    """
    Route for Diario El Mundo scraper.

    Args:
        search (str): The search term (default: "").
        date_start (str): The start date (default: "").
        date_end (str): The end date (default: "").

    Returns:
        list: A list of scraped content URLs.
    """
    if date_start is None:
        date_start = date.today().isoformat()
        date_end = date.today().isoformat()

    scraper = DiarioElMundoScrapper(search, date_start, date_end)
    return await perform_scraping(scraper)

@router.get("/diarioelsalvador")
async def diarioelsalvador(search: str = "Feminicidio", date: str = "") -> list:
    """
    Route for Diario El Salvador scraper.

    Args:
        search (str): The search term (default: "Feminicidio").
        date (str): The date (default: "").

    Returns:
        list: A list of scraped content URLs.
    """
    scraper = DiarioElSalvadorScrapper(search)
    return await perform_scraping(scraper)

@router.get("/global")
async def global_search(search: str = "Feminicidio") -> StreamingResponse:
    """
    Route for global search across multiple sources.

    Args:
        search (str): The search term (default: "Feminicidio").

    Returns:
        StreamingResponse: A streaming response containing the scraped content URLs.
    """
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

def global_search_static(search: str = "Feminicidio", date_start: str = "", date_end: str = "") -> list:
    """
    Perform a static global search across multiple sources.

    Args:
        search (str): The search term (default: "Feminicidio").
        date_start (str): The start date (default: "").
        date_end (str): The end date (default: "").

    Returns:
        list: A list of scraped content URLs.
    """
    if date_start is None:
        date_start = date.today().isoformat()
        date_end = date.today().isoformat()

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
        content_urls.extend(scraper_urls)
    return content_urls

@router.get("/model_gemma")
async def model_gemma(search: str = "Feminicidio", gemma_mode: str = "accurate", date_start: str = "", date_end: str = "") -> StreamingResponse:
    """
    Route for applying the Gemma model to scraped news.

    Args:
        search (str): The search term (default: "Feminicidio").
        gemma_mode (str): The Gemma mode (default: "accurate").
        date_start (str): The start date (default: "").
        date_end (str): The end date (default: "").

    Returns:
        StreamingResponse: A streaming response containing the processed news data.
    """
    news = global_search_static(search, date_start, date_end)
    return StreamingResponse(create_news_gemma(news, gemma_mode), media_type="text/event-stream")

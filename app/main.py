from fastapi import FastAPI
from services.elsalvador import ElSalvadorScraper
app = FastAPI()

@app.get("/poc")
async def poc(search: str = ""):
    scraper = ElSalvadorScraper(search)
    urls = scraper.init_search_urls()
    content_urls = []
    for url in   urls:
        content_urls.append(scraper.get_url_content(url))
    return content_urls
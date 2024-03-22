from ..models.models import *
from ..prompts.main_prompt import *
import requests

from ..services import DiarioElMundoScrapper


# router = APIRouter()

def create_notice(r: NoticeRequest):
    query = requests.post(url="http://localhost:3000/ollama/api/generate", json={"prompt": r.prompt, "model": r.model, "stream": False},
                         headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjBmNjg5MTM1LTI1OGUtNDAxNi04NDZkLTNmYjZkNjAyNmNlNyJ9.-jFD5ZMqhbSe6Eb_lmgNVoWLyBLr7b36wBgJIDJ3kGU"})
    return query.json()



def poc(search: str = ""):
    scraper = DiarioElMundoScrapper(search)
    urls = scraper.init_search_urls()
    content_urls = []
    for url in urls:
        content_urls.append(scraper.get_url_content(url))
    return content_urls

def test_create_notice():

    list_news = poc("feminicidio")
    for new in list_news:
        new_ = NoticeRequest(
            model="gemma:7b",
            prompt=generate_prompt(new.get("title"), new.get("text")),
            stream=False,
        )
        new["sheet"] = create_notice(new_)
    #
    print(list_news)
    print("Done")
    exit(0)

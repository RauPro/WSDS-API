from ..models.models import *
from ..prompts.main_prompt import *
import requests
import os
from ..services import DiarioElMundoScrapper


# router = APIRouter()

def create_notice(r: NoticeRequest):
    token = os.environ.get("OLLAMA-Token")
    query = requests.post(url="http://localhost:3000/ollama/api/generate", json={"prompt": r.prompt, "model": r.model, "stream": False},
                         headers={"Authorization": f"Bearer {token}"})
    return query.json()


def test_create_notice(list_news):
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
    return list_news

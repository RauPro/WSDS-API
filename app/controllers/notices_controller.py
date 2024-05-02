from ..models.models import *
from ..prompts.main_prompt import *
import requests
import os
from ..services import DiarioElMundoScrapper


# router = APIRouter()

def create_notice(r: NoticeRequest):
    token = os.environ.get("OLLAMA-Token")
    query = requests.post(url="http://localhost:3000/ollama/api/generate",
                          json={"prompt": r.prompt, "model": r.model, "stream": False},
                          headers={"Authorization": f"Bearer {token}"})
    return query.json()


def test_create_notice(list_news: [New]):
    ans = []
    for new in list_news:
        new_ = generate_answer(new)
        ans.append(new_)
    print(ans)
    print("Done")
    return ans


def generate_prompt(title, description, field):
    base_prompt = f"""
    Noticia:
    Título: {title}
    Descripción: {description}

    Por favor, analiza y proporciona la siguiente información sobre la noticia:
    """
    full_prompt = f"{base_prompt}{field}"
    return full_prompt


def generate_answer(new):
    prompts = get_prompts()
    ans = []
    for p in prompts:
        new_generated = {
            "indicator_name": p.get("indicator_name")
        }
        new_ = NoticeRequest(
            model="gemma:7b",
            prompt=generate_prompt(new.get("title"), new.get("text"), p.get("prompt")),
            stream=False,
        )
        gemma_ans = create_notice(new_)
        new_generated["response"] = gemma_ans["response"]
        ans.append(new_generated)
        print(new_)
        print()
    return ans

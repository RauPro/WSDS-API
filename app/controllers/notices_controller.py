import json
from copy import deepcopy

from ..models.enums import GemmaMode, PrioritySheet
from ..models.models import *
from ..prompts.main_prompt import *
import requests
import os
from ..services import DiarioElMundoScrapper
from ..services.driver.news_crud import create_new
from ..services.driver.sheets_crud import create_sheet, create_sheet_priority, get_sheet_by_id
import json
from bson import ObjectId  # Assuming you are using PyMongo

class JSONEncoder(json.JSONEncoder):
    """ Extend json-encoder class to handle ObjectId type """
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)

# router = APIRouter()

def create_notice(r: NoticeRequest):
    token = os.environ.get("OLLAMA-Token")
    query = requests.post(url="http://localhost:3000/ollama/api/generate",
                          json={"prompt": r.prompt, "model": r.model, "stream": False},
                          headers={"Authorization": f"Bearer {token}"})
    return query.json()


async def test_create_notice(list_news: [New], gemma_mode: str):
    yield f"data: True\n\n"
    if gemma_mode == GemmaMode.ACCURATE.value:
        ans =[]
        for new in list_news:
            existing_sheet = get_sheet_by_id(new["url"])
            if existing_sheet is not None and existing_sheet["priority"] == 3:
                continue
            new_ = generate_answer(new)
            new_to_save = deepcopy(new)
            new_to_save["sheet_id"] = new.get("url")
            debugger = create_new(new_to_save)
            #print(debugger)
            new["sheet"] = {}
            new["sheet_id"] = new.get("url")
            new["sheet"]["indicators"] = new_
            new["sheet"]["priority"] = PrioritySheet.ACCURATE.value
            new["sheet"]["id"] = new.get("url")
            ans.append(new)
            try:
                json_data = json.dumps(ans, cls=JSONEncoder)
                yield f"data: {json_data}\n\n"
            except Exception as e:
                # Log the exception or handle it accordingly
                print(f"Failed to create sheet: {e}")
                raise
            try:
                debugger = create_sheet_priority(new["sheet"])
                print(debugger)
            except Exception as e:
                # Log the exception or handle it accordingly
                print(f"Failed to create sheet: {e}")
                raise
        #print(ans)
        print("Done")
        #return ans
    elif gemma_mode == GemmaMode.STANDARD.value:
        ans = []
        for new in list_news:
            existing_sheet = get_sheet_by_id(new["url"])

            new_to_save = deepcopy(new)
            new_to_save["sheet_id"] = new.get("url")
            debugger = create_new(new_to_save)
            #print(debugger)
            if existing_sheet is not None and existing_sheet["priority"] == 4:
                new["sheet"] = existing_sheet
                ans.append(new)
                json_data = json.dumps(ans, cls=JSONEncoder)
                yield f"data: {json_data}\n\n"
                continue
            new = generate_standard_answer(new)
            new["sheet_id"] = new.get("url")
            new["sheet"]["priority"] = PrioritySheet.STANDARD.value
            ans.append(new)
            try:
                json_data = json.dumps(ans, cls=JSONEncoder)
                yield f"data: {json_data}\n\n"
            except Exception as e:
                # Log the exception or handle it accordingly
                print(f"Failed to create sheet: {e}")
                raise
            try:
                debugger = create_sheet_priority(new["sheet"])
                print(debugger)
            except Exception as e:
                # Log the exception or handle it accordingly
                print(f"Failed to create sheet: {e}")
                raise



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
        #print(new_)
        #print()
    return ans


def classification_standard_model(raw_sheet, url):
    data = {
        "Clasificación": "N/A",
        "Título": "N/A",
        "Resumen": "N/A",
        "Lugar de los Hechos": "N/A",
        "Fuentes": "N/A",
        "Temas": "N/A",
        "Hechos Violatorios": "N/A",
        "Hipótesis de Hechos": "N/A",
        "Población Vulnerable": "N/A",
        "Tipo de Arma": "N/A",
        "Víctimas": "N/A",
        "Victimario o Presunto Agresor": "N/A"
    }

    pattern = {
        "Clasificación": r"Clasificación:\s*(.*)\s*\n",
        "Título": r"Título:\s*(.*)\s*\n",
        "Resumen": r"Resumen:\s*(.*)\s*\n",
        "Lugar de los Hechos": r"Lugar de los Hechos:\s*(.*)\s*\n",
        "Fuentes": r"Fuentes:\s*(.*)\s*\n",
        "Temas": r"Temas:\s*(.*)\s*\n",
        "Hechos Violatorios": r"Hechos Violatorios:\s*(.*)\s*\n",
        "Hipótesis de Hechos": r"Hipótesis de Hechos:\s*(.*)\s*\n",
        "Población Vulnerable": r"Población Vulnerable:\s*(.*)\s*\n",
        "Tipo de Arma": r"Tipo de Arma:\s*(.*)\s*\n",
        "Víctimas": r"Víctimas:\s*(.*)\s*\n",
        "Victimario o Presunto Agresor": r"Victimario o Presunto Agresor:\s*(.*)\s*\n"
    }

    for field, val in pattern.items():
        match = re.search(val, raw_sheet, re.MULTILINE)
        if match:
            data[field] = match.group(1).strip()

    ans = []
    for key, value in data.items():
        response ={
            "indicator_name": key,
            "response": value
        }
        ans.append(response)
    response = {
        "indicators": ans,
        "id": url
    }
    return response

def generate_standard_answer(new):
    new_ = NoticeRequest(
        model="gemma:7b",
        prompt=generate_prompt_standard(new.get("title"), new.get("text")),
        stream=False,
    )
    get_raw_ans = create_notice(new_)
    new["sheet"] = classification_standard_model(get_raw_ans.get("response"), new.get("url"))
    return new


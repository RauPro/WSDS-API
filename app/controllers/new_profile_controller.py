import re
from copy import deepcopy
import json
import os
from copy import deepcopy

import requests
from bson import ObjectId

from ..models.enums import GemmaMode, PrioritySheet
from ..models.models import *
from ..prompts.main_prompt import *
from ..services.driver.news_crud import create_new
from ..services.driver.prompts_crud import get_prompts
from ..services.driver.sheets_crud import create_sheet_priority, get_sheet_by_id


class JSONEncoder(json.JSONEncoder):
    """
    Extend json-encoder class to handle ObjectId type.
    """

    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


def create_notice(r: NewProfileRequest) -> dict:
    """
    Create a notice by sending a request to the Ollama API.

    Args:
        r (NewProfileRequest): The request data for creating the notice.

    Returns:
        dict: The response from the Ollama API.
    """
    token = os.environ.get("OLLAMA-Token")
    base_url = 'http://host.docker.internal'
    query = requests.post(url="http://localhost:3000/ollama/api/generate",
                          json={"prompt": r.prompt, "model": r.model, "stream": False},
                          headers={"Authorization": f"Bearer {token}"})
    return query.json()


async def create_news_gemma(list_news: [New], gemma_mode: str) -> None:
    """
    Create notices based on the provided list of news and Gemma mode.

    Args:
        list_news ([New]): The list of news items to create notices for.
        gemma_mode (str): The Gemma mode to use for creating notices.

    Yields:
        str: The JSON data of the created notices.
    """
    yield f"data: True\n\n"
    if gemma_mode == GemmaMode.ACCURATE.value:
        ans = []
        for new in list_news:
            new_to_save = deepcopy(new)
            new_to_save["sheet_id"] = new.get("url")
            debugger = create_new(new_to_save)
            existing_sheet = get_sheet_by_id(new["url"])
            if existing_sheet is not None and existing_sheet["priority"] <= PrioritySheet.ACCURATE.value:
                new["sheet"] = existing_sheet
                ans.append(new)
                json_data = json.dumps(ans, cls=JSONEncoder)
                yield f"data: {json_data}\n\n"
                continue
            new_ = generate_answer(new)
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
                print(f"Failed to create sheet: {e}")
                raise
            try:
                debugger = create_sheet_priority(new["sheet"])
                print(debugger)
            except Exception as e:
                print(f"Failed to create sheet: {e}")
                raise
        print("Done")
    elif gemma_mode == GemmaMode.STANDARD.value:
        ans = []
        for new in list_news:
            existing_sheet = get_sheet_by_id(new["url"])
            new_to_save = deepcopy(new)
            new_to_save["sheet_id"] = new.get("url")
            debugger = create_new(new_to_save)
            if existing_sheet is not None and existing_sheet["priority"] <= PrioritySheet.STANDARD.value:
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
                print(f"Failed to create sheet: {e}")
                raise
            try:
                debugger = create_sheet_priority(new["sheet"])
                print(debugger)
            except Exception as e:
                print(f"Failed to create sheet: {e}")
                raise


def generate_prompt(title: str, description: str, field: str) -> str:
    """
    Generate a prompt for analyzing a news article.

    Args:
        title (str): The title of the news article.
        description (str): The description of the news article.
        field (str): The specific field to analyze.

    Returns:
        str: The generated prompt.
    """
    base_prompt = f"""
    Noticia:
    Título: {title}
    Descripción: {description}

    Por favor, analiza y proporciona la siguiente información sobre la noticia:
    """
    full_prompt = f"{base_prompt}{field}"
    return full_prompt


def generate_answer(new: dict) -> list:
    """
    Generate answers for a news article based on predefined prompts.

    Args:
        new (dict): The news article data.

    Returns:
        list: The generated answers for each prompt.
    """
    prompts = get_prompts()
    ans = []
    for p in prompts:
        new_generated = {
            "indicator_name": p.get("indicator_name")
        }
        new_ = NewProfileRequest(
            model="gemma:7b",
            prompt=generate_prompt(new.get("title"), new.get("text"), p.get("prompt")),
            stream=False,
        )
        gemma_ans = create_notice(new_)
        new_generated["response"] = gemma_ans["response"]
        ans.append(new_generated)
    return ans


def classification_standard_model(raw_sheet: str, url: str) -> dict:
    """
    Classify a news article using a standard model.

    Args:
        raw_sheet (str): The raw text of the news article.
        url (str): The URL of the news article.

    Returns:
        dict: The classified data of the news article.
    """
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
        response = {
            "indicator_name": key,
            "response": value
        }
        ans.append(response)
    response = {
        "indicators": ans,
        "id": url
    }
    return response


def generate_standard_answer(new: dict) -> dict:
    """
    Generate a standard answer for a news article.

    Args:
        new (dict): The news article data.

    Returns:
        dict: The news article data with the generated standard answer.
    """
    new_ = NewProfileRequest(
        model="gemma:7b",
        prompt=generate_prompt_standard(new.get("title"), new.get("text")),
        stream=False,
    )
    get_raw_ans = create_notice(new_)
    new["sheet"] = classification_standard_model(get_raw_ans.get("response"), new.get("url"))
    return new

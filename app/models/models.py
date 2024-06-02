from typing import List, Optional

from pydantic import BaseModel


class NewProfileRequest(BaseModel):
    """
    Represents a request to create a new profile.

    Attributes:
        model (str): The model to use for the profile.
        prompt (str): The prompt to use for the profile.
        stream (Optional[bool], optional): Whether to stream the response. Defaults to False.
    """
    model: str
    prompt: str
    stream: Optional[bool] = False


class NewProfileResponse(BaseModel):
    """
    Represents the response from creating a new profile.

    Attributes:
        model (str): The model used for the profile.
        created_at (str): The timestamp when the profile was created.
        response (str): The response generated for the profile.
        done (bool): Indicates if the profile creation is complete.
        context (List[int]): The context used for the profile.
        total_duration (int): The total duration of the profile creation process.
        load_duration (int): The duration of loading the model.
        prompt_eval_duration (int): The duration of evaluating the prompt.
        eval_count (int): The number of evaluations performed.
        eval_duration (int): The total duration of evaluations.
    """
    model: str
    created_at: str
    response: str
    done: bool
    context: List[int]
    total_duration: int
    load_duration: int
    prompt_eval_duration: int
    eval_count: int
    eval_duration: int


class Prompt(BaseModel):
    """
    Represents a prompt.

    Attributes:
        indicator_name (str): The name of the indicator associated with the prompt.
        prompt (str): The prompt text.
        id (str): The unique identifier of the prompt.
    """
    indicator_name: str
    prompt: str
    id: str


class PromptEntry(BaseModel):
    """
    Represents an entry containing a list of prompts.

    Attributes:
        indicators (List[Prompt]): The list of prompts.
        name (str): The name of the prompt entry.
        id (str): The unique identifier of the prompt entry.
    """
    indicators: List[Prompt]
    name: str
    id: str


class Sheet(BaseModel):
    """
    Represents a sheet.

    Attributes:
        indicator_name (str): The name of the indicator associated with the sheet.
        response (str): The response for the sheet.
    """
    indicator_name: str
    response: str


class SheetEntry(BaseModel):
    """
    Represents an entry containing a list of sheets.

    Attributes:
        indicators (List[Sheet]): The list of sheets.
        priority (int): The priority of the sheet entry.
        id (str): The unique identifier of the sheet entry.
    """
    indicators: List[Sheet]
    priority: int
    id: str


class New(BaseModel):
    """
    Represents a new item.

    Attributes:
        title (str): The title of the item.
        text (str): The text content of the item.
        source (str): The source of the item.
        url (str): The URL associated with the item.
        tag (str): The tag assigned to the item.
        sheet_id (str): The identifier of the sheet associated with the item.
        date (str): The date of the item.
    """
    title: str
    text: str
    source: str
    url: str
    tag: str
    sheet_id: str
    date: str

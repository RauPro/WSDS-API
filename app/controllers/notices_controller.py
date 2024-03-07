from fastapi import APIRouter
from models.models import NoticeRequest, NoticeResponse


router = APIRouter()

@router.post("/notices", response_model=NoticeResponse)
async def create_notice(request: NoticeRequest):

    return NoticeResponse(
        model=request.model,
        created_at="2024-02-27T23:46:36.068271311Z",
        response="*Clasificación:* Homicidio\n\n*Título:* Envían a prisión a hombre acusado de asesinar a su \"amigo\" en Chalatenango\n\n*Resumen:\nUn hombre se encuentra en prisión acusado de haber matado a su \"amigo\" en San Miguel de Mercedes, en Chalatenango. La víctima se quedó dormida en la acera y fue atacada con un hacha y un corvo.\n\nLugar de los hechos:* San Miguel de Mercedes, Chalatenango\n\n*Fuentes:* No se especifica en la noticia.\n\n*Temas:* Homicidio, asesinato, víctima, agresor, alcohol, estado de embriaguez.\n\n*Hechos violatorios:* No se especifica en la noticia.\n\n*Hipótesis de hechos:* No se especifica en la noticia.\n\n*Población vulnerable:* No se especifica en la noticia.\n\n*Tipo de arma:* Hacha, corvo.\n\n*Víctimas:* Una persona.\n\n*Victimario o presunto agresor:* Mario Gregorio Hernández.",
        done=True,
        context=[106, 1645],
        total_duration=37812502352,
        load_duration=206006,
        prompt_eval_duration=196774000,
        eval_count=212,
        eval_duration=37615051000
    )
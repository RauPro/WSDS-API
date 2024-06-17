import re

saved = {
    "indicators": [
        {
            "indicator_name": "Clasificacion",
            "response": "Actualización2: La situación ha cambiado."
        },
        {
            "indicator_name": "Titulo",
            "response": "Actualización del título previo."
        },
        {
            "indicator_name": "Resumen",
            "response": "Nuevo resumen actualizado del evento."
        },
        {
            "indicator_name": "Ubicacion del Suceso",
            "response": "Nueva ubicación actualizada del suceso."
        },
        {
            "indicator_name": "Fuentes",
            "response": "Nuevas fuentes citadas en la actualización."
        },
        {
            "indicator_name": "Temas",
            "response": "Temas actualizados tratados en la noticia."
        },
        {
            "indicator_name": "Hechos Violativos",
            "response": "Información actualizada sobre violaciones legales."
        },
        {
            "indicator_name": "Hipotesis de los Hechos",
            "response": "Teoría actualizada de los hechos."
        },
        {
            "indicator_name": "Poblacion Vulnerable",
            "response": "Datos actualizados sobre población vulnerable."
        },
        {
            "indicator_name": "Tipo de Arma",
            "response": "Actualización sobre el tipo de arma utilizada."
        },
        {
            "indicator_name": "Victimas",
            "response": "Información actualizada sobre las víctimas."
        },
        {
            "indicator_name": "Agresor o Sospechoso",
            "response": "Información actualizada sobre el agresor o sospechoso."
        }
    ],
    "priority": 2,
    "id": "url_test"
}

filters = {
    "indicators": [
        {
            "indicator_name": "Clasificacion",
            "response": "modify"
        },
        {
            "indicator_name": "Titulo",
            "response": "Actualización del título previo."
        },
        {
            "indicator_name": "Resumen",
            "response": "Nuevo resumen actualizado del evento."
        },
        {
            "indicator_name": "Ubicacion del Suceso",
            "response": "Nueva ubicación actualizada del suceso."
        },
        {
            "indicator_name": "Fuentes",
            "response": "Nuevas fuentes citadas en la actualización."
        },
        {
            "indicator_name": "Temas",
            "response": "Temas actualizados tratados en la noticia."
        },
        {
            "indicator_name": "Hechos Violativos",
            "response": "Información actualizada sobre violaciones legales."
        },
        {
            "indicator_name": "Hipotesis de los Hechos",
            "response": "Teoría actualizada de los hechos."
        },
        {
            "indicator_name": "Poblacion Vulnerable",
            "response": "Datos actualizados sobre población vulnerable."
        },
        {
            "indicator_name": "Tipo de Arma",
            "response": "Actualización sobre el tipo de arma utilizada."
        },
        {
            "indicator_name": "Victimas",
            "response": "Información actualizada sobre las víctimas."
        },
        {
            "indicator_name": "Agresor o Sospechoso",
            "response": "Información actualizada sobre el agresor o sospechoso."
        },
        {
            "indicator_name": "Agresor sexo",
            "response": "Información actualizada sobre el agresor o sospechoso."
        },
        {
            "indicator_name": "sexo Sospechoso",
            "response": "Información actualizada sobre el agresor o sospechoso."
        }
    ],
    "priority": 2,
    "id": "url_test"
}

ans = 0
for filter in filters["indicators"]:
    indicator_to_find = filter["indicator_name"]
    response_to_find = filter["response"]

    for it in saved["indicators"]:
        if indicator_to_find == it["indicator_name"] and response_to_find in it["response"]:
            ans += 1

print(ans)

date_regex = r"^.{4}-.{2}-.{2}$"
print(re.match(date_regex, "2024-05-04") and False)

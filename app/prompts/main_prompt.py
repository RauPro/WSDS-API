def generate_prompt(title, description, field):
    base_prompt = f"""
    Noticia:
    Título: {title}
    Descripción: {description}

    Por favor, analiza y proporciona la siguiente información sobre la noticia:
    """

    field_prompts = {
        "classification": "Clasifica si la noticia describe un homicidio.",
        "title": "Extrae el título de la noticia.",
        "summary": "Proporciona un breve resumen de la noticia.",
        "location_of_incident": "Dónde ocurrió el suceso.",
        "sources": "Cita las fuentes de información.",
        "themes": "Los temas principales tratados.",
        "violative_facts": "Detalles específicos sobre la violación a la ley.",
        "hypothesis_of_facts": "Cualquier teoría o suposición presentada.",
        "vulnerable_population": "Grupos en riesgo mencionados.",
        "type_of_weapon": "Especifica el tipo de arma, si se menciona.",
        "victims": "Identifica a las víctimas, si es posible.",
        "perpetrator_or_suspected_aggressor": "Nombre del agresor, si se menciona."
    }

    specific_prompt = field_prompts.get(field, "Por favor, verifica la noticia y proporciona información relevante.")
    full_prompt = f"{base_prompt}{specific_prompt}"

    return full_prompt


def create_notice(title, description, fields):

    for field in fields:
        prompt = generate_prompt(title, description, field)
        print(prompt)


create_notice("Local man arrested", "A local man was arrested yesterday on suspicion of murder.",
              ["classification", "summary", "location_of_incident"])

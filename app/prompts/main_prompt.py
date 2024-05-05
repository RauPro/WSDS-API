import re

from app.services.driver.prompts_crud import get_prompts
def generate_prompt_standard(title, description):
    prompt = f"""
    Noticia:
Título:  {title}
Descripción:  {description}


Analiza la noticia proporcionada siguiendo estos pasos y criterios para determinar si clasifica como un caso de homicidio, y luego extrae la información específica solicitada:

1. Clasificación de la Noticia:

Primero, identifica si la noticia describe un homicidio basándote en el análisis del título y la descripción mediante la detección de palabras clave organizadas en orden de prioridad. Utiliza las siguientes listas de palabras clave para evaluar el contenido:

Orden de Prioridad 1: Homicidio, feminicidio, osamenta, fosa clandestina, grupo de exterminio.
Orden de Prioridad 2: Homicida, feminicida.
Orden de Prioridad 3: Crimen, sin vida, cuerpo sin vida, cuerpo en estado de descomposición, cadáver en estado de descomposición, estado de putrefacción, semienterrado, cadáver, cuerpo.
Orden de Prioridad 4: Arma blanca, arma de fuego, machete, cuchillo, arma contundente, corvo.
Orden de Prioridad 5: Acto de intolerancia, alcohol, droga, privada de libertad, defensa propia, rencilla personal, legítima defensa, violencia, sangre, ataque de esquizofrenia, ataque.
Segundo, si identificas alguna de estas palabras clave, especialmente aquellas de prioridad más alta, determina que la noticia describe un homicidio.

2. Extracción de Información:

Si la noticia es clasificada como un homicidio, procede a extraer y organizar la siguiente información específica, si está disponible en el contenido:

Clasificación: Homicidio
Título: Extrae el título de la noticia.
Resumen: Proporciona un breve resumen de la noticia.
Lugar de los Hechos: Dónde ocurrió el suceso.
Fuentes: Cita las fuentes de información.
Temas: Los temas principales tratados.
Hechos Violatorios: Detalles específicos sobre la violación a la ley.
Hipótesis de Hechos: Cualquier teoría o suposición presentada.
Población Vulnerable: Grupos en riesgo mencionados.
Tipo de Arma: Especifica el tipo de arma, si se menciona.
Víctimas: Identifica a las víctimas, si es posible.
Victimario o Presunto Agresor: Nombre del agresor, si se menciona.
En cualquier caso que la información no esté disponible o no se especifique en la noticia, indica "N/A" para ese campo.

    """
    return prompt





if __name__ == "__main__":
    new_example = """Clasificación de la Noticia:
La noticia describe un homicidio, según el análisis del título y la descripción. La presencia de las palabras clave como "homicidio", "asesinato" y "lesión" indica que la noticia se refiere a un caso de homicidio.
Extracción de Información:
Clasificación: Homicidio
Título: Capturan a hombre que lesionó con corvo a una joven en Cabañas
Resumen: Un hombre fue capturado por la policía por el delito de intento de homicidio en perjuicio de una adolescente.
Lugar de los Hechos: Cabañas
Fuentes: N/A
Temas: Violencia contra la mujer, lesiones graves


Hechos Violatorios: El sospechoso lesionó a la víctima con un corvo.


Hipótesis de Hechos: N/A


Población Vulnerable: N/A


Tipo de Arma: Corvo


Víctimas: La víctima es una joven de 16 años.


Victimario o Presunto Agresor: Jesús C. M."""
    classification_standard_model(new_example)
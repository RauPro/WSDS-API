import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
nltk.download('punkt')
nltk.download('stopwords')

palabras_clave_prioridad = {
    1: {
        "sustantivo": ["homicidio", "feminicidio", "osamenta", "fosa_clandestina", "grupo_de_exterminio"],
        "sinonimos": [],
        "terminos_coloquiales": []
    },
    2: {
        "sustantivo": ["homicida", "feminicida"],
        "sinonimos": [],
        "terminos_coloquiales": []
    },
    3: {
        "sustantivo": ["crimen", "sin_vida", "cuerpo_sin_vida", "cuerpo_en_estado_de_descomposicion", "cadaver_en_estado_de_descomposicion", "estado_de_putrefaccion", "semienterrado", "cadaver", "cuerpo"],
        "sinonimos": ["fallecer", "morir", "suicidar", "perder_la_vida", "arrebatar_la_vida", "quitar_la_vida"],
        "terminos_coloquiales": []
    },
    4: {
        "sustantivo": ["arma_blanca", "arma_de_fuego", "machete", "cuchillo", "arma_contundente", "corvo"],
        "sinonimos": [],
        "terminos_coloquiales": ["a_tiros", "tiroteo", "impactos_de_bala", "balazo", "balazos", "disparos"]
    },
    5: {
        "sustantivo": ["acto_de_intolerancia", "alcohol", "droga", "privada_de_libertad", "defensa_propia", "rencilla_personal", "legitima_defensa", "violencia", "sangre", "ataque_de_esquizofrenia", "ataque"],
        "sinonimos": ["robar", "atacar", "apunalar", "disparar", "agredir", "lesionar", "apalera", "golpear", "vapulear", "ahorcar", "hurtar", "amenazar", "pelear", "defender", "herir"],
        "terminos_coloquiales": ["pelea", "golpiza", "golpe", "ahorcamiento"]
    },
}

def preprocess_text(text):
    text = text.lower()
    text_tokens = word_tokenize(text)
    tokens_without_sw = [word for word in text_tokens if not word in stopwords.words('spanish')]
    return tokens_without_sw

def calculate_score(texto):
    tokens = preprocess_text(texto)
    score = 0
    for prior, category in palabras_clave_prioridad.items():
        for cat, keywords in category.items():
            for token in tokens:
                if token in keywords:
                    score += (6 - prior)  # Asume que 1er orden suma 5, 2do orden suma 4, etc.
    return score

homicidio_threshold = 5 

def classify_new(texto):
    score = calculate_score(texto)
    if score >= homicidio_threshold:
        return "Homicidio"
    else:
        return "Otros"


import json
from datetime import date, datetime
import random
from typing import Generator
from fastapi import HTTPException, APIRouter
from starlette.responses import StreamingResponse
from app.controllers import create_news_gemma
from app.services import ElSalvadorScraper, DiarioColatinoScrapper, DiarioElSalvadorScrapper, DiarioElMundoScrapper
from app.services.driver.news_crud import create_new

router = APIRouter()


async def perform_scraping(scraper) -> tuple:
    """
    Perform web scraping using the provided scraper.

    Args:
        scraper: The web scraper instance.

    Returns:
        list: A list of scraped content URLs.
    """
    urls, results = scraper.init_search_urls()
    content_urls = [scraper.get_url_content(url) for url in urls]
    return content_urls, results


@router.get("/colatino")
async def colatino(search: str = "", date: str = "") -> list:
    """
    Route for Diario Colatino scraper.

    Args:
        search (str): The search term (default: "").
        date (str): The date (default: "").

    Returns:
        list: A list of scraped content URLs.
    """
    scraper = DiarioColatinoScrapper(search)
    return await perform_scraping(scraper)


@router.get("/diarioelmundo")
async def diarioelmundo(search: str = "", date_start: str = "", date_end: str = "") -> list:
    """
    Route for Diario El Mundo scraper.

    Args:
        search (str): The search term (default: "").
        date_start (str): The start date (default: "").
        date_end (str): The end date (default: "").

    Returns:
        list: A list of scraped content URLs.
    """
    if date_start is None:
        date_start = date.today().isoformat()
        date_end = date.today().isoformat()

    scraper = DiarioElMundoScrapper(search, date_start, date_end)
    return await perform_scraping(scraper)


@router.get("/diarioelsalvador")
async def diarioelsalvador(search: str = "Feminicidio", date: str = "") -> list:
    """
    Route for Diario El Salvador scraper.

    Args:
        search (str): The search term (default: "Feminicidio").
        date (str): The date (default: "").

    Returns:
        list: A list of scraped content URLs.
    """
    scraper = DiarioElSalvadorScrapper(search)
    return await perform_scraping(scraper)


@router.get("/global")
async def global_search(search: str = "Feminicidio") -> StreamingResponse:
    """
    Route for global search across multiple sources.

    Args:
        search (str): The search term (default: "Feminicidio").

    Returns:
        StreamingResponse: A streaming response containing the scraped content URLs.
    """
    scrapers = [
        DiarioElSalvadorScrapper(search),
        DiarioColatinoScrapper(search),
        DiarioElMundoScrapper(search)
    ]
    scrapersName = [
        "Diario El Salvador",
        "Diario Colatino",
        "Diario El mundo"
    ]

    async def event_stream() -> Generator[str, None, None]:
        content_urls = []
        for i, scraper in enumerate(scrapers):
            scraper_urls = await perform_scraping(scraper)
            for url_content in scraper_urls:
                if url_content is not None:
                    url_content['tag'] = search
                    url_content['date'] = datetime.today().strftime('%Y-%m-%d')
                    saved = create_new(url_content)
                    yield f"data: {json.dumps({'saved': saved, 'scraper': scrapersName[i]})}\n\n"
                    yield f"data: {json.dumps({'status': 'starting', 'scraper': scrapersName[i]})}\n\n"
            content_urls.extend(scraper_urls)
            yield f"data: {json.dumps({'status': 'completed', 'scraper': scrapersName[i], 'results': [url for url in scraper_urls if url is not None]})}\n\n"

        random.shuffle(content_urls)
        content_urls = [url for url in content_urls if url is not None]
        yield f"data: {json.dumps({'status': 'final', 'results': content_urls})}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")


def global_search_static(search: str = "Feminicidio", date_start: str = "", date_end: str = "", number_search: int = 10,
                         start_from: int = 0) -> list:
    """
    Perform a static global search across multiple sources.

    Args:
        search (str): The search term (default: "Feminicidio").
        date_start (str): The start date (default: "").
        date_end (str): The end date (default: "").
        start_from: index of the started element
        number_search:  number of results
    Returns:
        list: A list of scraped content URLs.

    """
    if date_start is None:
        date_start = date.today().isoformat()
        date_end = date.today().isoformat()

    scrapers = [
        DiarioElSalvadorScrapper(search, date_start, date_end, number_search, start_from),
        DiarioColatinoScrapper(search, date_start, date_end, number_search, start_from),
        DiarioElMundoScrapper(search, date_start, date_end, number_search, start_from)
    ]
    content_urls = []
    for scraper in scrapers:
        scraper_urls = [scraper.get_url_content(url) for url in scraper.init_search_urls()[0]]
        for url_content in scraper_urls:
            if url_content is not None:
                url_content['tag'] = search
        content_urls.extend(scraper_urls)
    return content_urls


@router.get("/total_results")
def get_pagination_number(search: str = "Feminicidio", date_start: str = "", date_end: str = "",
                          number_search=10, start_from=0) -> int:
    """
    Perform a static global search across multiple sources looking for pagination.

    Args:
        search (str): The search term (default: "Feminicidio").
        date_start (str): The start date (default: "").
        date_end (str): The end date (default: "").
        number_search (int): results
    Returns:
        int: the number of results
    """
    if date_start is None:
        date_start = date.today().isoformat()
        date_end = date.today().isoformat()

    scrapers = [
        DiarioElSalvadorScrapper(search, date_start, date_end, number_search),
        DiarioColatinoScrapper(search, date_start, date_end, number_search),
        DiarioElMundoScrapper(search, date_start, date_end, number_search)
    ]
    total_results = 0
    for scraper in scrapers:
        results = scraper.init_search_urls()
        total_results += int(results[1])

    return total_results


mocked = [
    {
        "title": "Fin de semana sin homicidios en El Salvador",
        "text": "La Policía Nacional Civil (PNC) confirmó en su cuenta de X (antes Twitter) que el domingo 16 de junio no hubo homicidios en todo el territorio nacional. Con estas nueva estadística, son tres días consecutivo (14, 15 y 16 de junio) que El Salvador amanece sin homicidios, lo que demuestra el impacto positivo de las estrategias de seguridad que ha puesto en marcha el Gobierno. «Finalizamos el domingo 16 de junio, con 0 homicidios en el país», destacó la PNC. El Plan Control Territorial ha sido reforzado con el régimen de excepción para que los pandilleros enfrenten a la justicia, lo que ha derivado en la captura de miles de estos criminales. Hoy, El Salvador se ha transformado y destacado por aspectos positivos como el incremento de la seguridad y la llegada de turistas extranjeros al país.",
        "source": "diarioelsalvador.com",
        "url": "https://diarioelsalvador.com/fin-de-semana-sin-homicidio-en-el-salvador/519528/",
        "sheet_id": "https://diarioelsalvador.com/fin-de-semana-sin-homicidio-en-el-salvador/519528/",
        "date": "2024-06-17",
        "tag": "Homicidio",
        "sheet": {
            "indicators": [
                {
                    "indicator_name": "Clasificación",
                    "response": "** N/A"
                },
                {
                    "indicator_name": "Título",
                    "response": "** Fin de semana sin homicidios en El Salvador"
                },
                {
                    "indicator_name": "Resumen",
                    "response": "** La policía nacional de El Salvador confirmó que no hay homicidios en el país el domingo 16 de junio."
                },
                {
                    "indicator_name": "Lugar de los Hechos",
                    "response": "** N/A"
                },
                {
                    "indicator_name": "Fuentes",
                    "response": "** N/A"
                },
                {
                    "indicator_name": "Temas",
                    "response": "** Seguridad, reducción de homicidios."
                },
                {
                    "indicator_name": "Hechos Violatorios",
                    "response": "** N/A"
                },
                {
                    "indicator_name": "Hipótesis de Hechos",
                    "response": "** N/A"
                },
                {
                    "indicator_name": "Población Vulnerable",
                    "response": "** N/A"
                },
                {
                    "indicator_name": "Tipo de Arma",
                    "response": "** N/A"
                },
                {
                    "indicator_name": "Víctimas",
                    "response": "** N/A"
                },
                {
                    "indicator_name": "Victimario o Presunto Agresor",
                    "response": "N/A"
                }
            ],
            "id": "https://diarioelsalvador.com/fin-de-semana-sin-homicidio-en-el-salvador/519528/",
            "priority": 4,
            "_id": "6670d7410eb47c223af309d1"
        }
    },
    {
        "title": "Asesinan en México a alcalde electo de municipio del estado de Guerrero",
        "text": "Salvador Villalba Flores, electo presidente municipal de Copala por el nuevo partido regional México Avanza (izquierda), fue ultimado en la carretera Acapulco-Pinotepa Nacional, apuntó en un comunicado la fiscalía de Guerrero. La institución añadió que inició la investigación por homicidio calificado, sin dar más detalles. El Sur de Guerrero, un periódico de esa región, apuntó que Villalba es capitán retirado de la secretaría de Marina y contaba con escoltas de la Guardia Nacional, quienes sin embargo no lo acompañaron a un viaje que estaba haciendo a Ciudad de México cuando fue asesinado. «El alcalde electo fue bajado del autobús en el que viajaba cuando la unidad hizo alto cerca de San Pedro las Playas» en la madrugada del lunes para asesinarlo a balazos, apuntó ese medio de comunicación en su página web. Según versiones de medios de Guerrero, Villalba decidió competir en las elecciones luego del asesinato de su amigo Jesús González Ríos, dirigente del Partido Verde de México en Copala, registrado el 29 de junio de 2023. Violencia derivada del narcotráfico México celebró elecciones generales el pasado 2 de junio. En esos comicios la izquierdista Claudia Sheinbaum fue elegida por una abrumadora mayoría como la primera presidenta de la historia del país latinoamericano. Durante la campaña electoral, que comenzó en septiembre, una treintena de candidatos a diversos cargos fueron asesinados, según la oenegé Data Cívica. Guerrero, uno de los estados más convulsionados por la actividad de los cárteles del narcotráfico que tiene costas en el Pacífico, acumuló 1.890 asesinatos en 2023 debido principalmente a la violencia de las organizaciones criminales. Uno de esos asesinados fue Yonis Baños, candidato del centrista Partido Revolucionario Institucional (PRI) a la alcaldía de Santo Domingo Armenta, del estado de Oaxaca, que junto con Guerrero es una de las regiones más pobres del país. Baños fue ultimado después del cierre de casillas de las elecciones del 2 de junio. El crimen lo perpetró una persona que ingresó a su casa, informó ese día el gobierno de Oaxaca. El candidato abatido no había solicitado a las autoridades ninguna medida de protección para resguardar su integridad ante autoridades estatales o federales.",
        "source": "diarioelsalvador.com",
        "url": "https://diarioelsalvador.com/asesinan-en-mexico-a-alcalde-electo-de-municipio-del-estado-de-guerrero/519613/",
        "sheet_id": "https://diarioelsalvador.com/asesinan-en-mexico-a-alcalde-electo-de-municipio-del-estado-de-guerrero/519613/",
        "date": "2024-06-17",
        "tag": "Homicidio",
        "sheet": {
            "indicators": [
                {
                    "indicator_name": "Clasificación",
                    "response": "** Homicidio"
                },
                {
                    "indicator_name": "Título",
                    "response": "** Asesinan en México a alcalde electo de municipio del estado de Guerrero"
                },
                {
                    "indicator_name": "Resumen",
                    "response": "** El alcalde electo de Copala por el nuevo partido regional México Avanza (izquierda), Salvador Villalba Flores, fue asesinado en la carretera Acapulco-Pinotepa Nacional."
                },
                {
                    "indicator_name": "Lugar de los Hechos",
                    "response": "** La carretera Acapulco-Pinotepa Nacional, en Guerrero, México."
                },
                {
                    "indicator_name": "Fuentes",
                    "response": "** N/A"
                },
                {
                    "indicator_name": "Temas",
                    "response": "** Seguridad pública, violencia, asesinato, política."
                },
                {
                    "indicator_name": "Hechos Violatorios",
                    "response": "** El asesinato se perpetró con una arma de fuego."
                },
                {
                    "indicator_name": "Hipótesis de Hechos",
                    "response": "** No se especifica en la noticia."
                },
                {
                    "indicator_name": "Población Vulnerable",
                    "response": "** Los políticos en México."
                },
                {
                    "indicator_name": "Tipo de Arma",
                    "response": "** Arma de fuego."
                },
                {
                    "indicator_name": "Víctimas",
                    "response": "** El alcalde electo, Salvador Villalba Flores."
                },
                {
                    "indicator_name": "Victimario o Presunto Agresor",
                    "response": "N/A"
                }
            ],
            "id": "https://diarioelsalvador.com/asesinan-en-mexico-a-alcalde-electo-de-municipio-del-estado-de-guerrero/519613/",
            "priority": 4,
            "_id": "6670d74a0eb47c223af309d2"
        }
    },
    {
        "title": "Continúan las lluvias en El Salvador y se registran vientos de hasta 45 kilómetros por hora",
        "text": "El Ministerio de Medio Ambiente y Recursos Naturales (MARN) informó sobre el registro de fuertes ráfagas de viento que alcanzan hasta los 45 kilómetros por hora; además de la ocurrencia de luvias en distintos puntos del país. «Continúan las lluvias fuertes en Ahuachapán, Sonsonate, Santa Ana y La Libertad. Se registran ráfagas de viento de hasta 45 km/h. En el resto del país, incluyendo el AMSS, se mantienen las lluvias dispersas de intensidades variables», informó la institución. Las condiciones climáticas han generado probabilidades entre un 80 % y 100 % de ocurrencia de flujos de escombros, deslizamientos y caídas de roca, lo que podría generar daños a la población, en infraestructura, medios de vida e interrupciones prolongadas en la movilidad en San Francisco Menéndez, Tacuba, Comasagua, Tamanique, Chiltiupán, Jicalapa, Teotepeque, Santa Isabel Ishuatán, entre otros. Desde las 7 de la mañana de ayer, domingo 16 de junio, hasta las 4:30 de la madrugada de este 17, Apaneca registra 307.6 milímetros de lluvia acumulada, seguido con 205.6 mm en San Francisco Menéndez y 166.4 mm en Juayúa. El Salvador se encuentra en alerta roja debido a las fuertes lluvias que han impactado en el país en los últimos días. La Asamblea Legislativa decretó Estado de Emergencia a escala nacional durante 15 días.",
        "source": "diarioelsalvador.com",
        "url": "https://diarioelsalvador.com/continuan-las-lluvias-en-el-salvador-y-se-registran-vientos-de-hasta-45-kilometros-por-hora/519533/",
        "sheet_id": "https://diarioelsalvador.com/continuan-las-lluvias-en-el-salvador-y-se-registran-vientos-de-hasta-45-kilometros-por-hora/519533/",
        "date": "2024-06-17",
        "tag": "Homicidio",
        "sheet": {
            "indicators": [
                {
                    "indicator_name": "Clasificación",
                    "response": "** N/A"
                },
                {
                    "indicator_name": "Título",
                    "response": "** Continúan las lluvias en El Salvador y se registran vientos de hasta 45 kilómetros por hora"
                },
                {
                    "indicator_name": "Resumen",
                    "response": "** El Ministerio de Medio Ambiente y Recursos Naturales (MARN) informó sobre el registro de fuertes ráfagas de viento que alcanzan hasta los 45 kilómetros por hora."
                },
                {
                    "indicator_name": "Lugar de los Hechos",
                    "response": "** No se especifica en la noticia."
                },
                {
                    "indicator_name": "Fuentes",
                    "response": "** No se especifica en la noticia."
                },
                {
                    "indicator_name": "Temas",
                    "response": "** Las condiciones climáticas y las lluvias."
                },
                {
                    "indicator_name": "Hechos Violatorios",
                    "response": "** No se especifica en la noticia."
                },
                {
                    "indicator_name": "Hipótesis de Hechos",
                    "response": "** No se especifica en la noticia."
                },
                {
                    "indicator_name": "Población Vulnerable",
                    "response": "** No se especifica en la noticia."
                },
                {
                    "indicator_name": "Tipo de Arma",
                    "response": "** No se especifica en la noticia."
                },
                {
                    "indicator_name": "Víctimas",
                    "response": "** No se especifica en la noticia."
                },
                {
                    "indicator_name": "Victimario o Presunto Agresor",
                    "response": "N/A"
                }
            ],
            "id": "https://diarioelsalvador.com/continuan-las-lluvias-en-el-salvador-y-se-registran-vientos-de-hasta-45-kilometros-por-hora/519533/",
            "priority": 4,
            "_id": "6670d7530eb47c223af309d3"
        }
    },
    {
        "title": "Patricia Bullrich, ministra de Seguridad de Argentina, visita El Salvador para conocer «El Modelo Bukele»",
        "text": "La ministra de Seguridad de Argentina, Patricia Bullrich, se encuentra en El Salvador para mantener un intercambio con las autoridades del Gabinete de Seguridad del país y conocer así «El Modelo Bukele» para combatir la violencia y la delincuencia. La funcionaria del gobierno de Javier Milei en la nación suramericana se encuentra en el país para conocer el trabajo del gobierno de Nayib Bukele en la reducción histórica de la violencia que ha experimentado El Salvador durante su mandato, con el fin de retomarlo como un ejemplo para implementar en Argentina. Bullrich fue recibida por el ministro de Seguridad, Gustavo Villatoro, quien la acompañó por un recorrido en el Centro de Confinamiento del Terrorismo (Cecot), la megacárcel construida bajo el mandato de Nayib Bukele y que funciona como parte de las estrategias para erradicar a las pandillas del territorio salvadoreño. Como fruto de la reunión bilateral entre el Presidente @nayibbukele y el Presidente @JMilei, le damos la bienvenida a la Ministra @PatoBullrich, al país más seguro de América Latina. Es un verdadero placer recibirla en El Salvador, estoy seguro de que esta visita desde… pic.twitter.com/rxhuR8rqBz «Como fruto de la reunión bilateral entre el Presidente @nayibbukele y el Presidente @JMilei, le damos la bienvenida a la Ministra @PatoBullrich, al país más seguro de América Latina. Es un verdadero placer recibirla en El Salvador, estoy seguro de que esta visita desde Argentina será enriquecedora, usted y su equipo van a poder conocer de primera mano el “Modelo Bukele”», publicó el ministro Villatoro en la red social X. El pasado mes de febrero, Bullrich sostuvo un breve encuentro con el presidente Nayib Bukele. La funcionaria publicó en su cuenta de X un video sobre el encuentro con el mandatario salvadoreño enfatizando en el deseo del actual gobierno argentino de retomar las estrategias de El Salvador para combatir la delincuencia. «De una masacre diaria y un país controlado por las maras (bandas criminales) a una sociedad donde se cuida la vida. Una experiencia donde se cuida a la gente y el delincuente no es bienvenido. ¡Hacia allí vamos!», publicó la ministra argentina en su cuenta de X tras el encuentro con Bukele. El encuentro entre Bullrich y Bukele se produjo en el marco de la Conferencia Política de Acción Conservadora (CPAC), en la que Bukele participó como invitado especial, los logros en seguridad pública que tiene El Salvador y que lo han llevado a posicionarse como el país más seguro de América Latina.",
        "source": "diarioelsalvador.com",
        "url": "https://diarioelsalvador.com/patricia-bullrich-ministra-de-seguridad-de-argentina-visita-el-salvador-para-conocer-el-modelo-bukele/519392/",
        "sheet_id": "https://diarioelsalvador.com/patricia-bullrich-ministra-de-seguridad-de-argentina-visita-el-salvador-para-conocer-el-modelo-bukele/519392/",
        "date": "2024-06-16",
        "tag": "Homicidio",
        "sheet": {
            "indicators": [
                {
                    "indicator_name": "Clasificación",
                    "response": "** N/A"
                },
                {
                    "indicator_name": "Título",
                    "response": "** Patricia Bullrich, ministra de Seguridad de Argentina, visita El Salvador para conocer «El Modelo Bukele»"
                },
                {
                    "indicator_name": "Resumen",
                    "response": "** La ministra de Seguridad de Argentina, Patricia Bullrich, se encuentra en El Salvador para mantener un intercambio con las autoridades del Gabinete de Seguridad del país y conocer el \"Modelo Bukele\" para combater la violencia y la delincuencia."
                },
                {
                    "indicator_name": "Lugar de los Hechos",
                    "response": "** El Salvador"
                },
                {
                    "indicator_name": "Fuentes",
                    "response": "** No se especifica en la noticia"
                },
                {
                    "indicator_name": "Temas",
                    "response": "** Seguridad, delincuencia, El Salvador, Argentina"
                },
                {
                    "indicator_name": "Hechos Violatorios",
                    "response": "** No se especifica en la noticia"
                },
                {
                    "indicator_name": "Hipótesis de Hechos",
                    "response": "** No se especifica en la noticia"
                },
                {
                    "indicator_name": "Población Vulnerable",
                    "response": "** No se especifica en la noticia"
                },
                {
                    "indicator_name": "Tipo de Arma",
                    "response": "** No se especifica en la noticia"
                },
                {
                    "indicator_name": "Víctimas",
                    "response": "** No se especifica en la noticia"
                },
                {
                    "indicator_name": "Victimario o Presunto Agresor",
                    "response": "N/A"
                }
            ],
            "id": "https://diarioelsalvador.com/patricia-bullrich-ministra-de-seguridad-de-argentina-visita-el-salvador-para-conocer-el-modelo-bukele/519392/",
            "priority": 4,
            "_id": "6670d75c0eb47c223af309d4"
        }
    },
    {
        "title": "En tres años y medio 1,351 agresores sexuales de menores fueron condenados",
        "text": "La efectividad de las medidas de seguridad implementadas por el Gobierno se ve reflejada no solo en los más de 80,000 pandilleros y sus colaboradores capturados en más de 26 meses o los más de 500 días con cero homicidios reportados en dicho periodo, también se refleja en la capacidad que ahora tienen las autoridades para capturar, judicializar y encarcelar a delincuentes que comenten otros delitos como agresiones sexuales contra menores de edad. Según las estadísticas de la Fiscalía General de la República (FGR), entre enero de 2021 y mayo de 2024, un total de 1,351 personas han sido procesadas y condenadas por agredir sexualmente a menores de edad. «La división de la Fiscalía en diversas fiscalías adjuntas ha permitido de que una buena parte del personal de fiscales se dedique también a combatir otro tipo de manifestaciones delictivas que también se han dado durante todo este periodo [del régimen de excepción], estamos hablando de los delitos de naturaleza sexual en los cuales hay una Fiscalía Adjunta que se encarga exclusivamente de investigar ese tipo de hechos», indicó el fiscal general, Rodolfo Delgado. Agregó «lo que sucede es que era tanta la capacidad criminal que tenían estas pandillas que invisibilizaban otros fenómenos criminales que se estaban dando, entonces cuando salen de la escena las pandillas, como se ha hecho hasta este momento, eso también nos ha permitido a la Fiscalía y a la Policía poder investigar otros fenómenos criminales principalmente relacionados con estafas, delitos de contenido patrimonial, como falsedades, cometidos en perjuicio de la propiedad de los salvadoreños, y los delitos de naturaleza sexual». Del total de procesados en tres años y medio, 663 han sido condenados por el delito de agresión sexual en menor e incapaz, de estos 198 fueron sentenciados en 2021, otros 173 en 2022, en el 2023 fueron condenados 209 y 83 en lo que va del 2024. Por los delitos de violación en menor e incapaz y agresión sexual en menor e incapaz, fue condenado el pasado 23 de mayo, a 40 años de cárcel Salvador Antonio Velásquez Martínez. «Con abundante prueba de cargo la Fiscalía demostró que el imputado comenzó a violar a la niña desde el año 2022, aprovechando que quedaba a solas en su vivienda y bajo amenazas la sometió en repetidas ocasiones», indicó el fiscal del caso. Los delitos se cometieron en una colonia del distrito de Soyapango, en el municipio de San Salvador Este. El Tribunal Tercero de Sentencia de San Salvador, lo declaró responsable penalmente por los ilícitos de violación en menor e incapaz y agresión sexual en menor e incapaz, imponiéndole 20 años de prisión por cada uno de los delitos. MÁS ACUSACIONES Respecto al delito de agresión sexual en menor e incapaz agravada un total de 181 personas han sido condenadas entre 2019 y 2024, de estos, 51 fueron sentenciados en 2021, un total de 52 en el 2022, en el año 2023 hasta 55 personas fueron condenadas por dicho delito, y 23 en lo que va del 2024. Mientras que, el delito de agresión sexual en menor e incapaz en su modalidad continuada 253 han sido condenadas en tres años y medio, y 254 han recibido sentencias por el delito de agresión sexual en menor o incapaz continuada. El pasado 4 de junio, el Tribunal Segundo de Sentencia de Santa Tecla condenó a 16 años de cárcel a Juan Rafael López Monterrosa por agredir sexualmente a una niña de 5 años. Los abusos fueron cometidos en reiteradas ocasiones. «Los hechos sucedieron en el año 2013 en la casa de habitación de la víctima, ubicada en la lotificación La Esperanza, distrito de Huizúcar, en el municipio de La Libertad Este», señaló el fiscal del caso. La fuente detalló que el imputado era la pareja sentimental de la madre de la víctima. López Monterrosa aprovechaba para tocar indebidamente el cuerpo de la menor cuando la madre salía de casa a trabajar, el imputado era el encargado del cuido de la víctima y su hermano. «Después de agredir a la niña, el procesado le daba chocolates, churros y galletas para que callara. En el 2023, tras varios años de abuso, la menor decidió escribirle una carta a su mamá para contarle sobre las agresiones, y ella interpuso la denuncia», apuntó el fiscal. Tras la evidencia presentada por la Fiscalía en el juicio, el respectivo tribunal condenó al imputado por el delito de agresión sexual en menor o incapaz agravada continuada. MÁS DE 1,800 CAPTURADOS Las estadísticas de la Fiscalía también dan cuenta que un total de 1,802 personas han sido capturadas entre enero de 2021 y mayo de 2024 por agredir sexualmente a menores de edad. De dicho total, 884 han sido detenidos por el delito de agresión sexual en menor e incapaz, de estos 261 fueron aprendidos en 2021, otros 216 en 2022, mientras que, en el 2023 las autoridades capturaron a 301 personas por dicho delito y 106 en este 2024. En Ciudad Arce, La Libertad, capturamos a Wilber Alonso Rodríguez Ramírez, alias Chele Lee, homeboy de la MS13, clica Hollywood Locos Salvatruchos. Se encargaba de extorsionar a los habitantes de San Sebastián Salitrillo, Santa Ana, pero trató de huir de la… pic.twitter.com/P0h7UFhMVj Las estadísticas, además, reflejan que por el delito de agresión sexual en menor e incapaz agravada un total de 249 han sido detenidas en tres años y medio; mientras que, por el delito de agresión sexual en menor e incapaz en su modalidad continuada se han capturado a 310 y otras 359 personas han sido aprendidas por agresión sexual en menor o incapaz continuada. El pasado 3 de junio, la Policía reportó la captura de Edwin Oswaldo Núñez, quien será procesado por el delito de agresión sexualmente a una menor de edad. «En Santa Ana, capturamos a Edwin Oswaldo Núñez de 38 años, quien cuenta con orden de captura por agresión sexual agravada en menor e incapaz», informó la corporación policial. La Policía añadió que Núñez fue remitido al Juez Primero de Sentencia de Santa Ana, para que sea judicializado por dicho delito.",
        "source": "diarioelsalvador.com",
        "url": "https://diarioelsalvador.com/en-tres-anos-y-medio-1351-agresores-sexuales-de-menores-fueron-condenados/515666/",
        "sheet_id": "https://diarioelsalvador.com/en-tres-anos-y-medio-1351-agresores-sexuales-de-menores-fueron-condenados/515666/",
        "date": "2024-06-17",
        "tag": "Homicidio",
        "sheet": {
            "indicators": [
                {
                    "indicator_name": "Clasificación",
                    "response": "** No es un caso de homicidio. La noticia describe la captura y condena de individuos por delitos de agresión sexual contra menores de edad."
                },
                {
                    "indicator_name": "Título",
                    "response": "N/A"
                },
                {
                    "indicator_name": "Resumen",
                    "response": "N/A"
                },
                {
                    "indicator_name": "Lugar de los Hechos",
                    "response": "N/A"
                },
                {
                    "indicator_name": "Fuentes",
                    "response": "N/A"
                },
                {
                    "indicator_name": "Temas",
                    "response": "N/A"
                },
                {
                    "indicator_name": "Hechos Violatorios",
                    "response": "N/A"
                },
                {
                    "indicator_name": "Hipótesis de Hechos",
                    "response": "N/A"
                },
                {
                    "indicator_name": "Población Vulnerable",
                    "response": "N/A"
                },
                {
                    "indicator_name": "Tipo de Arma",
                    "response": "N/A"
                },
                {
                    "indicator_name": "Víctimas",
                    "response": "N/A"
                },
                {
                    "indicator_name": "Victimario o Presunto Agresor",
                    "response": "N/A"
                }
            ],
            "id": "https://diarioelsalvador.com/en-tres-anos-y-medio-1351-agresores-sexuales-de-menores-fueron-condenados/515666/",
            "priority": 4,
            "_id": "6670d7610eb47c223af309d5"
        }
    },
    {
        "title": "Senador de EE. UU., Marco Rubio, destaca la seguridad de El Salvador",
        "text": "El senador estadounidense, Marco Rubio, destacó los avances en materia de seguridad que registra El Salvador desde que inició el Gobierno del presidente de la república, Nayib Bukele. En un video compartido por el mandatario salvadoreño en la red social «X», Rubio resaltó que El Salvador era uno de los países más peligrosos del mundo y que ahora, gracias a los planes de seguridad de Nayib Bukele, se ha convertido en la nación más segura del hemisferio occidental. «De repente, la tasa de homicidios ha caído en picada, por primera vez en décadas, la gente puede salir por la noche, la gente ya no tiene que pagar extorsión a la pandilla», expresó.El senador informó que recientemente realizó una visita oficial de dos días a El Salvador y pudo constatar la transformación que vive el país. «Eligieron a un nuevo presidente, Nayib Bukele, y él logró que el órgano legislativo le concediera autoridades especiales durante un período delimitado. Él usó esta autoridad para salir y atrapar a todos los pandilleros», dijo.Subrayó que el Gobierno salvadoreño ha logrado la captura de más de 40,000 pandilleros y una reducción sustancial en la tasa de homicidios. Aseguró que el presidente Bukele «ha querido llevarse bien» con el gobierno de Joe Biden; sin embargo, Rubio desaprobó el accionar del jefe del estado norteamericano hacia países como El Salvador y República Dominicana. «Tenemos un problema con nuestra política exterior. Tratamos mejor a nuestros enemigos que a nuestros amigos. Tenemos un gobierno que hace hasta lo imposible por tratar de acomodar a Maduro, un gobierno que tiene miedo de hacer algo fuerte contra Ortega en Nicaragua, o contra el régimen en Cuba, pero por otro lado deciden: “me voy a hacer el fuerte contra El Salvador, los voy a sancionar, voy a hablar mal de ellos e intentar hacer de ese país una paria mundial”», señaló.",
        "source": "diarioelsalvador.com",
        "url": "https://diarioelsalvador.com/senador-de-ee-uu-destaca-la-seguridad-de-el-salvador/519029/",
        "sheet_id": "https://diarioelsalvador.com/senador-de-ee-uu-destaca-la-seguridad-de-el-salvador/519029/",
        "date": "2024-06-16",
        "tag": "Homicidio",
        "sheet": {
            "indicators": [
                {
                    "indicator_name": "Clasificación",
                    "response": "** Homicidio"
                },
                {
                    "indicator_name": "Título",
                    "response": "** Senador de EE. UU., Marco Rubio, destaca la seguridad de El Salvador"
                },
                {
                    "indicator_name": "Resumen",
                    "response": "** El senador estadounidense, Marco Rubio, destacó los avances en materia de seguridad que registra El Salvador desde que inició el Gobierno del presidente de la república, Nayib Bukele."
                },
                {
                    "indicator_name": "Lugar de los Hechos",
                    "response": "** No se especifica en la noticia."
                },
                {
                    "indicator_name": "Fuentes",
                    "response": "** No se especifica en la noticia."
                },
                {
                    "indicator_name": "Temas",
                    "response": "** Seguridad en El Salvador, reducción de homicidios, gobierno de Nayib Bukele."
                },
                {
                    "indicator_name": "Hechos Violatorios",
                    "response": "** No se especifica en la noticia."
                },
                {
                    "indicator_name": "Hipótesis de Hechos",
                    "response": "** No se especifica en la noticia."
                },
                {
                    "indicator_name": "Población Vulnerable",
                    "response": "** No se especifica en la noticia."
                },
                {
                    "indicator_name": "Tipo de Arma",
                    "response": "** No se especifica en la noticia."
                },
                {
                    "indicator_name": "Víctimas",
                    "response": "** No se especifica en la noticia."
                },
                {
                    "indicator_name": "Victimario o Presunto Agresor",
                    "response": "N/A"
                }
            ],
            "id": "https://diarioelsalvador.com/senador-de-ee-uu-destaca-la-seguridad-de-el-salvador/519029/",
            "priority": 4,
            "_id": "6670d76a0eb47c223af309d6"
        }
    },
    {
        "title": "Capturan a homicida en La Paz",
        "text": "La Policía Nacional Civil (PNC) confirmó este sábado por la tarde la captura de un sujeto implicado en un caso de homicidio y reclamado por un juzgado del departamento de San Salvador. El detenido responde al nombre de Santos Ernesto Luna Ayala, quien es perfilado por las autoridades policiales como el responsable de un homicidio cometido en 2014. Tras asesinar a un hombre en el año 2014, capturamos a Santos Ernesto Luna Ayala, quien era reclamado por un juzgado de San Salvador.Gracias a la efectividad de nuestros policías, la detención se realizó en la calle principal del caserío El Cabral, cantón El Limón, en San Pedro… pic.twitter.com/7T4AnPREdf La captura se llevó a cabo en la calle principal del caserío El Cabral, cantón El Limón, en el sector de San Pedro Masahuat, departamento de La Paz. La institución policial señaló que Luna Ayala será entregado a los tribunales correspondientes para que sea procesado por el delito de homicidio agravado.",
        "source": "diarioelsalvador.com",
        "url": "https://diarioelsalvador.com/capturan-a-homicida-en-la-paz/519066/",
        "sheet_id": "https://diarioelsalvador.com/capturan-a-homicida-en-la-paz/519066/",
        "date": "2024-06-15",
        "tag": "Homicidio",
        "sheet": {
            "indicators": [
                {
                    "indicator_name": "Clasificación",
                    "response": "** Homicidio"
                },
                {
                    "indicator_name": "Título",
                    "response": "** Capturan a homicida en La Paz"
                },
                {
                    "indicator_name": "Resumen",
                    "response": "** La policía captura a un homicida en La Paz."
                },
                {
                    "indicator_name": "Lugar de los Hechos",
                    "response": "** Calle principal del caserío El Cabral, cantón El Limón, en San Pedro Masahuat, departamento de La Paz."
                },
                {
                    "indicator_name": "Fuentes",
                    "response": "** No se especifica la fuente de información."
                },
                {
                    "indicator_name": "Temas",
                    "response": "** Seguridad pública, crimen, homicidio."
                },
                {
                    "indicator_name": "Hechos Violatorios",
                    "response": "** No se especifica el delito específico."
                },
                {
                    "indicator_name": "Hipótesis de Hechos",
                    "response": "** No se especifica la hipótesis de hechos."
                },
                {
                    "indicator_name": "Población Vulnerable",
                    "response": "** No se especifica la población vulnerable."
                },
                {
                    "indicator_name": "Tipo de Arma",
                    "response": "** No se especifica el tipo de arma."
                },
                {
                    "indicator_name": "Víctimas",
                    "response": "** No se especifica el número de víctimas."
                },
                {
                    "indicator_name": "Victimario o Presunto Agresor",
                    "response": "N/A"
                }
            ],
            "id": "https://diarioelsalvador.com/capturan-a-homicida-en-la-paz/519066/",
            "priority": 4,
            "_id": "6670d7720eb47c223af309d7"
        }
    },
    {
        "title": "Aeropuerto Internacional de El Salvador recibe vuelos alternos de otros países debido a las lluvias",
        "text": "La Comisión Ejecutiva Portuaria Autónoma (CEPA) informó que, debido a la situación climatológica, el Aeropuerto Internacional San Oscar Arnulfo Romero, en San Luis Talpa, La Paz Oeste, está recibiendo vuelos alternos. La institución informó en su cuenta oficial de X, que se debe a que algunos aeropuertos de la región han tenido dificultades adversas. «Nuestro Aeropuerto Internacional de El Salvador está recibiendo vuelos alternos debido a las condiciones meteorológicas adversas que se han presentado en algunos aeropuertos de la región Centroamericana», informaron. Agregó que, en horas del mediodía de hoy, recibieron un vuelo de American Airlines procedente de Guatemala, debido a que no pudo aterrizar por las condiciones del clima. De igual forma, en la mañana se recibió un vuelo de Avianca con ruta de San José, Costa Rica; hacia Ciudad de Guatemala. En tanto, agregaron: «Mantenemos nuestro compromiso con la seguridad y eficiencia en nuestras operaciones aéreas», indican en la publicación. El Gobierno a través del Sistema Nacional de Protección Civil ha decretado alerta roja esta tarde debido a las lluvias tipo temporal, debido a la Depresión Tropical 19-E, ubicada al suroeste de la costa de El Salvador.",
        "source": "diarioelsalvador.com",
        "url": "https://diarioelsalvador.com/aeropuerto-internacional-de-el-salvador-recibe-vuelos-alternos-de-otros-paises-debido-a-las-lluvias/519290/",
        "sheet_id": "https://diarioelsalvador.com/aeropuerto-internacional-de-el-salvador-recibe-vuelos-alternos-de-otros-paises-debido-a-las-lluvias/519290/",
        "date": "2024-06-16",
        "tag": "Homicidio",
        "sheet": {
            "indicators": [
                {
                    "indicator_name": "Clasificación",
                    "response": "** N/A"
                },
                {
                    "indicator_name": "Título",
                    "response": "** Aeropuerto internacional de El Salvador recibe vuelos alternos de otros países debido a las lluvias"
                },
                {
                    "indicator_name": "Resumen",
                    "response": "** El Aeropuerto internacional de El Salvador está recibiendo vuelos alternos debido a las condiciones meteorológicas adversas que se han presentado en algunos aeropuertos de la región Centroamericana."
                },
                {
                    "indicator_name": "Lugar de los Hechos",
                    "response": "** San Luis Talpa, La Paz Oeste, El Salvador"
                },
                {
                    "indicator_name": "Fuentes",
                    "response": "** No se especifica en la noticia."
                },
                {
                    "indicator_name": "Temas",
                    "response": "** Seguridad, eficiencia, operaciones aéreas."
                },
                {
                    "indicator_name": "Hechos Violatorios",
                    "response": "** No se especifica en la noticia."
                },
                {
                    "indicator_name": "Hipótesis de Hechos",
                    "response": "** No se especifica en la noticia."
                },
                {
                    "indicator_name": "Población Vulnerable",
                    "response": "** No se especifica en la noticia."
                },
                {
                    "indicator_name": "Tipo de Arma",
                    "response": "** No se especifica en la noticia."
                },
                {
                    "indicator_name": "Víctimas",
                    "response": "** No se especifica en la noticia."
                },
                {
                    "indicator_name": "Victimario o Presunto Agresor",
                    "response": "N/A"
                }
            ],
            "id": "https://diarioelsalvador.com/aeropuerto-internacional-de-el-salvador-recibe-vuelos-alternos-de-otros-paises-debido-a-las-lluvias/519290/",
            "priority": 4,
            "_id": "6670d77b0eb47c223af309d8"
        }
    },
    {
        "title": "«El Salvador está posicionado para ser el Singapur de Occidente»: congresista Matthew Louis Gaetz",
        "text": "Matthew Louis Gaetz, congresista republicano de Estados Unidos (EE. UU.), destacó durante una entrevista cómo El Salvador, con la presidencia de Nayib Bukele, pasó de ser un «Estado fallido» a posicionarse para ser el Singapur del hemisferio occidental. El funcionario estadounidense recordó su reciente visita al país, con motivo de la ceremonia de investidura del presidente Bukele, que comenzó su segundo mandato el 1.º de junio anterior. «Acabo de regresar de El Salvador. Estuve en la investidura de Bukele. Es una de las personas más impresionantes que he conocido. Tenía frente a mí un país que básicamente era un Estado fallido y ahora está posicionado para ser el Singapur del hemisferio occidental», dijo Gaetz. Añadió que si El Salvador, siendo un país con 6 millones de habitantes, ha logrado alcanzar dicha posición, «con solo encerrar a 70,000 personas, entonces no me convenzo de que Canadá esté tan dominado por los globalistas que no pueda sobreponerse a ellos». La estrategia de seguridad del presidente Bukele, implementando el Plan Control Territorial, reforzado con el régimen de excepción, es la más exitosa en la historia del país y ejemplo en el mundo. El año pasado, la tasa de asesinatos cerró con 2.4 por cada 100,000 habitantes; además del descenso en el cometimiento de delitos como extorsiones, robos, hurtos y agresiones de todo tipo a escala nacional. Al cierre del primer trimestre de 2024 (enero-marzo) fue de 1.5. Ante los comentarios de la entrevistadora sobre la necesidad de que los países escojan a líderes «que crean en sus ciudadanos y quieran apoyarlos», el congresista Gaetz señaló que «así es, aunque debe ser más duradero que eso. Tiene que durar más que una sola persona, pero creo que en cada movimiento grande hay personas que se vuelven la vanguardia». «Vi personas en el congreso [Asamblea Legislativa], en su Gobierno, en el cuerpo diplomático, para quienes el bukelismo surge como un concepto […] y creo que eso es lo que atrae a la generación joven», reflexionó el congresista. Comentó que el presidente Bukele le mostró una fotografía que retrata cómo los estudiantes de una escuela pública ya no piensan en ser pandilleros o ladrones, sino policías, chefs y empresarios. «Comparen eso con lo nuestro», dijo, agregó su admiración porque en un karaoke salvadoreño encontró que se celebra el Día del Padre todo junio.",
        "source": "diarioelsalvador.com",
        "url": "https://diarioelsalvador.com/el-salvador-esta-posicionado-para-ser-el-singapur-de-occidente-congresista-matthew-louis-gaetz/518834/",
        "sheet_id": "https://diarioelsalvador.com/el-salvador-esta-posicionado-para-ser-el-singapur-de-occidente-congresista-matthew-louis-gaetz/518834/",
        "date": "2024-06-15",
        "tag": "Homicidio",
        "sheet": {
            "indicators": [
                {
                    "indicator_name": "Clasificación",
                    "response": "** N/A"
                },
                {
                    "indicator_name": "Título",
                    "response": "** El Salvador está posicionado para ser el Singapur de Occidente"
                },
                {
                    "indicator_name": "Resumen",
                    "response": "** La noticia informa sobre la opinión de un congresista estadounidense sobre el progreso del Salvador bajo la presidencia de Nayib Bukele."
                },
                {
                    "indicator_name": "Lugar de los Hechos",
                    "response": "** No se especifica el lugar de los hechos en la noticia."
                },
                {
                    "indicator_name": "Fuentes",
                    "response": "** No se indican las fuentes de información."
                },
                {
                    "indicator_name": "Temas",
                    "response": "** Seguridad, reducción de crímenes, Plan Control Territorial."
                },
                {
                    "indicator_name": "Hechos Violatorios",
                    "response": "** No se especifican los hechos violatorios."
                },
                {
                    "indicator_name": "Hipótesis de Hechos",
                    "response": "** No se presenta una hipótesis de hechos."
                },
                {
                    "indicator_name": "Población Vulnerable",
                    "response": "** No se menciona la población vulnerable."
                },
                {
                    "indicator_name": "Tipo de Arma",
                    "response": "** No se especifica el tipo de arma."
                },
                {
                    "indicator_name": "Víctimas",
                    "response": "** No se identifican las víctimas."
                },
                {
                    "indicator_name": "Victimario o Presunto Agresor",
                    "response": "N/A"
                }
            ],
            "id": "https://diarioelsalvador.com/el-salvador-esta-posicionado-para-ser-el-singapur-de-occidente-congresista-matthew-louis-gaetz/518834/",
            "priority": 4,
            "_id": "6670d7840eb47c223af309d9"
        }
    },
    {
        "title": "Un pandillero fue condenado a 498 años por cometer extorsiones",
        "text": "El Tribunal Segundo Contra el Crimen Organizado de San Miguel, impuso una condena de 498 años de prisión contra elpandillero José Joel Pineda Magaña, alias Caprichoso, informó la Fiscalía General de la República (FGR). Pineda en un primer proceso recibió una condena de 460 años por 23 casos de extorsión agravada; y en el segundo caso fue sentenciado a 38 por proposición y conspiración en el delito de homicidio y organizaciones terroristas. Según la FGR, él forma parte de una estructura delictiva que fue sentenciada a diferentes penas por delitos como extorsión, homicidio tentado y organizaciones terroristas. Carlos Alfredo Durán Moreira, alias Cara de Perro, recibió 360 años de cárcel por 18 casos de extorsión agravada; y se le sumaron 32 el en el segundo proceso por los delitos de proposición y conspiración en el delito de homicidio y organizaciones terroristas. «Durante la investigación fiscal se logró identificar a 24 víctimas de esta estructura delincuencial. Según la acusación fiscal, los terroristas les exigían a comerciantes, buseros y taxistas entre $40 y $100 mensuales para dejarlos trabajar», detalló la Fiscalía. Por los casos de extorsión también fueron condenados Raúl Ernesto Arévalo Álvarez, alias Raúl y José Isaac Portillo Torres, alias Drácula, quienes fueron sentenciados a 60 años de 3 extorsiones. Portillo Torres en el segundo proceso por proposición y conspiración en el delito de homicidio y organizaciones terroristas, recibió 152 años de prisión, junto a José Efraín Andrade Argueta, que deberá purgar una pena de 132 años. Cometieron los hechos entre enero y julio de 2020, en los distritos de Guatajiagua, de Morazán; y Ciudad Barrios, Chapeltique y Moncagua, de San Miguel.",
        "source": "diarioelsalvador.com",
        "url": "https://diarioelsalvador.com/un-pandillero-fue-condenado-a-498-anos-por-cometer-extorsiones/518669/",
        "sheet_id": "https://diarioelsalvador.com/un-pandillero-fue-condenado-a-498-anos-por-cometer-extorsiones/518669/",
        "date": "2024-06-14",
        "tag": "Homicidio",
        "sheet": {
            "indicators": [
                {
                    "indicator_name": "Clasificación",
                    "response": "** Homicidio"
                },
                {
                    "indicator_name": "Título",
                    "response": "** Un pandillero fue condenado a 498 años por cometer extorsiones"
                },
                {
                    "indicator_name": "Resumen",
                    "response": "** El pandillero José Joel Pineda Magaña, alias Caprichoso, fue condenado a 498 años de prisión por cometer extorsiones."
                },
                {
                    "indicator_name": "Lugar de los Hechos",
                    "response": "** Guatajiagua, de Morazán; Ciudad Barrios, Chapeltique y Moncagua, de San Miguel."
                },
                {
                    "indicator_name": "Fuentes",
                    "response": "** N/A"
                },
                {
                    "indicator_name": "Temas",
                    "response": "** Extorsión, crimen organizado."
                },
                {
                    "indicator_name": "Hechos Violatorios",
                    "response": "** La estructura delictiva exigía a las víctimas entre $40 y $100."
                },
                {
                    "indicator_name": "Hipótesis de Hechos",
                    "response": "** N/A"
                },
                {
                    "indicator_name": "Población Vulnerable",
                    "response": "** N/A"
                },
                {
                    "indicator_name": "Tipo de Arma",
                    "response": "** N/A"
                },
                {
                    "indicator_name": "Víctimas",
                    "response": "** Las víctimas de la estructura delictiva no se identifican en la noticia."
                },
                {
                    "indicator_name": "Victimario o Presunto Agresor",
                    "response": "N/A"
                }
            ],
            "id": "https://diarioelsalvador.com/un-pandillero-fue-condenado-a-498-anos-por-cometer-extorsiones/518669/",
            "priority": 4,
            "_id": "6670d78d0eb47c223af309da"
        }
    },
    {
        "title": "Algo que el ministerio de Justicia o Bukele deberían explicar",
        "text": "\n\nCompartir\n\n Facebook\n Twitter\n Google +\n\n\n\nLa semana pasada se conoció que en México fue capturado uno de los máximos jefes de la ranfla de la organización terrorista Mara Salvatrucha (MS), César Antonio López Larios, conocido como Greñas de Stoner, quien fue trasladado inmediatamente a Estados Unidos, que lo reclama al igual que otros líderes de esa organización criminal para ser juzgados por narcotráfico, entre otros delitos federales.\nMéxico informó que “Derivado de trabajos de inteligencia, elementos de la Policía de investigación, zona Istmo Costa, de la Fiscalía General del Estado (FGE) lograron la captura, en el municipio de Arriaga, Chiapas, de César Antonio López Larios, un objetivo prioritario buscado por el Gobierno de Estados Unidos”. Con Larios, suman siete los cabecillas o “ranfleros” de la MS detenidos en el exterior y que están siendo juzgados en una corte de un distrito de Nueva York.\nEs curioso, además de sospechoso, que, en El Salvador, pese a la guerra contra las pandillas decretada en marzo de 2022 por el entonces presidente constitucional Nayib Bukele, al decretar también el Estado de Excepción que, en el elevado número de capturas anunciadas por el Gobierno, no aparecen los cabecillas principales y secundarios de los grupos criminales MS, Barrio 18 sureños o revolucionarios. En el marco del Régimen de Excepción, que en un primer momento fue decretado como respuesta a un alza en los homicidios durante los últimos tres días de marzo del 2022, las autoridades de justicia informan de más de 80 mil capturados.\nLa prueba de esto es que la mayoría de líderes han sido capturados fuera del país.\nEn lo que va del año, por ejemplo, de Guatemala, Honduras y Nicaragua han informado de la entrega a las autoridades policiales de El Salvador jefes de clicas de las pandillas, que suman cerca de una centena. La mayoría capturados en Guatemala.\nSi a los anteriores le agregamos a los capturados en México, como el reciente caso de Larios, y antes del Cook, no se puede dudar que los líderes de los grupos terroristas están fuera del país, bien porque huyeron al poner en vigencia de estado de excepción, o como parte de las negociaciones entre esos grupos delincuenciales y el gobierno de Bukele. Entonces, si los jefes de las pandillas los capturan fuera del país, significa entonces que los 80 mil capturados, miles son inocentes, mientras que el resto son parte de la base social de esos grupos delincuenciales.\nPor decencia, por transparencia, el gobierno debería explicar por qué los “ranfleros” no han sido capturados en el marco del régimen de excepción. Por qué han ido contra la base social de esos grupos, muchos de los cuales, seguramente cumplieron un rol en el esquema delictivo, más por amenaza de los pandilleros, ante la falta de control territorial del estado que por afinidad a esos grupos.\nEl gobierno debería, por decencia, explicarle al país, por qué la negociación con las pandillas, qué se logró con ello, y por qué se rompió la tregua. Recordemos que en 2012, cuando se dio la tregua entre las pandillas, a pesar de que se intentó mantener en secreto, al final fue el propio presidente Mauricio Funes quien reconoció la “facilitación de la tregua”, bajo el compromiso de disminuir los homicidios y la libre circulación de “los civiles” en los territorios controlados por los delincuentes.\nEl gobierno debería explicar, por decencia, por qué el Estado de Excepción no ha servido para capturar a los líderes de las pandillas, pero sí para intimidar a la población en general. El cardenal Gregorio Rosa Chávez tiene razón al exigir que se le ponga fin al régimen de excepción “cuanto antes”, ya que “los frutos amargos” son grandes y “hay mucho sufrimiento”. Además, agregamos nosotros, el Régimen de Excepción no ha servido ni servirá para capturar a los cabecillas de los grupos delincuenciales, pues estos son capturados en el exterior, producto de la inteligencia policial y la investigación.\nPor supuesto que el Gobierno no dará marcha atrás al “Régimen”, porque este le está sirviendo al gobierno para mantener a raya a los salvadoreños, independientemente que hayan jurado o no “no quejarse por nada”.\nComparte esto:FacebookXMe gusta esto:Me gusta Cargando...\n\nRelacionado\n\n",
        "source": "diariocolatino.com",
        "url": "https://www.diariocolatino.com/algo-que-el-ministerio-de-justicia-o-bukele-deberian-explicar/",
        "sheet_id": "https://www.diariocolatino.com/algo-que-el-ministerio-de-justicia-o-bukele-deberian-explicar/",
        "date": "2024-06-17",
        "tag": "Homicidio",
        "sheet": {
            "indicators": [
                {
                    "indicator_name": "Clasificación",
                    "response": "** No se trata de un caso de homicidio, ya que la noticia no describe el asesinato de nadie."
                },
                {
                    "indicator_name": "Título",
                    "response": "** Algo que el Ministerio de Justicia o Bukele deberían explicar"
                },
                {
                    "indicator_name": "Resumen",
                    "response": "** La noticia habla de la captura de un máximo jefe de la organización terrorista Mara Salvatrucha en México y la falta de captura de los cabecillas principales y secundarios de los grupos criminales MS, Barrio 18 sureños o revolucionarios en el marco del régimen de Excepción."
                },
                {
                    "indicator_name": "Lugar de los Hechos",
                    "response": "** Arriaga, Chiapas, México"
                },
                {
                    "indicator_name": "Fuentes",
                    "response": "** No se indica en la noticia."
                },
                {
                    "indicator_name": "Temas",
                    "response": "** Seguridad, crimen, pandillas, Estado de Excepción"
                },
                {
                    "indicator_name": "Hechos Violatorios",
                    "response": "** No se indica en la noticia."
                },
                {
                    "indicator_name": "Hipótesis de Hechos",
                    "response": "** No se indica en la noticia."
                },
                {
                    "indicator_name": "Población Vulnerable",
                    "response": "** No se indica en la noticia."
                },
                {
                    "indicator_name": "Tipo de Arma",
                    "response": "** No se indica en la noticia."
                },
                {
                    "indicator_name": "Víctimas",
                    "response": "** No se indica en la noticia."
                },
                {
                    "indicator_name": "Victimario o Presunto Agresor",
                    "response": "N/A"
                }
            ],
            "id": "https://www.diariocolatino.com/algo-que-el-ministerio-de-justicia-o-bukele-deberian-explicar/",
            "priority": 4,
            "_id": "6670d7980eb47c223af309db"
        }
    },
    {
        "title": "Empresas eléctricas de El Salvador investigadas por «estafa agravada»",
        "text": "\n\nCompartir\n\n Facebook\n Twitter\n Google +\n\n\n\nPor Elder Gómez\n\nLas empresas eléctricas de El Salvador han comenzado a ser investigadas por la Fiscalía General de la República (FGR), por el delito de «estafa agravada», por realizar «cobros excesivos» a miles de usuarios, ha anunciado el presidente, Nayib Bukele.\n\n«Hemos encontrado cobros excesivos en los recibos de energía eléctrica, que van más allá del incremento del consumo de los hogares por la época calurosa», escribió el gobernante en sus redes sociales.\n\nEl mandatario detalló que las empresas eléctricas implicadas en el delito de «estafa agravada», son el consorcio energético AES -CAESS, CLESSA, DEUSEM y EEO-, además, la compañía eléctrica DelSur.\n\nBukele ha asegurado que las compañías eléctricas investigadas por la FGR, «no pueden justificar técnicamente» los exorbitantes incrementos en el suministro energético, de los que miles de salvadoreños habían pegado el grito en el cielo.\nAumentos al servicio eléctrico que superan, en muchos casos, hasta el 200 por ciento del monto original.\n\nEl mandatario reveló que, hasta ahora, «hemos identificado cientos de recibos…con cobros que no pueden ser justificados técnicamente».\n\n\nComparte esto:FacebookXMe gusta esto:Me gusta Cargando...\n\nRelacionado\n\n",
        "source": "diariocolatino.com",
        "url": "https://www.diariocolatino.com/empresas-electricas-de-el-salvador-investigadas-por-estafa-agravada/",
        "sheet_id": "https://www.diariocolatino.com/empresas-electricas-de-el-salvador-investigadas-por-estafa-agravada/",
        "date": "2024-06-15",
        "tag": "Homicidio",
        "sheet": {
            "indicators": [
                {
                    "indicator_name": "Clasificación",
                    "response": "** N/A"
                },
                {
                    "indicator_name": "Título",
                    "response": "** Empresas eléctricas de El Salvador investigadas por \"estafa agravada\""
                },
                {
                    "indicator_name": "Resumen",
                    "response": "** Las empresas eléctricas de El Salvador han comenzado a ser investigadas por la Fiscalía General de la República (FGR), por realizar \"cobros excesivos\" a miles de usuarios."
                },
                {
                    "indicator_name": "Lugar de los Hechos",
                    "response": "** No se especifica en la noticia."
                },
                {
                    "indicator_name": "Fuentes",
                    "response": "** No se especifica en la noticia."
                },
                {
                    "indicator_name": "Temas",
                    "response": "** Precio de la energía, estafa, explotación."
                },
                {
                    "indicator_name": "Hechos Violatorios",
                    "response": "** No se especifica en la noticia."
                },
                {
                    "indicator_name": "Hipótesis de Hechos",
                    "response": "** No se especifica en la noticia."
                },
                {
                    "indicator_name": "Población Vulnerable",
                    "response": "** No se especifica en la noticia."
                },
                {
                    "indicator_name": "Tipo de Arma",
                    "response": "** No se especifica en la noticia."
                },
                {
                    "indicator_name": "Víctimas",
                    "response": "** No se especifica en la noticia."
                },
                {
                    "indicator_name": "Victimario o Presunto Agresor",
                    "response": "N/A"
                }
            ],
            "id": "https://www.diariocolatino.com/empresas-electricas-de-el-salvador-investigadas-por-estafa-agravada/",
            "priority": 4,
            "_id": "6670d7a00eb47c223af309dc"
        }
    },
    {
        "title": "Policía nicaragüense entregó a miembro de mara MS13 a El Salvador",
        "text": "\n\nCompartir\n\n Facebook\n Twitter\n Google +\n\n\n\nManagua/Prensa Latina\nLa Policía nicaragüense informó hoy la entrega, a las autoridades de El Salvador, de un miembro de la mara (pandilla) salvatrucha MS13, con orden de captura por los delitos de organizaciones terroristas y homicidio agravado.\nA través de un comunicado, la institución policial precisó que el sujeto de nacionalidad salvadoreña y de nombre José Rogelio Misael Rubio, alias el teacher, fue capturado este martes a las 05:00, hora local, en el municipio El Viejo, del departamento de Chinandega (noreste).\nEl texto precisó que la entrega y se realizó en coordinación con la Oficina Central de la Organización Internacional de Policía Criminal (Interpol) para América Central con sede en San Salvador.\nLa Policía Nacional de Nicaragua reiteró su compromiso de continuar trabajando por la seguridad de las personas, familias y comunidades.\nLa MS13 es una organización criminal predatoria que vive fundamentalmente de la extorsión.\nSegún analistas, tras las históricas medidas de seguridad aplicadas por el gobierno del presidente Nayib Bukele, que llevaron a la cárcel a cerca de dos tercios de sus miembros, la pandilla sufrió un fuerte golpe.\nComparte esto:FacebookXMe gusta esto:Me gusta Cargando...\n\nRelacionado\n\n",
        "source": "diariocolatino.com",
        "url": "https://www.diariocolatino.com/policia-nicaraguense-entrego-a-miembro-de-mara-ms13-a-el-salvador/",
        "sheet_id": "https://www.diariocolatino.com/policia-nicaraguense-entrego-a-miembro-de-mara-ms13-a-el-salvador/",
        "date": "2024-06-12",
        "tag": "Homicidio",
        "sheet": {
            "indicators": [
                {
                    "indicator_name": "Clasificación",
                    "response": "** Homicidio"
                },
                {
                    "indicator_name": "Título",
                    "response": "** Policía nicaragüense entregó a miembro de mara MS13 a El Salvador"
                },
                {
                    "indicator_name": "Resumen",
                    "response": "** La policía nicaragüense informó la entrega de un miembro de la pandilla salvatrucha MS13 a las autoridades de El Salvador."
                },
                {
                    "indicator_name": "Lugar de los Hechos",
                    "response": "** El municipio El Viejo, del departamento de Chinandega (noreste)."
                },
                {
                    "indicator_name": "Fuentes",
                    "response": "** No se indicaron las fuentes de información."
                },
                {
                    "indicator_name": "Temas",
                    "response": "** Seguridad, pandilla, crimen."
                },
                {
                    "indicator_name": "Hechos Violatorios",
                    "response": "** No se especificaron los hechos violatorios."
                },
                {
                    "indicator_name": "Hipótesis de Hechos",
                    "response": "** No se planteó una hipótesis de hechos."
                },
                {
                    "indicator_name": "Población Vulnerable",
                    "response": "** No se identificó la población vulnerable."
                },
                {
                    "indicator_name": "Tipo de Arma",
                    "response": "** No se especificó el tipo de arma."
                },
                {
                    "indicator_name": "Víctimas",
                    "response": "** No se identificaron las víctimas."
                },
                {
                    "indicator_name": "Victimario o Presunto Agresor",
                    "response": "N/A"
                }
            ],
            "id": "https://www.diariocolatino.com/policia-nicaraguense-entrego-a-miembro-de-mara-ms13-a-el-salvador/",
            "priority": 4,
            "_id": "6670d7a90eb47c223af309dd"
        }
    },
    {
        "title": "No se encontró el título",
        "text": "\nAlessia Genoves Colaboradora @DiarioCoLatino La Asamblea Legislativa aprobó una nueva prórroga a la normativa que establece la emisión de subsidios y la fijación temporal de los precios del Gas Licuado del Petróleo (GLP). Se trata de la Ley Especial y Transitoria para la Estabilización de los Precios del GLP, contenida en el decreto 761, y que fue prorrogada en la …\nLeer artículo completo \n",
        "source": "diariocolatino.com",
        "url": "https://www.diariocolatino.com/category/nacionales/page/202/",
        "sheet_id": "https://www.diariocolatino.com/category/nacionales/page/202/",
        "date": "2024-01-25",
        "tag": "Homicidio",
        "sheet": {
            "indicators": [
                {
                    "indicator_name": "Clasificación",
                    "response": "N/A"
                },
                {
                    "indicator_name": "Título",
                    "response": "No se encontró el título"
                },
                {
                    "indicator_name": "Resumen",
                    "response": "N/A"
                },
                {
                    "indicator_name": "Lugar de los Hechos",
                    "response": "N/A"
                },
                {
                    "indicator_name": "Fuentes",
                    "response": "N/A"
                },
                {
                    "indicator_name": "Temas",
                    "response": "N/A"
                },
                {
                    "indicator_name": "Hechos Violatorios",
                    "response": "N/A"
                },
                {
                    "indicator_name": "Hipótesis de Hechos",
                    "response": "N/A"
                },
                {
                    "indicator_name": "Población Vulnerable",
                    "response": "N/A"
                },
                {
                    "indicator_name": "Tipo de Arma",
                    "response": "N/A"
                },
                {
                    "indicator_name": "Víctimas",
                    "response": "N/A"
                },
                {
                    "indicator_name": "Victimario o Presunto Agresor",
                    "response": "N/A"
                }
            ],
            "id": "https://www.diariocolatino.com/category/nacionales/page/202/",
            "priority": 4,
            "_id": "6670d7b00eb47c223af309de"
        }
    },
    {
        "title": "Juzgado condena a 45 años de prisión a un hombre por feminicidio",
        "text": "\n\nCompartir\n\n Facebook\n Twitter\n Google +\n\n\n\nRedacción Nacionales\n@DiarioCoLatino\nEl Juzgado Especializado de Sentencia para una Vida Libre de Violencia y Discriminación para las Mujeres, de San Salvador, condenó a 30 años de prisión a José Marcelino López López por el feminicidio simple de su esposa, quien era de 46 años, y a 15 años de prisión por el homicidio simple de Rufino Leiva.\nLa jueza dijo que se acreditó la participación del acusado en las dos muertes con la prueba testimonial, balística y documental.\nLos hechos por los cuales Marcelino López recibió la pena ocurrieron el 31 de octubre de 2022, en el Cantón La Vega, de Ilobasco, Cabañas, cuando cegado por los celos, atacó con arma de fuego a su esposa, que se encontraba en compañía del señor Rufino a quien también le disparó.\nEsto ocurrió mientras las dos víctimas se encontraban en un terreno rústico cercano a la vivienda del imputado y su esposa. Se detalla que la esposa falleció en el lugar a causa de los múltiples disparos y el hombre murió días después en un hospital.\nInstrucción contra motorista de una ambulancia por homicidio\nEn otro caso judicial, se ordenó institución formal para imputados señalados de homicidio culposo. El pasado 15 de febrero, un grave accidente vial en el kilómetro 4 del bulevar del Ejército Nacional resultó en la muerte de José Luis P. L., de 26 años, quien viajaba como pasajero en la motocicleta conducida por Fernando Dagoberto M.\nAl intentar ceder paso a una ambulancia del ISSS con la sirena encendida, la motocicleta colisionó contra un separador de cemento, causando la caída de la víctima y su posterior arrastre por la ambulancia.\nEl motorista de la ambulancia, Carlos Antonio C. B., enfrentará instrucción formal con la restricción de no abandonar el país, según lo decretado por el Juzgado Cuarto de Paz de Soyapango en una audiencia inicial.\nFernando Dagoberto, al no presentarse a la diligencia, también recibió instrucción formal. El caso será transferido a un juzgado de tránsito en San Salvador para esclarecer responsabilidades.\n \nLa autoridad judicial enfatizó la irresponsabilidad de manejar la ambulancia sin una emergencia vital, señalando que, aunque el paciente necesitaba atención, no había riesgo de vida inminente, sino que se dirigía a una curación.\nComparte esto:FacebookXMe gusta esto:Me gusta Cargando...\n\nRelacionado\n\n",
        "source": "diariocolatino.com",
        "url": "https://www.diariocolatino.com/juzgado-condena-a-45-anos-de-prision-a-un-hombre-por-feminicidio/",
        "sheet_id": "https://www.diariocolatino.com/juzgado-condena-a-45-anos-de-prision-a-un-hombre-por-feminicidio/",
        "date": "2024-05-21",
        "tag": "Homicidio",
        "sheet": {
            "indicators": [
                {
                    "indicator_name": "Clasificación",
                    "response": "** Homicidio"
                },
                {
                    "indicator_name": "Título",
                    "response": "** Juzgado condena a 45 años de prisión por feminicidio"
                },
                {
                    "indicator_name": "Resumen",
                    "response": "** El Juzgado Especializado de Sentencia para una Vida Libre de Violencia y Discriminación para las Mujeres, de San Salvador, condenó a 30 años de prisión a José Marcelino López López por el feminicidio simple de su esposa, quien era de 46 años, y a 15 años de prisión por el homicidio simple de Rufino Leiva."
                },
                {
                    "indicator_name": "Lugar de los Hechos",
                    "response": "** Cantón La Vega, de Ilobasco, Cabañas"
                },
                {
                    "indicator_name": "Fuentes",
                    "response": "** No se indica la fuente de información."
                },
                {
                    "indicator_name": "Temas",
                    "response": "** Violencia contra las mujeres, feminicidio, justicia."
                },
                {
                    "indicator_name": "Hechos Violatorios",
                    "response": "** El acusado cegado por los celos atacó con arma de fuego a su esposa, que se encontraba en compañía del señor Rufino."
                },
                {
                    "indicator_name": "Hipótesis de Hechos",
                    "response": "** No se presenta una hipótesis de hechos."
                },
                {
                    "indicator_name": "Población Vulnerable",
                    "response": "** No se indica la población vulnerable."
                },
                {
                    "indicator_name": "Tipo de Arma",
                    "response": "** Arma de fuego"
                },
                {
                    "indicator_name": "Víctimas",
                    "response": "** La esposa y el señor Rufino."
                },
                {
                    "indicator_name": "Victimario o Presunto Agresor",
                    "response": "N/A"
                }
            ],
            "id": "https://www.diariocolatino.com/juzgado-condena-a-45-anos-de-prision-a-un-hombre-por-feminicidio/",
            "priority": 4,
            "_id": "6670d7bb0eb47c223af309df"
        }
    },
    {
        "title": "No se encontró el título",
        "text": "\n@AlmaCoLatino El jefe de la División de Investigaciones de Accidentes de Tránsito de la Policía Nacional Civil (PNC) Otto Urrutia indicó que los conductores peligrosos y el exceso de velocidad son las principales causas de accidentes de tránsito en el país, sin embargo, del 30 de julio al 2 de agosto, se tiene reducción de fallecidos y lesionados. Urrutia dijo …\nLeer artículo completo \n",
        "source": "diariocolatino.com",
        "url": "https://www.diariocolatino.com/category/titular_principal/page/612/",
        "sheet_id": "https://www.diariocolatino.com/category/titular_principal/page/612/",
        "date": "2016-08-03",
        "tag": "Homicidio",
        "sheet": {
            "indicators": [
                {
                    "indicator_name": "Clasificacion",
                    "response": "La noticia no describe un homicidio, por lo que no se puede clasificar como una noticia de homicidio."
                },
                {
                    "indicator_name": "Titulo",
                    "response": "**Título de la noticia:** No se encontró el título\n\nEl texto no contiene el título de la noticia, por lo que no se pudo extraer la información requested."
                },
                {
                    "indicator_name": "Resumen",
                    "response": "**Resumen:**\n\nLa noticia informa sobre la aprobación de $152 millones en Títulos Valores por la Asamblea Legislativa salvadoreña. La aprobación ocurrió en medio de negociaciones entre la opositora ARENA y el FMLN. El Vicepresidente expresó su satisfacción por la aprobación, diciendo que es un día importante para el país."
                },
                {
                    "indicator_name": "Ubicacion del Suceso",
                    "response": "La noticia no indica el lugar donde ocurrió el suceso, por lo que no se puede proporcionar la información de donde ocurrió el suceso."
                },
                {
                    "indicator_name": "Fuentes",
                    "response": "La texto no contiene ninguna fuente de información, por lo que no se puede proporcionar la información sobre las fuentes de información de la noticia."
                },
                {
                    "indicator_name": "Temas",
                    "response": "Los temas principales tratados en la noticia son:\n\n* **La aprobación de $152 millones en Títulos Valores por la Asamblea Legislativa.**\n* **Las negociaciones entre la opositora ARENA y el FMLN sobre la contraloría.**\n* **La importancia de la aprobación para el gobierno salvadoreño.**"
                },
                {
                    "indicator_name": "Hechos Violativos",
                    "response": "La texto no contiene información sobre la violación a la ley, por lo que no se puede proporcionar la información requested."
                },
                {
                    "indicator_name": "Hipotesis de los Hechos",
                    "response": "**Teoría:**\n\nLa noticia no presenta una teoría o suposición, por lo que no se puede proporcionar la información solicitada."
                },
                {
                    "indicator_name": "Poblacion Vulnerable",
                    "response": "La texto no contiene información sobre los grupos en riesgo mencionados en la noticia, por lo que no se puede proporcionar la información solicitada."
                },
                {
                    "indicator_name": "Tipo de Arma",
                    "response": "La texto no describe armas, por lo que no se puede determinar si se menciona o no el tipo de arma en la noticia, por lo que no se puede proporcionar la información solicitada."
                },
                {
                    "indicator_name": "Victimas",
                    "response": "La noticia no contiene información sobre las víctimas, por lo que no se puede identificar la información de las víctimas."
                },
                {
                    "indicator_name": "Agresor o Sospechoso",
                    "response": "La noticia no indica el nombre del agresor, por lo que no se puede proporcionar la información requesteda."
                }
            ],
            "priority": 3,
            "id": "https://www.diariocolatino.com/category/titular_principal/page/612/"
        }
    },
    {
        "title": "No se encontró el título",
        "text": "\nCésar Méndez @poncesj Apostados junto a sus hijos y familiares, store los habitantes de la comunidad de El Espino colocaron pancartas de protesta en el bulevar cancillería. Entonaron la canción “casas de cartón” y de manera pacífica esperaban que les entregaran sus pertenencias y que se las sacaran a la calle para quedarse ahí durante todo el día y toda …\nLeer artículo completo \n",
        "source": "diariocolatino.com",
        "url": "https://www.diariocolatino.com/category/nacionales/page/5526/",
        "sheet_id": "https://www.diariocolatino.com/category/nacionales/page/5526/",
        "date": "2015-06-10",
        "tag": "Homicidio",
        "sheet": {
            "indicators": [
                {
                    "indicator_name": "Clasificación",
                    "response": "** No homicidio"
                },
                {
                    "indicator_name": "Título",
                    "response": "** No se encontró el título"
                },
                {
                    "indicator_name": "Resumen",
                    "response": "** No disponible"
                },
                {
                    "indicator_name": "Lugar de los Hechos",
                    "response": "** No disponible"
                },
                {
                    "indicator_name": "Fuentes",
                    "response": "** No disponibles"
                },
                {
                    "indicator_name": "Temas",
                    "response": "** No disponibles"
                },
                {
                    "indicator_name": "Hechos Violatorios",
                    "response": "** No disponibles"
                },
                {
                    "indicator_name": "Hipótesis de Hechos",
                    "response": "** No disponible"
                },
                {
                    "indicator_name": "Población Vulnerable",
                    "response": "** No disponible"
                },
                {
                    "indicator_name": "Tipo de Arma",
                    "response": "** No disponible"
                },
                {
                    "indicator_name": "Víctimas",
                    "response": "** No disponibles"
                },
                {
                    "indicator_name": "Victimario o Presunto Agresor",
                    "response": "N/A"
                }
            ],
            "id": "https://www.diariocolatino.com/category/nacionales/page/5526/",
            "priority": 4,
            "_id": "6670d7c10eb47c223af309e0"
        }
    },
    {
        "title": "No se encontró el título",
        "text": "\nOscar López @Oscar_DCL Veteranos de guerra de la Fuerza Armada de El Salvador (FAES) y el Frente Farabundo Martí para la Liberación Nacional (FMLN) coincidieron que con el actual Gobierno existen retrocesos en cuanto al cumplimiento los derechos y beneficios del sector. “Hemos retrocedido con la llegada de este presidente (Nayib Bukele), lo lamentamos, le decimos que no se equivoque …\nLeer artículo completo \n",
        "source": "diariocolatino.com",
        "url": "https://www.diariocolatino.com/category/nacionales/page/2426/",
        "sheet_id": "https://www.diariocolatino.com/category/nacionales/page/2426/",
        "date": "2020-02-03",
        "tag": "Homicidio",
        "sheet": {
            "indicators": [
                {
                    "indicator_name": "Clasificacion",
                    "response": "La noticia no describe un homicidio, por lo que no se puede determinar si la noticia describe un homicidio o no."
                },
                {
                    "indicator_name": "Titulo",
                    "response": "**Título de la noticia:** No se encontró el título\n\nLa noticia no contiene un título, por lo que no se pudo extraer el título solicitado."
                },
                {
                    "indicator_name": "Resumen",
                    "response": "**Resumen de la noticia:**\n\nLa noticia informa sobre la declaración de Carla de Varela, ministra de Educación, de que se preparará un plan de seguridad para los contornos de las escuelas. El plan se sumará al esfuerzo integrado en el plan Control Territorial que ha logrado reducir los principales índices de violencia del país.\n\nLa noticia no contiene el título de la noticia, el cual no se ha encontrado en el texto."
                },
                {
                    "indicator_name": "Ubicacion del Suceso",
                    "response": "La noticia no contiene información sobre el lugar donde ocurrió el suceso, por lo que no se puede proporcionar la información solicitada."
                },
                {
                    "indicator_name": "Fuentes",
                    "response": "La texto no contiene ninguna fuente de información, por lo que no se puede analizar la información de la cita de las fuentes de información."
                },
                {
                    "indicator_name": "Temas",
                    "response": "**Temas principales tratados en la noticia:**\n\n* **Inicio del año escolar:** El 20 de enero se inicia el año escolar.\n* **Plan de seguridad para las escuelas:** La ministra de Educación, Carla de Varela, anuncia que prepara un plan de seguridad para los contornos de las escuelas.\n* **Plan Control Territorial:** El plan Control Territorial ha logrado reducir los principales índices de violencia del país."
                },
                {
                    "indicator_name": "Hechos Violativos",
                    "response": "La texto no contiene información sobre la violación a la ley, por lo que no se puede proporcionar la información requested."
                },
                {
                    "indicator_name": "Hipotesis de los Hechos",
                    "response": "La información que se puede extraer de la noticia es que el gobierno mexicano está preparando un plan de seguridad para los contornos de las escuelas. La suposición que se presenta es que el objetivo de este plan es reducir la violencia en las escuelas."
                },
                {
                    "indicator_name": "Poblacion Vulnerable",
                    "response": "La texto no contiene información sobre los grupos en riesgo mencionados en la noticia, por lo que no se puede proporcionar la información requested."
                },
                {
                    "indicator_name": "Tipo de Arma",
                    "response": "La texto no contiene información sobre el tipo de arma que se menciona, por lo que no se puede determinar si se incluye la información sobre el tipo de arma en la noticia."
                },
                {
                    "indicator_name": "Victimas",
                    "response": "La texto no indica a las víctimas, por lo que no se puede identificar la información sobre las víctimas en la noticia."
                },
                {
                    "indicator_name": "Agresor o Sospechoso",
                    "response": "La texto no contiene información sobre el nombre del agresor, por lo que no se puede proporcionar la información requesteda."
                }
            ],
            "priority": 3,
            "id": "https://www.diariocolatino.com/category/nacionales/page/2426/"
        }
    },
    {
        "title": "No se encontró el título",
        "text": "\nAlma Vilches @AlmaCoLatino Representantes de organizaciones que conforman el Movimiento Salvadoreño de Solidaridad con Cuba, recordaron el 129 aniversario de la caída en combate del revolucionario cubano José Martí, quien la mañana del 19 de mayo de l895 fue abatido por las balas cuando participó en un encuentro entre tropas españolas y un pequeño contingente liderado por el general Máximo Gómez. …\nLeer artículo completo \n",
        "source": "diariocolatino.com",
        "url": "https://www.diariocolatino.com/category/nacionales/page/41/",
        "sheet_id": "https://www.diariocolatino.com/category/nacionales/page/41/",
        "date": "2024-05-20",
        "tag": "Homicidio",
        "sheet": {
            "indicators": [
                {
                    "indicator_name": "Clasificacion",
                    "response": "La noticia no describe un homicidio, por lo que no se puede determinar si la noticia describe un homicidio o no."
                },
                {
                    "indicator_name": "Titulo",
                    "response": "**Título de la noticia:** No se encontró el título. La noticia no tiene título."
                },
                {
                    "indicator_name": "Resumen",
                    "response": "**Resumen:**\n\nLa noticia informa sobre las esperadas lluvias sobre la franja costera y cordillera volcánica, con énfasis en la cordillera El Bálsamo, Apaneca-Ilamatepec y sus alrededores. Las lluvias se espera que continuen durante la tarde y se espera también lluvia y tormentas en la franja norte."
                },
                {
                    "indicator_name": "Ubicacion del Suceso",
                    "response": "La noticia habla de un evento que ocurrió en la cordillera El Bálsamo, Apaneca-Ilamatepec y la franja norte.\n\n**Dónde ocurrió el suceso:**\n\n* cordillera El Bálsamo\n* Apaneca-Ilamatepec\n* Franja norte"
                },
                {
                    "indicator_name": "Fuentes",
                    "response": "La texto no contiene información sobre las fuentes de información, por lo que no se puede proporcionar la información de las fuentes de información para la noticia."
                },
                {
                    "indicator_name": "Temas",
                    "response": "**Los temas principales tratados en la noticia:**\n\n* **Clima:** Previsión de lluvia sobre la franja costera y cordillera volcánica, con énfasis en la cordillera El Bálsamo, Apaneca-Ilamatepec y sus alrededores.\n* **Ocurrencia de lluvias:** Continuación de las lluvias sobre la cordillera El Bálsamo y Apaneca-Ilamatepec, y se espera más lluvia y tormentas en la franja norte."
                },
                {
                    "indicator_name": "Hechos Violativos",
                    "response": "La texto no contiene información sobre la violación a la ley, por lo que no se puede proporcionar la información requested."
                },
                {
                    "indicator_name": "Hipotesis de los Hechos",
                    "response": "La información que se deduce de la noticia es que las lluvias se espera que ocurran sobre la cordillera El Bálsamo y Apaneca-Ilamatepec, y también sobre la franja norte del país."
                },
                {
                    "indicator_name": "Poblacion Vulnerable",
                    "response": "La texto no indica los grupos en riesgo por lo que no se puede proporcionar la información de los grupos en riesgo mencionados en la noticia."
                },
                {
                    "indicator_name": "Tipo de Arma",
                    "response": "La texto no contiene ninguna información sobre armas, por lo que no se puede determinar el tipo de arma que se menciona en la noticia."
                },
                {
                    "indicator_name": "Victimas",
                    "response": "La texto no contiene información sobre las víctimas, por lo que no se puede identificar a las víctimas en la noticia."
                },
                {
                    "indicator_name": "Agresor o Sospechoso",
                    "response": "La texto no contiene información sobre el nombre del agresor, por lo que no se puede proporcionar la información solicitada."
                }
            ],
            "priority": 3,
            "id": "https://www.diariocolatino.com/category/nacionales/page/41/"
        }
    },
    {
        "title": "No se encontró el título",
        "text": "\nJoaquín Salazar @joakinSalazar El Director de Protección Civil y Secretario de Asuntos para la Vulnerabilidad, prescription Jorge Meléndez, order reiteró esta mañana que hasta el momento las vacaciones de Semana Santa han dejado al menos 20 fallecidos, sildenafil de los cuales 16 son por accidentes de tránsito y cuatro por inmersión. Para Jorge Meléndez expresó que la distracción del conductor …\nLeer artículo completo \n",
        "source": "diariocolatino.com",
        "url": "https://www.diariocolatino.com/category/nacionales/page/6283/",
        "sheet_id": "https://www.diariocolatino.com/category/nacionales/page/6283/",
        "date": "2014-04-20",
        "tag": "Homicidio",
        "sheet": {
            "indicators": [
                {
                    "indicator_name": "Clasificacion",
                    "response": "La noticia no describe un homicidio, por lo que no se puede clasificar como una noticia sobre un homicidio."
                },
                {
                    "indicator_name": "Titulo",
                    "response": "**Extraído el título de la noticia:**\n\nNo se encontró el título de la noticia."
                },
                {
                    "indicator_name": "Resumen",
                    "response": "**Resumen:**\n\nLa noticia informa sobre la resolución de la Sala de lo Constitucional de la CSJ que declaró improcedente el recurso de recuento de votos por voto que solicitaba el partido ARENA. El partido expresó su acatamiento de la resolución, afirmando que es una prueba de vocación democrática y pleno respeto a la institucionalidad de El Salvador.\n\n**Brevo resumen:**\n\nLa resolución de la Sala de lo Constitucional declaró improcedente el recurso de recuento de votos por voto solicitado por el partido ARENA. El partido reaccionó con acatamiento, enfatizando su compromiso con la democracia y el respeto a la institucionalidad."
                },
                {
                    "indicator_name": "Ubicacion del Suceso",
                    "response": "La noticia no indica el lugar donde ocurrió el suceso, por lo que no se puede proporcionar la información de donde ocurrió el suceso."
                },
                {
                    "indicator_name": "Fuentes",
                    "response": "La información no contiene citas de fuentes de información, por lo que no se puede proporcionar la información de las fuentes de información de la noticia."
                },
                {
                    "indicator_name": "Temas",
                    "response": "**Temas principales tratados en la noticia:**\n\n* **Recounto voto por voto:** La resolución de la Sala de lo Constitucional de la CSJ que declaró improcedente el recurso de cuenta voto por voto de la Alianza Republicana Nacionalista (ARENA)\n* **Voación democrática:** El partido ARENA creía que la resolución es una prueba de vocación democrática y pleno respeto a la institucionalidad de El Salvador.\n* **Institutionalidad:** La importancia de la resolución para la institucionalidad de El Salvador.\n* **Legitimidad:** La necesidad de mantener la legitimidad de las instituciones salvadorianas."
                },
                {
                    "indicator_name": "Hechos Violativos",
                    "response": "La texto no contiene información sobre la violación a la ley, por lo que no se puede proporcionar la información requested."
                },
                {
                    "indicator_name": "Hipotesis de los Hechos",
                    "response": "**Teoría:**\n\nLa noticia no contiene información sobre la teoría o suposición que se presenta, por lo que no se puede proporcionar la información solicitada."
                },
                {
                    "indicator_name": "Poblacion Vulnerable",
                    "response": "La texto no contiene información sobre los grupos en riesgo que se menciona en la noticia, por lo que no se puede proporcionar la información requested."
                },
                {
                    "indicator_name": "Tipo de Arma",
                    "response": "La texto no contiene información sobre armas, por lo que no se puede proporcionar la información de tipo de arma que se solicita."
                },
                {
                    "indicator_name": "Victimas",
                    "response": "La noticia no contiene información sobre las víctimas, por lo que no se puede proporcionar la información solicitada."
                },
                {
                    "indicator_name": "Agresor o Sospechoso",
                    "response": "La texto no indica el nombre del agresor, por lo que no se puede proporcionar la información de nombre del agresor."
                }
            ],
            "priority": 3,
            "id": "https://www.diariocolatino.com/category/nacionales/page/6283/"
        }
    },
    {
        "title": "Encuentran dos cadáveres, uno en río Acelhuate y otro en una hacienda",
        "text": "\n        La sección San Salvador Norte de Comandos de Salvamento informó este domingo de la recuperación de un cadáver del río Acelhuate, jurisdicción de la Comunidad El Trapiche, en el distrito de Guazapa, en San Salvador. \rComandos de Salvamento informó que asistieron porque los habitantes reportaron “un cuerpo en medio del río Acelhuate”. \r“Llegamos al lugar y, por la zona que había quedado el cuerpo de difícil acceso, se aseguró la escena, para guardar la integridad física de nuestros socorristas y así procedieran a hacer la recuperación del mismo y entregarlo a las autoridades pertinentes”, informó Comandos de Salvamento. \rSe desconoce la identidad de la víctima y las posibles causas de su muerte. \rTambién, Comandos de Salvamento informó que ayer fue encontrado un segundo cadáver en estado de putrefacción en la Hacienda Los Mangos, en el distrito de Aguilares, al norte del departamento de San Salvador. Se maneja la versión preliminar que fue identificado como Douglas Ernesto Brito Mayorga, de 47 años. La primera hipótesis es que hace varios días se había quitado la vida, pero se desconoce de forma oficial la causa de su muerte. “Por el lugar donde se encontraba se necesitaban técnicas para recuperar su cuerpo\", informaron los cuerpos de socorro. \rLa Policía Nacional Civil (PNC) ha reportado en redes sociales que no hubo ningún homicidio a nivel nacional en los últimos dos días. En su cuenta tampoco ha reportado la aparición de estos dos cadáveres.  \n\n\n\n\n\nOtro cuerpo de un hombre no identificado fue encontrado, en estado de descomposición, en una hacienda, en Guazapa. / Comandos.\n\n\n\n\n\n\n",
        "source": "diario.elmundo.sv",
        "url": "https://diario.elmundo.sv/nacionales/encuentran-dos-cadaveres-uno-en-rio-acelhuate-y-otro-en-una-hacienda",
        "sheet_id": "https://diario.elmundo.sv/nacionales/encuentran-dos-cadaveres-uno-en-rio-acelhuate-y-otro-en-una-hacienda",
        "date": "2024-06-16",
        "tag": "Homicidio",
        "sheet": {
            "indicators": [
                {
                    "indicator_name": "Clasificación",
                    "response": "** Homicidio"
                },
                {
                    "indicator_name": "Título",
                    "response": "** Encuentran dos cadáveres, uno en río Acelhuate y otro en una hacienda"
                },
                {
                    "indicator_name": "Resumen",
                    "response": "** La sección San Salvador Norte de Comandos de Salvamento informó de la recuperación de un cadáver en el río Acelhuate y otro en una hacienda."
                },
                {
                    "indicator_name": "Lugar de los Hechos",
                    "response": "** Guazapa, San Salvador."
                },
                {
                    "indicator_name": "Fuentes",
                    "response": "** No se indica la fuente de información."
                },
                {
                    "indicator_name": "Temas",
                    "response": "** Seguridad pública, crimen, víctima."
                },
                {
                    "indicator_name": "Hechos Violatorios",
                    "response": "** No se specifies los hechos violatorios."
                },
                {
                    "indicator_name": "Hipótesis de Hechos",
                    "response": "** No se presenta una hipótesis de hechos."
                },
                {
                    "indicator_name": "Población Vulnerable",
                    "response": "** No se menciona la población vulnerable."
                },
                {
                    "indicator_name": "Tipo de Arma",
                    "response": "** No se especifica el tipo de arma."
                },
                {
                    "indicator_name": "Víctimas",
                    "response": "** No se identifica la víctima."
                },
                {
                    "indicator_name": "Victimario o Presunto Agresor",
                    "response": "N/A"
                }
            ],
            "id": "https://diario.elmundo.sv/nacionales/encuentran-dos-cadaveres-uno-en-rio-acelhuate-y-otro-en-una-hacienda",
            "priority": 4,
            "_id": "6670d7cb0eb47c223af309e1"
        }
    },
    {
        "title": "Capturan a 16 personas que tenían 270 puntos de venta de droga en San Miguel",
        "text": "\n        La Fiscalía General de la República (FGR) informó de la captura de 16 personas pertenecientes a dos estructuras dedicadas a la venta de drogas marihuana y cocaína en San Miguel. \rLa Fiscalía sostiene que entre junio del 2023 y mayo del 2024 tenían 270 puntos de venta a nivel departamental. \r“16 sujetos que pertenecían a dos diferentes estructuras dedicadas al narcotráfico permanecerán en detención mientras el proceso en su contra avanza a la siguiente fase”, informó la Fiscalía. \rA todos se les procesa por un caso de proposición y conspiración para cometer el delito de homicidio agravado, 95 casos de actos preparatorios, proposición, conspiración y asociaciones delictivas. \rTambién se les imputa 6 casos de tráfico ilícito de droga y del delito de agrupaciones ilícitas. \rTodos permanecen detenidos desde mayo de este año, y según la Fiscalía cuando fueron capturados se les incautó dinero en efectivo, y porciones pequeñas y medianas de droga.  \n\n\n\n\n\n\n\n  \n\n\n\n\n\nUno de los capturados señalados de pertenecer a estructuras de venta de drogas en San Miguel.\n\n  \n\n\n\n\n\nParte de los decomisos a los capturados en San Miguel.\n\n\n\n\n\n\n",
        "source": "diario.elmundo.sv",
        "url": "https://diario.elmundo.sv/nacionales/capturan-a-16-personas-que-tenian-270-puntos-de-venta-de-droga-en-san-miguel",
        "sheet_id": "https://diario.elmundo.sv/nacionales/capturan-a-16-personas-que-tenian-270-puntos-de-venta-de-droga-en-san-miguel",
        "date": "2024-06-15",
        "tag": "Homicidio",
        "sheet": {
            "indicators": [
                {
                    "indicator_name": "Clasificación",
                    "response": "** No se trata de un caso de homicidio. La noticia describe la captura de individuos involucrados en la venta de drogas, no un crimen de homicidio."
                },
                {
                    "indicator_name": "Título",
                    "response": "** Capturan a 16 personas que tenían 270 puntos de venta de droga en San Miguel"
                },
                {
                    "indicator_name": "Resumen",
                    "response": "** La Fiscalía General de la República (FGR) informó de la captura de 16 personas que pertenecían a dos estructuras dedicadas a la venta de drogas marihuana y cocaína en San Miguel."
                },
                {
                    "indicator_name": "Lugar de los Hechos",
                    "response": "** San Miguel"
                },
                {
                    "indicator_name": "Fuentes",
                    "response": "** No se indica la fuente de información."
                },
                {
                    "indicator_name": "Temas",
                    "response": "** Venta de drogas, crimen organizado."
                },
                {
                    "indicator_name": "Hechos Violatorios",
                    "response": "** No se indica."
                },
                {
                    "indicator_name": "Hipótesis de Hechos",
                    "response": "** No se presenta."
                },
                {
                    "indicator_name": "Población Vulnerable",
                    "response": "** No se menciona."
                },
                {
                    "indicator_name": "Tipo de Arma",
                    "response": "** No se indica."
                },
                {
                    "indicator_name": "Víctimas",
                    "response": "** No se identifica."
                },
                {
                    "indicator_name": "Victimario o Presunto Agresor",
                    "response": "N/A"
                }
            ],
            "id": "https://diario.elmundo.sv/nacionales/capturan-a-16-personas-que-tenian-270-puntos-de-venta-de-droga-en-san-miguel",
            "priority": 4,
            "_id": "6670d7d50eb47c223af309e2"
        }
    },
    {
        "title": "La ministra argentina Patricia Bullrich viaja a El Salvador para reunirse con Bukele y visitar el CECOT",
        "text": "\n        La excandidata presidencial y ahora ministra de Seguridad de Argentina, Patricia Bullrich, viajará esta noche a El Salvador para reunirse con el presidente salvadoreño Nayib Bukele y visitar mañana domingo al Centro de Confinamiento del Terrorismo (CECOT), ubicada en el distrito de Tecoluca, San Vicente Sur. \rLa funcionaria argentina busca interiorizarse de las estrategias tomadas por el gobierno de El Salvador que hicieron que bajaran los índices de violencia, según el comunicado del Ministerio de Seguridad de Argentina.  \"La ministra está interesada en toda la estructura que permitió bajar drásticamente el delito en El Salvador que hasta hace no mucho tiempo fue un país dominado por la violencia de las maras. De ser el país más violento del mundo y tener 145 homicidios cada 100 mil habitantes, pasó a tener 2 cada 100 mil\", indica el comunicado oficial del Ministerio argentino de Seguridad y que busca enfocar una estrategia en la ciudad argentina de Rosario, Santa Fe. \rEl domingo, tiene previsto recorrer el CECOT, considerada la cárcel más grande de América con capacidad para 40,000 presos. \rSu agenda reuniones con los ministros de Defensa Nacional, Francis Merino Monroy, y de Seguridad, Gustavo Villatoro, una visita a la Dirección General Centros Penales y de Inteligencia, \"con el fin de intercambiar información con funcionarios de dichas áreas\"; así mismo, con el director de la Policía Nacional Civil (PNC), Mauricio Arriaza Chicas, y el fiscal general, Rodolfo Delgado. \rBullrich será recibida la noche del sábado por el embajador de Argentina en El Salvador, Sergio Luis Iaciuk. Además, visitará la Academia Nacional de Seguridad Pública (ANSP) donde mantendrá un encuentro con el director César Flores Murillo.  Le recomendamos: Las conversaciones entre Javier Milei y Nayib Bukele\n\n\n\n\n",
        "source": "diario.elmundo.sv",
        "url": "https://diario.elmundo.sv/politica/patricia-bullrich-viaja-a-el-salvador-para-reunirse-con-bukele-y-visitar-el-cecot",
        "sheet_id": "https://diario.elmundo.sv/politica/patricia-bullrich-viaja-a-el-salvador-para-reunirse-con-bukele-y-visitar-el-cecot",
        "date": "2024-06-15",
        "tag": "Homicidio",
        "sheet": {
            "indicators": [
                {
                    "indicator_name": "Clasificación",
                    "response": "** No es un caso de homicidio. La noticia describe la visita de la ministra argentina Patricia Bullrich a El Salvador para reunirse con el presidente Nayib Bukele y visitar el Centro de Confinamiento del Terrorismo (CECOT)."
                },
                {
                    "indicator_name": "Título",
                    "response": "** La ministra argentina Patricia Bullrich viaja a El Salvador para reunirse con Bukele y visitar el CECOT"
                },
                {
                    "indicator_name": "Resumen",
                    "response": "** La funcionaria argentina busca interiorizarse de las estrategias tomadas por el gobierno de El Salvador que hicieron que bajaran los índices de violencia."
                },
                {
                    "indicator_name": "Lugar de los Hechos",
                    "response": "** El Salvador"
                },
                {
                    "indicator_name": "Fuentes",
                    "response": "** No se especifica en la noticia."
                },
                {
                    "indicator_name": "Temas",
                    "response": "** subjación, estrategia contra la violencia."
                },
                {
                    "indicator_name": "Hechos Violatorios",
                    "response": "** No se especifica en la noticia."
                },
                {
                    "indicator_name": "Hipótesis de Hechos",
                    "response": "** No se especifica en la noticia."
                },
                {
                    "indicator_name": "Población Vulnerable",
                    "response": "** No se especifica en la noticia."
                },
                {
                    "indicator_name": "Tipo de Arma",
                    "response": "** No se especifica en la noticia."
                },
                {
                    "indicator_name": "Víctimas",
                    "response": "** No se especifica en la noticia."
                },
                {
                    "indicator_name": "Victimario o Presunto Agresor",
                    "response": "N/A"
                }
            ],
            "id": "https://diario.elmundo.sv/politica/patricia-bullrich-viaja-a-el-salvador-para-reunirse-con-bukele-y-visitar-el-cecot",
            "priority": 4,
            "_id": "6670d7de0eb47c223af309e3"
        }
    },
    {
        "title": "Policía nicaragüense captura y entrega a exconcejal de Conchagua señalado de ser miembro de la MS-13",
        "text": "\n        A través de un comunicado, la Policía Nacional de Nicaragua informó este martes de la captura y entrega a El Salvador de José Rogelio Misael Perla Rubio, un exconcejal de la alcaldía de Conchagua, por el partido de Arena, señalado de ser miembro de la Mara Salvatrucha (MS-13). \rEn el comunicado dicen que la captura se realizó cuando una patrulla realizaba labores de vigilancia en el municipio de El Viejo, en el departamento de Chinandega.  La Policía de Nicaragua lo perfila como miembro de la Mara Salvatrucha, con el alias \"Teacher\", y con orden de captura por los delitos de organizaciones terroristas y homicidio agravado.  \"En coordinación con la oficina Central de Interpol para América Central, con sede en San Salvador, entregó a las autoridades de la Policía Nacional Civil de El Salvador al sujeto de nacionalidad salvadoreña José Rogelio Misael Rubio, alias \"El Teacher\", miembro de la Mara MS-13\". Comunicado de prensa de la PNC de Nicaragua sobre la extradición. \rLa Policía nicaragüense dijo que \"reitera su compromiso en continuar trabajando por la seguridad de las personas, familias y comunidades\". \rRubio Perla fue el cuarto regidor propietario por el partido Arena, en la alcaldía de Conchagua, en La Unión, en el periodo del 2018 al 2021, en la gestión de Jesús Abelino Medina Flores, quien actualmente también está detenido por delitos de corrupción en su gestión.  Capturado en El Salvador y liberado sin razón \rEn agosto del 2019, José Rogelio Misael Perla Rubio fue capturado por la Policía Nacional Civil (PNC) junto con 23 personas acusadas de cometer delitos en Conchagua como organizaciones terroristas, 12 casos de homicidios agravados, 15 casos de extorsión, robo, y hurto. \rSu captura fue ejecutada por miembros de la División de Investigación Criminal Transnacional (DICT), de la Unidad de Investigaciones de la PNC y de la Fiscalía General de la República (FGR). Se desconoce porque fue liberado.    \n\n\n\n\n",
        "source": "diario.elmundo.sv",
        "url": "https://diario.elmundo.sv/nacionales/policia-nicaraguense-captura-y-entrega-a-exconcejal-de-conchagua-senalado-de-ser-miembro-de-la-ms-13",
        "sheet_id": "https://diario.elmundo.sv/nacionales/policia-nicaraguense-captura-y-entrega-a-exconcejal-de-conchagua-senalado-de-ser-miembro-de-la-ms-13",
        "date": "2024-06-12",
        "tag": "Homicidio",
        "sheet": {
            "indicators": [
                {
                    "indicator_name": "Clasificación",
                    "response": "** Homicidio"
                },
                {
                    "indicator_name": "Título",
                    "response": "** Policía nicaragüense captura y entrega a exconcejal de Conchagua acusado de ser miembro de la MS-13"
                },
                {
                    "indicator_name": "Resumen",
                    "response": "** La policía nicaragüense capturó y entregó a El Salvador a un exconcejal de la alcaldía de Conchagua por el partido de Arena, acusado de ser miembro de la Mara Salvatrucha (MS-13)."
                },
                {
                    "indicator_name": "Lugar de los Hechos",
                    "response": "** El municipio de El Viejo, en el departamento de Chinandega."
                },
                {
                    "indicator_name": "Fuentes",
                    "response": "** No se indica la fuente de información."
                },
                {
                    "indicator_name": "Temas",
                    "response": "** Seguridad, crimen, Membersía de una organización criminal."
                },
                {
                    "indicator_name": "Hechos Violatorios",
                    "response": "** No se especifica ningún hecho violatorio."
                },
                {
                    "indicator_name": "Hipótesis de Hechos",
                    "response": "** No se presenta ninguna hipótesis de hechos."
                },
                {
                    "indicator_name": "Población Vulnerable",
                    "response": "** No se menciona población vulnerable."
                },
                {
                    "indicator_name": "Tipo de Arma",
                    "response": "** No se especifica el tipo de arma."
                },
                {
                    "indicator_name": "Víctimas",
                    "response": "** No se identifican las víctimas."
                },
                {
                    "indicator_name": "Victimario o Presunto Agresor",
                    "response": "N/A"
                }
            ],
            "id": "https://diario.elmundo.sv/nacionales/policia-nicaraguense-captura-y-entrega-a-exconcejal-de-conchagua-senalado-de-ser-miembro-de-la-ms-13",
            "priority": 4,
            "_id": "6670d7e90eb47c223af309e4"
        }
    },
    {
        "title": "El cabecilla MS-13 \"El Greñas\" fue capturado en Estados Unidos",
        "text": "\n        El Departamento de Justicia de Estados Unidos informó sobre la captura del cabecilla de la Mara Salvatrucha, César Humberto López Larios, alias \"El Greñas de Stoner\", quien fue acusado en una corte de Nueva York por cargos de terrorismo, junto con la ranfla nacional de la MS-13. \rEn una nota de prensa, el Departamento de Justicia explica que López Larios fue detenido el pasado 9 de junio en el aeropuerto de Houston, Texas, a su arribo; medios de comunicación han informado que el pandillero fue detenido inicialmente en México por la Fiscalía de Chiapas, pero fue capturado por el la Oficina Federal de Investigaciones (FBI) e Investigaciones de Seguridad Nacional (HSI) en un vuelo de repatriación. \r\"Específicamente, López-Larios está acusado de conspiración para proporcionar y ocultar apoyo material a los terroristas, conspiración para cometer actos de terrorismo que trascienden las fronteras nacionales, conspiración para financiar el terrorismo y conspiración de narcoterrorismo\", explica el departamento de Justicia. \"El Greñas\" será transferido al distrito Este de Nueva York en los próximos días. \r\"El arresto de López-Larios, que es uno de los líderes más altos de la EM-13 en el mundo, es un logro significativo para la aplicación de la ley y otro paso crucial en el desmantelamiento de esta empresa criminal internacional\", sostuvo el fiscal de los Estados Unidos para el Distrito Este de Nueva York. \r\"El Greñas\" se había mantenido prófugo y el FBI ofrecía una recompensa de $10,000 por información que condujera a su arresto. Un aviso publicado en español por el FBI señalaba que \"ordenó la comisión de numerosos actos violentos contra civiles, miembros de pandillas rivales, al igual que actividades para distribuir narcóticos y conspiraciones para llevar a cabo extorsiones a nivel mundial\". \rLa detención de López Larios se une a la de Elmer Canales Rivera, alias \"El Crook\", quien fue detenido en noviembre del año pasado también en México y luego llevado a Estados Unidos.\r¿Quién es el \"Crook\"?\rCanales Rivera es uno de los 12 cabecillas de la Mara Salvatrucha, de origen salvadoreño, que conformaron la ranfla nacional, el alto mando de la temida pandilla que causó terror en las últimas décadas en El Salvador. \"Crook\", de 47 años de edad, guardaba arresto tras una condena de 10 años de cárcel por proposición y conspiración por homicidio agravado y otros 30 años por homicidio agravado. Según los expedientes judiciales a los que periodistas tuvieron acceso, guardaba arresto desde el año 2000, y su pena aún no había terminado. \rInvestigaciones periodísticas revelaron que Canales fue sacado del penal de máxima seguridad en Zacatecoluca, departamento de La Paz, donde purgaba su pena de prisión. Tenía un proceso pendiente por extorsión y agrupaciones ilícitas. \rEn julio del año pasado, El Faro reveló audios donde el director de Reconstrucción de Tejido Social, Carlos Marroquín, decía que él mismo sacó al \"Crook\" del país, vía Guatemala. Posteriormente, el mismo periódico digital documentó una presunta huida del pandillero, gracias a las fotografías y videos que su pareja sentimental publicaba en redes sociales, entre noviembre de 2021 y diciembre de 2022. El material multimedia permitió identificar que la pareja estuvo en unos apartamentos de la colonia Escalón, en San Salvador, y luego en Guatemala, concluye el reportaje. \rPosterior a esas revelaciones, el Gobierno de Estados Unidos también habría preguntado, a través de la nota diplomática No. 2021-511, a la Corte Suprema de Justicia cuál era la situación jurídica de Canales Rivera en el país, y si éste había sido liberado, bajo qué circunstancias había ocurrido, debido a que \"Crook\" tenía una solicitud de extradición de Estados Unidos en El Salvador y también, una orden de captura de la Policía Internacional, Interpol.\rLos acusados \rEn enero del año 2021, la Fiscalía de Nueva York acusó a 14 pandilleros salvadoreños por una camándula de delitos ligados al terrorismo, todos perfilados como miembros de la ranfla nacional. \rEntre los acusados figuran:\r Borromeo Enrique Henríquez, alias “Diablito de Hollywood”, quien ya guarda prisión, es reconocido como el “miembro más poderoso de la “Ranfla Nacional”, la cúpula de dirigentes de la pandilla. Fredy Iván Jandres Parada, alias “Lucky de Park View”; César Humberto López Larios, alias “El Greñas de Stoners”; Hugo Armando Quinteros Mineros, alias “Flaco de Francis”. Arístides Dionisio Umanzor \"Sirra de Teclas\" Eduardo Erazo Nolasco, \"Colocho o Mustage de Western\" Elmer Rivera Canales \"El Crook\" José Luis Mendoza, \"Pavas de 7/11\" Leonel Alexander González, \"El Necio de San Cocos\" Saúl Antonio Turcios, \"Trece de Teclas\" Efraín Cortez \"Tigre de Park View\" Ricardo Alberto Díaz, \"Rata de Leewards\". Edson Sachary Eufemia, \"Speedy de Park View\" José Fernandez Flores, \"Cola de Western\". \n\n\n\n\n",
        "source": "diario.elmundo.sv",
        "url": "https://diario.elmundo.sv/nacionales/el-cabecilla-ms-13-el-grenas-fue-capturado-en-estados-unidos",
        "sheet_id": "https://diario.elmundo.sv/nacionales/el-cabecilla-ms-13-el-grenas-fue-capturado-en-estados-unidos",
        "date": "2024-06-11",
        "tag": "Homicidio",
        "sheet": {
            "indicators": [
                {
                    "indicator_name": "Clasificación",
                    "response": "**"
                },
                {
                    "indicator_name": "Título",
                    "response": "** El cabecilla MS-13 \"El Greñas\" fue capturado en Estados Unidos"
                },
                {
                    "indicator_name": "Resumen",
                    "response": "** El Departamento de Justicia de Estados Unidos informó sobre la captura del cabecilla de la Mara Salvatrucha, César Humberto López Larios, alias \"El Greñas de Stoner\"."
                },
                {
                    "indicator_name": "Lugar de los Hechos",
                    "response": "** No se especifica en la noticia."
                },
                {
                    "indicator_name": "Fuentes",
                    "response": "** No se especifica en la noticia."
                },
                {
                    "indicator_name": "Temas",
                    "response": "**"
                },
                {
                    "indicator_name": "Hechos Violatorios",
                    "response": "**"
                },
                {
                    "indicator_name": "Hipótesis de Hechos",
                    "response": "**"
                },
                {
                    "indicator_name": "Población Vulnerable",
                    "response": "**"
                },
                {
                    "indicator_name": "Tipo de Arma",
                    "response": "**"
                },
                {
                    "indicator_name": "Víctimas",
                    "response": "**"
                },
                {
                    "indicator_name": "Victimario o Presunto Agresor",
                    "response": "**"
                }
            ],
            "id": "https://diario.elmundo.sv/nacionales/el-cabecilla-ms-13-el-grenas-fue-capturado-en-estados-unidos",
            "priority": 4,
            "_id": "6670d7f50eb47c223af309e5"
        }
    },
    {
        "title": "EEUU repatria a salvadoreño buscado por homicidio agravado y agrupaciones ilícitas",
        "text": "\n        La oficina de Operaciones de Aplicaciones y Remoción de Houston (ICE), de Estados Unidos, confirmó este martes la repatriación de un fugitivo salvadoreño, identificado como Ismael Adonay Aguilar Cornejo, quien era buscado por las autoridades por los delitos de homicidio agravado y agrupaciones ilícitas. \rLa repatriación, realizada el 24 de mayo pasado, contó con la asistencia de ERO El Salvador y la Fuerza de Tareas de la Alianza para la Aplicación de Fugitivos (SAFE). \rLa ICE detalló que Aguilar, de 31 años, fue trasladado desde Alejandría, Luisiana, en un vuelo chárter hacia el Aeropuerto Internacional de El Salvador, donde fue recibido por los agentes de la Policía Nacional Civil (PNC). \rSegún la investigación policial, Aguilar ingresó de manera irregular a Estados Unidos, en una fecha y un lugar desconocido. El salvadoreño fue detenido el 11 de septiembre de 2012 por la Patrulla Fronteriza, cerca de Hidalgo, y dos días después se entregó a la custodia de la ICE. \rEl 30 de noviembre de ese año quedó en libertad con orden de reconocimiento a la espera de la resolución de un proceso migratorio; sin embargo, no compareció ante las autoridades y se fugó de las autoridades. El 5 de febrero de 2014, un juez de inmigración ordenó al Departamento de Justicia su deportación. \rNueve años después, el 8 de octubre de 2023, los oficiales de ERO Huston localizaron y arrestaron a Aguilar en el suroeste de Houston. Tras su detención, las autoridades estadounidenses confirmaron a con sus homólogos salvadoreños que era buscado en El Salvador por homicidio agravado y agrupaciones ilícitas. \rAguilar presentó una moción para reabrir su caso migratorio en noviembre, pero fue denegada en diciembre. Luego, apeló la decisión al juez de inmigración ante la Junta de Apelaciones de Inmigración en enero de 2024, quien desestimó la petición. \rBret A. Bradford, director de ERO Houston, señaló que Estados Unidos no será un “refugio seguro para fugitivos extranjeros, criminales violentos y pandilleros transnacionales que buscan evadir el procesamiento por crímenes que supuestamente cometieron en otro país”.\n                \n\n\n\n",
        "source": "diario.elmundo.sv",
        "url": "https://diario.elmundo.sv/nacionales/eeuu-repatria-a-salvadoreno-buscado-por-homicidio-agravado-y-agrupaciones-ilicitas",
        "sheet_id": "https://diario.elmundo.sv/nacionales/eeuu-repatria-a-salvadoreno-buscado-por-homicidio-agravado-y-agrupaciones-ilicitas",
        "date": "2024-05-28",
        "tag": "Homicidio",
        "sheet": {
            "indicators": [
                {
                    "indicator_name": "Clasificación",
                    "response": "** Homicidio"
                },
                {
                    "indicator_name": "Título",
                    "response": "** EEU repatria a salvadoreño buscado por homicidio agravado y agrupaciones ilícitas"
                },
                {
                    "indicator_name": "Resumen",
                    "response": "** La oficina de Operaciones de Aplicaciones y Remoción de Houston (ICE) de Estados Unidos confirma la repatriación de un fugitivo salvadoreño identificado como Ismael Adonay Aguilar Cornejo, buscado por los delitos de homicidio agravado y agrupaciones ilícitas."
                },
                {
                    "indicator_name": "Lugar de los Hechos",
                    "response": "** Alejandría, Luisiana, Estados Unidos"
                },
                {
                    "indicator_name": "Fuentes",
                    "response": "** No se especifica en la noticia."
                },
                {
                    "indicator_name": "Temas",
                    "response": "** Seguridad nacional, inmigración, violación de la ley"
                },
                {
                    "indicator_name": "Hechos Violatorios",
                    "response": "** Ingreso irregular a Estados Unidos, detención por la Patrulla Fronteriza, liberación con orden de reconocimiento, fuga, orden de deportación."
                },
                {
                    "indicator_name": "Hipótesis de Hechos",
                    "response": "** No se especifica en la noticia."
                },
                {
                    "indicator_name": "Población Vulnerable",
                    "response": "** No se especifica en la noticia."
                },
                {
                    "indicator_name": "Tipo de Arma",
                    "response": "** No se especifica en la noticia."
                },
                {
                    "indicator_name": "Víctimas",
                    "response": "** No se especifica en la noticia."
                },
                {
                    "indicator_name": "Victimario o Presunto Agresor",
                    "response": "N/A"
                }
            ],
            "id": "https://diario.elmundo.sv/nacionales/eeuu-repatria-a-salvadoreno-buscado-por-homicidio-agravado-y-agrupaciones-ilicitas",
            "priority": 4,
            "_id": "6670d7ff0eb47c223af309e6"
        }
    },
    {
        "title": "Capturan a dos supuestos responsables de homicidio en San Miguel",
        "text": "\n        La Policía Nacional Civil (PNC) capturó a José Fermín Iraheta Martínez, alias “Mancho”, y Óscar Alberto Bonilla Martínez, ambos señalados de cometer un homicidio en el cantón Hato Nuevo, de San Miguel. \rEl ministro de Justicia y Seguridad, Gustavo Villatoro, informó la noche del sábado que Iraheta Martínez se escondía en una casa abandonada en una zona boscosa del mismo cantón y que Bonilla Martínez se encontraba en un predio baldío a un kilómetro de distancia de la escena del crimen. \r\"Ambos asesinaron a la víctima con arma blanca, luego intentaron quemar su cuerpo\", aseveró el ministro. \rVillatoro también arremetió contra las organizaciones de la sociedad civil, señalando que \"el Estado capaz de hacer justicia es el que les incomoda a esos perversos vestidos de ONG u organizaciones de la sociedad civil\" porque \"les aleja de las migajas que recibían para hacer de la violencia homicida su fuente de ingreso\". \"Pero no vamos a permitir más impunidad para ningún asesino\", expresó el funcionario. \rAl mediodía del sábado, la PNC informó desde su cuenta X, en donde se divulgan las cifras de homicidios en El Salvador, que el viernes 17 de mayo finalizó con un homicidio y que el crimen ocurrido en San Miguel ya se había resuelto con \"la captura del responsable\". Desde el 1 de mayo, se han cometido 11 homicidios según las cifras policiales publicadas en X.  \n\n\n\n\n\nÓscar Alberto Bonilla Martínez se encontraba en un predio baldío, informó el ministro Villatoro.\n\n\n\n\n\n\n",
        "source": "diario.elmundo.sv",
        "url": "https://diario.elmundo.sv/nacionales/capturan-a-dos-supuestos-responsables-de-homicidio-en-san-miguel",
        "sheet_id": "https://diario.elmundo.sv/nacionales/capturan-a-dos-supuestos-responsables-de-homicidio-en-san-miguel",
        "date": "2024-05-18",
        "tag": "Homicidio",
        "sheet": {
            "indicators": [
                {
                    "indicator_name": "Clasificación",
                    "response": "**"
                },
                {
                    "indicator_name": "Título",
                    "response": "** Capturan a dos supuestos responsables de homicidio en San Miguel"
                },
                {
                    "indicator_name": "Resumen",
                    "response": "** La policía capturó a dos sospechosos de cometer un homicidio en el cantón Hato Nuevo, de San Miguel."
                },
                {
                    "indicator_name": "Lugar de los Hechos",
                    "response": "** Cantón Hato Nuevo, San Miguel"
                },
                {
                    "indicator_name": "Fuentes",
                    "response": "** No se indica la fuente de información."
                },
                {
                    "indicator_name": "Temas",
                    "response": "**"
                },
                {
                    "indicator_name": "Hechos Violatorios",
                    "response": "**"
                },
                {
                    "indicator_name": "Hipótesis de Hechos",
                    "response": "**"
                },
                {
                    "indicator_name": "Población Vulnerable",
                    "response": "**"
                },
                {
                    "indicator_name": "Tipo de Arma",
                    "response": "**"
                },
                {
                    "indicator_name": "Víctimas",
                    "response": "**"
                },
                {
                    "indicator_name": "Victimario o Presunto Agresor",
                    "response": "**"
                }
            ],
            "id": "https://diario.elmundo.sv/nacionales/capturan-a-dos-supuestos-responsables-de-homicidio-en-san-miguel",
            "priority": 4,
            "_id": "6670d8090eb47c223af309e7"
        }
    },
    {
        "title": "Condenan a dos sujetos a 50 años de cárcel por doble homicidio en 2015",
        "text": "\nEl Tribunal de Sentencia de Usulután condenó a 50 años de cárcel a dos sujetos acusados de un doble homicidio y un intento de homicidio en 2015. Los hechos ocurrieron en el caserío Los Desmontes del cantón Puerto Parada en Usulután.  Los condenados son Jorge Orlando Chávez Morejón y Rogelio Mendoza Ávalos por dos homicidios agravados y un intentó de homicidio. Los hechos ocurrieron el 26 de noviembre del 2015.  De acuerdo a la FGR, los dos condenados junto a seis hombres se vistieron como soldados y llegaron a la casa de las víctimas, las sacaron a la fuerza de su vivienda, los obligaron a acostarse boca abajo y los asesinaron con armas de fuego.  Además, los implicados en el crimen atacaron a balazos a otro hombre que vivía en el sector donde se dieron los hechos.  “Los hombres pidieron que abriera la puerta y no hizo caso, entonces lo sujetos le dijeron que iban a regresar a matarlo, pero este sujeto se fue corriendo por la parte de atrás de la casa, los delincuentes lo vieron y comenzaron a dispararle, pero la víctima se tiró al piso y las balas no impactaron en su puerto”, afirma el informe fiscal.  Los dos condenados llevaron el proceso en ausencia y fueron declarados en rebeldía.   #CombateAlCrimen | Jorge Orlando Chávez Morejón y Rogelio Mendoza Ávalos recibieron condenas de 50 años de prisión por dos homicidios agravados y un intento de homicidio, cometidos en noviembre de 2015 en Usulután. \rLos condenados, junto a otros sujetos, llegaron vestidos de... pic.twitter.com/5tpErstOxj\r— Fiscalía General de la República El Salvador (@FGR_SV) May 3, 2024 \n\n\n\n\n",
        "source": "diario.elmundo.sv",
        "url": "https://diario.elmundo.sv/nacionales/condenan-a-dos-sujetos-a-50-anos-de-carcel-por-doble-homicidio-en-2015",
        "sheet_id": "https://diario.elmundo.sv/nacionales/condenan-a-dos-sujetos-a-50-anos-de-carcel-por-doble-homicidio-en-2015",
        "date": "2024-05-04",
        "tag": "Homicidio",
        "sheet": {
            "indicators": [
                {
                    "indicator_name": "Clasificación",
                    "response": "** Homicidio"
                },
                {
                    "indicator_name": "Título",
                    "response": "** Condenan a dos sujetos a 50 años de cárcel por doble homicidio en 2015"
                },
                {
                    "indicator_name": "Resumen",
                    "response": "** El Tribunal de Sentencia de Usulután condenó a 50 años de cárcel a dos sujetos acusados de un doble homicidio y un intento de homicidio en 2015."
                },
                {
                    "indicator_name": "Lugar de los Hechos",
                    "response": "** Puerto Parada, Usulután"
                },
                {
                    "indicator_name": "Fuentes",
                    "response": "** N/A"
                },
                {
                    "indicator_name": "Temas",
                    "response": "** Seguridad, justicia"
                },
                {
                    "indicator_name": "Hechos Violatorios",
                    "response": "** Los dos condenados junto a seis hombres se vistieron como soldados y llegaron a la casa de las víctimas, las sacaron a la fuerza de su vivienda, los obligaron a acostarse boca abajo y los asesinaron con armas de fuego."
                },
                {
                    "indicator_name": "Hipótesis de Hechos",
                    "response": "** N/A"
                },
                {
                    "indicator_name": "Población Vulnerable",
                    "response": "** N/A"
                },
                {
                    "indicator_name": "Tipo de Arma",
                    "response": "** Armas de fuego"
                },
                {
                    "indicator_name": "Víctimas",
                    "response": "** N/A"
                },
                {
                    "indicator_name": "Victimario o Presunto Agresor",
                    "response": "N/A"
                }
            ],
            "id": "https://diario.elmundo.sv/nacionales/condenan-a-dos-sujetos-a-50-anos-de-carcel-por-doble-homicidio-en-2015",
            "priority": 4,
            "_id": "6670d8130eb47c223af309e8"
        }
    },
    {
        "title": "Capturan a supuesto responsable de homicidio en San Miguel",
        "text": "\n        La Policía Nacional Civil (PNC) capturó este viernes a Saúl Pineda Flores, supuesto responsable del homicidio de un hombre de 69 años en El Tránsito, San Miguel. \rFlores habría atacado a la víctima con arma blanca, ocasionándole la muerte, de acuerdo a las investigaciones de la corporación policial. \rLa PNC dijo en su cuenta de X, que el detenido “será enviado a prisión por el delito de homicidio”. \r“No vamos a dejar ningún crimen en la impunidad”, aseguró la Policía en la red social, acompañando la publicación con la foto del capturado.\n                \n\n\n\n",
        "source": "diario.elmundo.sv",
        "url": "https://diario.elmundo.sv/nacionales/capturan-a-supuesto-responsable-de-homicidio-en-san-miguel",
        "sheet_id": "https://diario.elmundo.sv/nacionales/capturan-a-supuesto-responsable-de-homicidio-en-san-miguel",
        "date": "2024-05-03",
        "tag": "Homicidio",
        "sheet": {
            "indicators": [
                {
                    "indicator_name": "Clasificación",
                    "response": "** Homicidio"
                },
                {
                    "indicator_name": "Título",
                    "response": "** Capturan a supuesto responsable de homicidio en San Miguel"
                },
                {
                    "indicator_name": "Resumen",
                    "response": "** La policía capturó a Saúl Pineda Flores, supuesto responsable del homicidio de un hombre de 69 años en El Tránsito, San Miguel."
                },
                {
                    "indicator_name": "Lugar de los Hechos",
                    "response": "** El Tránsito, San Miguel"
                },
                {
                    "indicator_name": "Fuentes",
                    "response": "** No se indicaron las fuentes de información."
                },
                {
                    "indicator_name": "Temas",
                    "response": "** Seguridad, crimen"
                },
                {
                    "indicator_name": "Hechos Violatorios",
                    "response": "** No se especificaron los hechos violatorios."
                },
                {
                    "indicator_name": "Hipótesis de Hechos",
                    "response": "** No se planteó una hipótesis de hechos."
                },
                {
                    "indicator_name": "Población Vulnerable",
                    "response": "** No se identificó población vulnerable."
                },
                {
                    "indicator_name": "Tipo de Arma",
                    "response": "** No se especificó el tipo de arma."
                },
                {
                    "indicator_name": "Víctimas",
                    "response": "** No se identificaron las víctimas."
                },
                {
                    "indicator_name": "Victimario o Presunto Agresor",
                    "response": "N/A"
                }
            ],
            "id": "https://diario.elmundo.sv/nacionales/capturan-a-supuesto-responsable-de-homicidio-en-san-miguel",
            "priority": 4,
            "_id": "6670d81b0eb47c223af309e9"
        }
    },
    {
        "title": "Capturan a hombre que deberá pasar un siglo en prisión por homicidio y secuestro",
        "text": "\n        La Policía Nacional Civil (PNC) capturó este miércoles a Ángel María López Preza quien deberá pasar un siglo en prisión por los delitos de homicidio y secuestro. \rLa institución explicó que López Preza fue detenido por la División de Cumplimiento de Disposiciones Judiciales, debido a que era reclamado por uno de los juzgados de Vigilancia Penitenciaria de San Salvador, desde el 2010. \rSegún el reporte, el detenido fue condenado a 80 años de prisión, por el secuestro de cuatro personas, y a 20 años más por homicidio agravado.\r “Con el trabajo de diferentes unidades policiales, este sujeto fue localizado en el cantón Ánimas, de San José Guayabal, Cuscatlán. Pasará el resto de sus años pagando cada uno de sus crímenes”.  PNC Redes sociales  Más capturas\rDurante este 17 de abril también se informó sobre capturas de otras personas relacionadas con grupos delictivos. \rAlexander Daniel Monroy Velásquez, alias Chapin, fue capturado en San Salvador y será procesado por agrupaciones ilícitas por pertenecer a la pandilla Barrio 18, fracción Sureños. El detenido posee antecedentes por tráfico de drogas y robo. \rPor el mismo delito, de agrupaciones ilíticas, serán procesados Carlos Antonio Sánchez Sánchez, alias Colocho, y Boris Mauricio Martínez Sánchez, alias Negro, este último involucrado en la desaparición de una mujer. Ambos hombres, supuestos miembros de la Mara Salvatrucha, fueron detenidos en el cantón El Cedral, en el municipio de Nejapa y la PNC aseguró que también están siendo investigados por extorsión agravada. \rHerson Roberto Sorto Aguilar, alias el Diablo, es otro de los capturados en las últimas horas, y es acusado de pertenecer a la Mara Salvatrucha. El detenido irá a prisión por el delito de agrupaciones ilícitas y, según la PNC, intentó esconderse en una vivienda en San Miguel, para evitar ser detenido. \rLa Policía también detuvo a Heriberto Antonio Flores Cubias, de 48 años, que posee antecedentes desde 2005 por homicidio simple y agrupaciones ilícitas, y se presume es miembro de la pandilla Barrio 18, fracción Revolucionarios. La PNC dijo que Flores Cubias intentó borrar sus tatuajes y se los quemó.\n\n\n\n\n",
        "source": "diario.elmundo.sv",
        "url": "https://diario.elmundo.sv/nacionales/capturan-a-hombre-que-debera-pasar-un-siglo-en-prision-por-homicidio-y-secuestro",
        "sheet_id": "https://diario.elmundo.sv/nacionales/capturan-a-hombre-que-debera-pasar-un-siglo-en-prision-por-homicidio-y-secuestro",
        "date": "2024-04-18",
        "tag": "Homicidio",
        "sheet": {
            "indicators": [
                {
                    "indicator_name": "Clasificación",
                    "response": "** Homicidio"
                },
                {
                    "indicator_name": "Título",
                    "response": "** Capturan a hombre que deberá pasar un siglo en prisión por homicidio y secuestro"
                },
                {
                    "indicator_name": "Resumen",
                    "response": "** La policía capturó a un hombre que deberá pasar un siglo en prisión por los delitos de homicidio y secuestro."
                },
                {
                    "indicator_name": "Lugar de los Hechos",
                    "response": "** San Salvador, Cuscatlán"
                },
                {
                    "indicator_name": "Fuentes",
                    "response": "** No se especifica la fuente de información."
                },
                {
                    "indicator_name": "Temas",
                    "response": "** Seguridad pública, crimen, homicidio, secuestro."
                },
                {
                    "indicator_name": "Hechos Violatorios",
                    "response": "** El hombre fue condenado a 80 años de prisión por el secuestro de cuatro personas y a 20 años más por homicidio agravado."
                },
                {
                    "indicator_name": "Hipótesis de Hechos",
                    "response": "** No se especifica la hipótesis de hechos."
                },
                {
                    "indicator_name": "Población Vulnerable",
                    "response": "** No se especifica la población vulnerable."
                },
                {
                    "indicator_name": "Tipo de Arma",
                    "response": "** No se especifica el tipo de arma."
                },
                {
                    "indicator_name": "Víctimas",
                    "response": "** No se especifica el número de víctimas."
                },
                {
                    "indicator_name": "Victimario o Presunto Agresor",
                    "response": "N/A"
                }
            ],
            "id": "https://diario.elmundo.sv/nacionales/capturan-a-hombre-que-debera-pasar-un-siglo-en-prision-por-homicidio-y-secuestro",
            "priority": 4
        }
    }
]


async def mocked_():
    yield f"data: True\n\n"
    yield f"data: {mocked}\n\n"


@router.get("/model_gemma")
async def model_gemma(search: str = "Feminicidio", gemma_mode: str = "accurate", date_start: str = "",
                      date_end: str = "", number_search=10, start_from=0) -> StreamingResponse:
    """
    Route for applying the Gemma model to scraped news.

    Args:
        search (str): The search term (default: "Feminicidio").
        gemma_mode (str): The Gemma mode (default: "accurate").
        date_start (str): The start date (default: "").
        date_end (str): The end date (default: "").

    Returns:
        StreamingResponse: A streaming response containing the processed news data.
        :param start_from: index of start new
        :param number_search: number of elemts to search
    """
    news = global_search_static(search, date_start, date_end, number_search, start_from)
    return StreamingResponse(create_news_gemma(news, gemma_mode), media_type="text/event-stream")

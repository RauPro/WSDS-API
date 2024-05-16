import re
from datetime import datetime
from uuid import uuid4

from fastapi import FastAPI, HTTPException, APIRouter

from ..models import Prompt, New, SheetEntry
from ..services.driver.news_crud import create_new, get_news, get_new_by_id, update_new, delete_new, get_news_sheets

router = APIRouter()


@router.post("/news/")
def create(new: New):
    new_ = create_new(new)
    return {"message": "new created successfully", "data": new.dict(), "returned": new_}


@router.get("/news/")
def read_all():
    return get_news()


@router.get("/news-sheet/")
def read_all():
    return get_news_sheets()

mocked_sheet = [
    {
        "url": "https://diario.elmundo.sv/Nacionales/policia-captura-a-feminicida",
        "date": "2024-05-01",
        "sheet_id": "https://diario.elmundo.sv/Nacionales/policia-captura-a-feminicida",
        "source": "diario.elmundo.sv",
        "tag": "Feminicido",
        "text": "\nEl sujeto fue presentado ayer por la PNC. /JM\n\r\nCarlos Alberto Gómez Ramos fue presentado ayer por la Policía Nacional Civil (PNC) por feminicido. Las investigaciones policiales sobre el feminicidio indican fue cometido, a principios de este mes contra una sirvienta en la colonia Escalón de San Salvador.\n\r\nLa Unidad de Delitos Especiales (UDE) de la PNC determinó que Gómez Ramos, de 28 años de edad, cometió el asesinato de Blanca López Hernández. Según la versión policial, el detenido ultimó a López Hernández con arma de fuego, porque ella decidió terminar la relación sentimental que ambos sostenían.\n\r\nEl homicidio ocurrió el 2 de julio en la 3a. avenida Norte, entre la 9a. y 11a. calle Poniente de San Salvador, cuando López Hernández se disponía a regresar a su hogar, en Monte San Juan, Cojutepeque.\n\r\n \n                \n\n\n\n",
        "title": "Policía captura a feminicida",
        "sheet": None
    },
    {
        "url": "https://www.diariocolatino.com/historia-universal-un-vistazo-al-pasado-desde-la-causa-popular/6el-salvador-feminicido/",
        "date": "2024-05-01",
        "sheet_id": "https://www.diariocolatino.com/historia-universal-un-vistazo-al-pasado-desde-la-causa-popular/6el-salvador-feminicido/",
        "source": "diariocolatino.com",
        "tag": "Feminicido",
        "text": "\n\nCompartir\n\n Facebook\n Twitter\n Google +\n\n\n\n\n\nArtículos relacionados\n\n\n\n\n\n \n\n\nJuramentan nueva legislatura \n1 mayo, 2024\n\n\n\n\n \n\n\nDesafíos para la izquierda salvadoreña\n1 mayo, 2024\n\n\n\n\n \n\n\nSesiona la nueva legislatura 2024-2027 \n1 mayo, 2024\n\n\n\n\n\n",
        "title": "*6El Salvador feminicido",
        "sheet": None
    },
    {
        "url": "https://diarioelsalvador.com/mas-de-65-mareros-capturados-en-operativo-efectuado-en-seis-municipios-de-santa-ana/433564/",
        "date": "2024-05-01",
        "sheet_id": "https://diarioelsalvador.com/mas-de-65-mareros-capturados-en-operativo-efectuado-en-seis-municipios-de-santa-ana/433564/",
        "source": "diarioelsalvador.com",
        "tag": "Feminicido",
        "text": "Un operativo policial y fiscal desarrollado la madrugada de este jueves permitió la captura de más de 65 criminales vinculados con la Mara Salvatrucha y la pandilla 18 Sureños, así como delincuentes comunes, que mantenían su accionar delictivo en seis municipios situados en el departamento de Santa Ana. Por medio de la operación denominada «Ucrania», las autoridades procedieron a hacer efectivos el arresto de los delincuentes de un total de 214 órdenes de capturas giradas por la Fiscalía General de la República (FGR). En ese sentido, hubo registros y allanamientos en los municipios de El Congo, Chalchuapa, Candelaria de La Frontera, Coatepeque, Metapán y Santa Ana. Los criminales serán procesados en los tribunales contra el crimen organizado donde serán acusados por los siguientes delitos: homicidio agravado, robo agravado, extorsión e intento de feminicidio, desaparición de personas, agrupaciones ilícitas y delitos sexuales. Las autoridades informaron que 45 de los pandilleros sobre los cuales fue emitida una orden de detención ya se encuentran bajo arresto en diferentes centros penitenciarios, pues han sido intervenidos en el marco del régimen de excepción, por lo que será en las cárceles donde se les informe de los nuevos delitos que les imputan. «Gracias a la operación se resolverán 40 casos de diversos delitos, llevando justicia a las víctimas de estos criminales», comunicó la FGR.Fuentes oficiales indicaron que para hacer efectivas las detenciones participaron en este procedimiento 160 agentes policiales que fueron apoyados por 100 soldados. Entre los sospechosos que fueron arrestados están: Eli Lazan, de 49 años, Luis Alonso Chicas, (47), Víctor Manuel García (30), Fernando Cruz (25), Nataly Pérez (35), Jaime Antonio Canjura (39), Berta Aquino (47), Bryan Omar Catota (22), Petrona Isabela Sama (67), Roxana Chávez (36), Reyna Cornejo (51), Evelyn Corado (43), Jeremías Hernández (54), Kevin Sorto (27), Marcos Henríquez (38), Elvira de Los Ángeles (47), Beatriz Morán (27), Daniela Catota (25), Ana Silvia Bojórquez (60), Margarita Peraza (29), María Isabel Gonzales (63), Cecilio Valiente (49), Guadalupe del Carmen (45), Julia Núñez (26), Marcela Estefanía Núñez (24), Katherine Godínez (22), Zoila María Hernández (30), Norma Pérez (36), Alejandro Ibero (18), Samuel Antonio Rodríguez (46), Yesenia Roxana Molina (43), César Eduardo Núñez (32), Sandra de Los Ángeles (39), Norma Griselda Hernández (46), Juan Alfredo Rendón (26), Carlos Antonio González (22), Alexander Bernal (19), Jhonatan Lázaro Cornejo (30), Rosa de Lázaro (43), Leticia Raquel Barrera de Gómez (42), Nora Elizabeth Hernández (46), Patricia del Rosario (37), Delmy Arely Lemus (20) y Ruth López Martínez(40).  #Operativo I De acuerdo a las investigaciones, los delitos por los que serán procesados son:▶️Homicidio agravado.▶️Robo agravado.▶️Extorsión.▶️Feminicido agravado en grado de tentativa. pic.twitter.com/RiLTjA7tfY",
        "title": "Más de 65 mareros capturados en operativo efectuado en seis municipios de Santa Ana",
        "sheet": None
    },
    {
        "url": "https://diarioelsalvador.com/fiscal-general-asegura-que-sospechoso-confeso-crimen-contra-nina-de-la-campanera/420371/",
        "date": "2024-05-01",
        "sheet_id": "https://diarioelsalvador.com/fiscal-general-asegura-que-sospechoso-confeso-crimen-contra-nina-de-la-campanera/420371/",
        "source": "diarioelsalvador.com",
        "tag": "Feminicido",
        "text": "El fiscal general de la república, Rodolfo Delgado, confirmó, este miércoles, que Edwin Mauricio Alvarado Lazo, quien actualmente se encuentra detenido por el delito de resistencia, será acusado formalmente por el feminicido de la niña Melissa, el próximo viernes y detalló que, el presunto agresor sexual ha confesado haber cometido el crimen que estremeció a los habitantes de La Campanera.«Durante las entrevistas realizadas por agentes de la Policía se empezó a perfilar a Edwin Alvarado como un posible sospechoso de la muerte de Melissa, y es de esa forma como se logra llegar a la casa 34, del polígono 31 sur, de La Campanera», expresó el fiscal. Detalló que durante la entrevista que realizaron los agentes investigadores, Alvarado Lazo se vio acorralado, y empezó a dar versiones contradictorias, llegando a un punto de la entrevista en que se quiebra y decide confesar los hechos, declarándose el causante de la muerte de Melissa.«Sin embargo, nosotros no solo estamos afirmando la participación de Edwin Alvarado con la confesión de él, ya que se practicaron diferentes inspecciones, en los diferentes escenarios donde Melissa permaneció las últimas horas de su vida, y se fueron recolectando uno a uno diferentes elementos probatorios, incluyendo una cuerda que poseía los mismos tipos de nudo que poseía la cuerda que Edwin Alvarado utilizaba en el interior de su vivienda», dijo Delgado.Añadió «encontramos en el interior de su vivienda un mismo tipo de esponja que se encontró contiguo al cadáver de la víctima, el mismo tipo de alambre que se encontró en el interior del saco donde fue encontrado su cuerpo, se encontraba también en su casa de habitación».Delgado detalló que en el interior de la vivienda del sospechoso también encontraron diferentes objetos que evidencian la presencia de otros niños en anteriores oportunidades, como por ejemplo: colas para el cabello, juguetes y ropa de niña que estaban ocultas bajo la cama en la cual dormía Edwin Alvarado. SEGUIRÁ PRESO Y SERÁ ACUSADO POR OTRO TRES DELITOSAyer, el Juzgado Primero de Paz de San Salvador, ordenó que Alvarado Lazo, acusado de asesinar a Melissa H. de siete años, siga en detención por el delito de resistencia. Este es el primer proceso en contra del imputado, ya que mañana viernes será remitido a otro juzgado por el crimen en perjuicio de la niña.«El día viernes estaremos presentando ante el Tribunal competente el requerimiento fiscal por los delitos de feminicidio, violación y privación de libertad contra Edwin Alvarado Lazo, cometidos en perjuicio de la niña Melissa», indicó el funcionario.El crimen fue cometido por Alvarado Lazo el pasado 9 de octubre en la colonia La Campanera, de Soyapango. Y ayer, el fiscal explicó cómo se dio la captura de Alvarado Lazo por el delito de resistencia. #DePaís | «Durante la entrevista que realizaron los agentes investigadores, el sujeto se vio acorralado, y empezó a dar versiones contradictorias, llega un punto de la entrevista en que el sujeto se quiebra y decide confesar los hechos, la persona confesó que fue él el causante… pic.twitter.com/6VlV2yVnaH «Es importante que quede claro, cómo se da la captura por resistencia de Alvarado Lazo, a quien durante las entrevistas que los agentes investigadores realizaron durante el día 10 de octubre, se empezó a perfilar como un sujeto de interés, al ser una persona que mantenía como costumbre merodear el parque de esa colonia y estar observando a los menores de edad que asistían a jugar, al tiempo que se tocaba su área genital», señaló Delgado.El fiscal explicó que, luego de las entrevistas, la PNC realizó las coordinaciones necesarias para ubicar al sospechoso en las inmediaciones del bulevar Tutunichapa, en San Salvador, lugar donde trabajaba como obrero, dedicado a cargar camiones con arena.«Cuando Edwin Mauricio regresaba de su trabajo fue abordado por elementos de la Policía, la persona desde que observó a los agentes intentó ocultarse de ellos en unos vehículos aparcados en esa zona, cuando los policías se acercan a él, lo ubica y lo requisa, Edwin empieza a insultarlos y forcejear con ellos, desde ese momento estaba cometiendo el delito de resistencia, y eso motivo su detención el día 11 de octubre», apuntó Delgado.",
        "title": "Fiscal General asegura que sospechoso confesó crimen contra niña de La Campanera",
        "sheet": None
    },
    {
        "url": "https://diarioelsalvador.com/hombre-que-asesino-a-su-expareja-en-san-salvador-seguira-en-prision/107025/",
        "date": "2024-05-01",
        "sheet_id": "https://diarioelsalvador.com/hombre-que-asesino-a-su-expareja-en-san-salvador-seguira-en-prision/107025/",
        "source": "diarioelsalvador.com",
        "tag": "Feminicido",
        "text": "Juan Carlos Ramírez, de 36 años continuará el proceso judicial en su contra en prisión. Ramírez es acusado por la Fiscalía General de la República (FGR) por haber asesinado a su expareja la noche del pasado sábado 10 de julio. «Tras finalizar la audiencia inicial, el juez del Juzgado Séptimo de Paz decretó que el caso continúe con la detención provisional del imputado», señaló la fiscal del caso. Agregó que tras las investigaciones realizadas por la FGR se ha establecido que Ramírez cometió el delito de feminicidio agravado en contra de su excompañera de vida Briana Flores. Según las autoridades el crimen ocurrido en la avenida Los Andes, al costado norte del Colegio García Flamenco, en San Salvador fue realizado con arma blanca. «Cuando el abordó a la víctima en el lugar del crimen, hubo una discusión, él procede a sacar un arma blanca causándole lesiones profundas que le provocaron una muerte inmediata a su expareja», detallaron las autoridades. Por su parte la fiscal señaló que la desigualdad de poder, el machismo, el sexismo, la posesión y la persecución que Ramírez le daba a la víctima derivó en el cometimiento del delito. «Tienen un hijo en común pero no podemos detallar si aún estaban juntos», explicó la fiscal. Añadió que por el momento el caso pasa al Juzgado Especializado para una Vida Libre de Violencia en contra de las Mujeres.",
        "title": "Hombre que asesinó a su expareja en San Salvador seguirá en prisión",
        "sheet": None
    },
    {
        "url": "https://www.diariocolatino.com/wp-content/uploads/2018/11/",
        "date": "2024-05-01",
        "sheet_id": "https://www.diariocolatino.com/wp-content/uploads/2018/11/",
        "source": "diariocolatino.com",
        "tag": "Feminicido",
        "text": "",
        "title": "No se encontró el título",
        "sheet": None
    },
    {
        "url": "https://diario.elmundo.sv/search?query=Feminicido",
        "date": "2024-05-01",
        "sheet_id": "https://diario.elmundo.sv/search?query=Feminicido",
        "source": "diario.elmundo.sv",
        "tag": "Feminicido",
        "text": "No se encontró el texto del articulo",
        "title": "No se encontró el título",
        "sheet": None
    },
    {
        "url": "https://diario.elmundo.sv/Nacionales/asesinan-a-madre-hija-y-nieta-de-4-meses-en-ciudad-delgado",
        "date": "2024-05-01",
        "sheet_id": "https://diario.elmundo.sv/Nacionales/asesinan-a-madre-hija-y-nieta-de-4-meses-en-ciudad-delgado",
        "source": "diario.elmundo.sv",
        "tag": "Feminicido",
        "text": "\n        Armida Marisol Méndez, de 42 años, su hija Alexia Marisol Rivera, de 22 y su nieta Valentina Rivas, de cuatro meses y 21 días, fueron asesinadas en una vivienda de la colonia Santa Marta, de Ciudad Delgado, San Salvador.\n\r\nEl triple crimen, supuestamente fue cometido por dos sujetos que habrían tocado la puerta haciéndose pasar como policías en la medianoche del pasado lunes.\n\r\nSegún la información, los homicidas dispararon directamente a madre e hija, mientras que la bebé fue alcanzada por las balas que dispararon contra su progenitora Alexia Marisol. La bebé, aún con vida, fue trasladada al hospital Benjamín Bloom, pero murió en los brazos de su padre, de acuerdo a la información.\n\r\nOtra niña se habría salvado de morir porque afortunadamente se fue a dormir donde otros parientes cercanos.\n\r\nArmida Marisol Méndez, estaría embarazada, según el informe de la Fiscalía General de La República (FGR).\n\r\nEl ministerio público no maneja una hipótesis del triple crimen, aunque la Policía no descarta que se trate de un ajuste de cuentas. Sin embargo, familiares cercanos desconocían que estuviesen amenazadas. Una versión, apunta a que ambas mujeres tendrían vínculos con pandillas.\n\r\nEsta sería la novena masacre del mes, según los registros policiales y fiscales. Además sería el segundo triple feminicido registrado en abril, el primero fue el de una madre y sus dos hijas asesinadas el pasado 4 de abril durante un robo en su vivienda, en la colonia Quezaltepec de Santa Tecla.\n\r\nPor su parte,  el titular de la Procuraduría para la Defensa de los Derechos Humanos, David Morales, lamenta este acto de violencia, “el cual evidencia la saña, odio, maldad y violencia irracional con la que operan las estructuras criminales que están atacando a la sociedad y que ahora se cobra la vida de tres mujeres de una misma familia”, dijo a través de un comunicado.\n\r\nEl procurador Morales externa su preocupación por el triple crimen de Ciudad Delgado, al igual que el alza en los casos que se han registrado durante los últimos meses y en los cuales mujeres y niñas han sido las víctimas. El funcionario  demanda a la Fiscalía General de la República que otorgue prioridad a la investigación de este crimen.\n\r\n \n\nDos masacres contra mujeres \n\r\n \n\r\nEl crimen de Ciudad Delgado sería la segunda masacre contra tres mujeres en un periodo de 10 días.\n\r\nEl pasado 4 de abril, una mujer de 40 años y sus hijas de 20 y ocho años, fueron asesinadas con saña, en una vivienda de la colonia Quezaltepec, de Santa Tecla.\n\r\nLos homicidas habrían utilizado arma blanca, luego de mantenerlas atadas por tres horas, según la Policía Nacional Civil.\n\r\nLos tres feminicidios habría sido cometido por sujetos que conocían a sus víctimas y para no dejar testigos les quitaron la vida, tras robarles $20 mil.\n\r\nMientras que el triple feminicidio contra madre, hija y nieta, cometido la noche del lunes, en Ciudad Delgado, estaría vinculado a las pandillas, según la PNC. Por el primer crimen, están siendo procesados tres sospechosos, mientras que por la segunda masacre aún no se reportan capturas.\n\r\n \n\n9 Masacres\n\r\nEntre el 3 y el 12 de abril, se han registrado nueve masacres en el país.\n\n \n\n6 Mujeres\n\r\nEn las dos masacres de mujeres registradas en abril han muerto seis mujeres.\n                \n\n\n\n",
        "title": "Asesinan a madre, hija y nieta de 4 meses en Ciudad Delgado",
        "sheet": None
    },
    {
        "url": "fake_url",
        "date": "2024-05-05",
        "sheet_id": "fake_url",
        "source": "diarioelsalvador.com",
        "tag": "Feminicido",
        "text": "Un joven adulto fue acusado el miércoles en Francia de haber asesinado a su compañera, con el fin de vivir una relación con una supuesta mujer de quien se había enamorado en internet y que resultó ser un estafador sentimental. El individuo nacido en 1994, empleado técnico de una alcaldía, reconoció haber planeado el crimen para poder «concretar» su relación virtual y afirmó que «lamentaba»  su acción, señaló en un comunicado la Fiscalía de Boulogne-sur-Mer (norte). La víctima, enfermera en una residencia de ancianos, nacida en 1995, fue hallada muerta el 28 de enero en el domicilio de la pareja, en la localidad de Beussent, con «heridas en el torso». Fue su propio compañero quien llamó a los gendarmes, asegurando que todo había ocurrido cuando se ausentó para ir a comprar pan, probablemente con fines de robo dada la desaparición de una alcancía. Pero la investigación descartó esa hipótesis y acusó al hombre, que «mantenía una relación afectiva en internet» con una persona de la cual ignoraba su verdadera identidad. Según el diario Le Parisien, que reveló el caso, esa pasión virtual se presentaba con el nombre de Béatrice Leroux, comerciante en la ciudad de Brest. La supuesta amante resultó ser un personaje ficticio creado por un estafador emocional, probablemente basado en Costa de Marfil, que había logrado que su enamorado le enviase 2.200 euros (unos 2.400 dólares). Numerosas bandas criminales que operan desde África occidental se especializan en estafas por internet, muchas veces creando fuertes vínculos afectivos con las personas contactadas. Francia registra en promedio un feminicidio cada tres días. El año pasado se contabilizaron 94.",
        "title": "Hombre enamorado de una mujer ficticia confiesa el asesinato de su compañera en Francia",
        "sheet": None
    },
    {
        "url": "https://diarioelsalvador.com/",
        "date": "2024-05-05",
        "sheet_id": "https://diarioelsalvador.com/",
        "source": "diarioelsalvador.com",
        "tag": "Homicidio",
        "text": "Alcaldes de Nuevas Ideas han impulsado y aprobado con sus concejos municipales no realizar incrementos en salarios, dietas y gastos... El Banco Central de Reserva (BCR) avanza en el Censo de Población y Vivienda y ha cubierto territorio en los... El Tribunal de Sentencia de Usulután condenó a 25 años de cárcel a cinco integrantes de la clica Criminal Gánster... El Ministerio de Obras Públicas (MOP) y el Viceministerio de Transporte (VMT) organizan la PedaleadaSV para promover la movilidad alternativa en El Salvador, que se desarrolla en el periférico Claudia Lars, en donde las familias salvadoreñas participan en esta iniciativa. Cientos de ciclistas de diferentes partes... Ahora se espera adelantar el reconocimiento internacional de estas zonas, lo que podría facilitar la apertura de mercados. El objetivo de Brasil es el reconocimiento internacional como país totalmente libre de fiebre aftosa sin vacunación para 2026. Las familias salvadoreñas han llenado de color las iglesias, casas, calles y escuelas con matices que adornan el altar a... La justicia de Nepal intimó al gobierno a limitar los permisos de ascenso del Everest y otras cumbres, confirmó el... La pelea de gallos es el juego de azar más famoso del distrito de Bastar, que alberga densos bosques poblados... Está semana se conoció que Firpo podría no jugar la Copa Centroamericana de Clubes...",
        "title": "",
        "sheet": None
    },
    {
        "url": "https://diarioelsalvador.com/condenados-a-50-anos-de-prision-por-dos-asesinatos/499881/",
        "date": "2024-05-05",
        "sheet_id": "https://diarioelsalvador.com/condenados-a-50-anos-de-prision-por-dos-asesinatos/499881/",
        "source": "diarioelsalvador.com",
        "tag": "Homicidio",
        "text": "Dos criminales fueron condenados a 50 años de cárcel por asesinar a dos personas e intentar quitarle la vida a otra. Los asesinos fueron identificados por las autoridades como Jorge Orlando Chávez Morejón y Rogelio Mendoza Ávalos, y aunque siguen prófugos de la justicia, fueron procesados por los delitos de homicidio agravado e intento de homicidio.  Según los registros de la Fiscalía General de la República (FGR), cometieron los crímenes en noviembre de 2015, en Usulután. Las investigaciones determinaron que Chávez y Mendoza, junto con otros sujetos, vestían como soldados y simularon operativos para sacar a las víctimas de su vivienda.  Una vez en la calle, los atacantes asesinaron con arma de fuego a los ciudadanos; sin embargo, en medio del ataque armado hubo sobrevivientes. Fuentes fiscales detallaron que hasta el momento Chávez Morejón y Mendoza Ávalos se mantienen prófugos, pero gracias a las reformas del Código Procesal Penal estos individuos fueron condenados en ausencia. Al ser localizados y arrestados cumplirán la pena establecida en un centro penitenciario.  Las autoridades piden la colaboración de la ciudadanía para brindar información sobre el paradero de los sujetos. En septiembre de 2022, la Asamblea Legislativa aprobó reformas en el Código Procesal Penal para que los reos en rebeldía declarados como prófugos sean enjuiciados.  Según los registros de la Fiscalía, entre 2013 y 2022 hubo 31,652 procesados en los juzgados que mantienen la condición de rebeldía, de los cuales, muchos están prófugos de la justicia. Por ejemplo, en julio de 2023, el Tribunal Tercero de Sentencia de San Salvador condenó a Mauricio Funes (expresidente por el FMLN, asilado en Nicaragua) a seis años de prisión por defraudación al fisco en la modalidad de evasión de impuestos, cometida en 2014.  Esa fue la segunda condena que Funes acumula, ya que el 29 de mayo de ese mismo año, el Juzgado Especializado de Sentencia C le impuso 14 años por promover, facilitar e impulsar una tregua con pandillas.",
        "title": "Condenados a 50 años de prisión por dos asesinatos",
        "sheet": None
    },
    {
        "url": "https://diarioelsalvador.com/familias-salvadorenas-participan-en-la-maraton-bicentenario-de-la-fuerza-armada/499919/",
        "date": "2024-05-05",
        "sheet_id": "https://diarioelsalvador.com/familias-salvadorenas-participan-en-la-maraton-bicentenario-de-la-fuerza-armada/499919/",
        "source": "diarioelsalvador.com",
        "tag": "Homicidio",
        "text": "Este domingo inició la Media Maratón Bicentenario que celebra los 200 años de existencia de la Fuerza Armada de El Salvador, y que cuenta también con la participación de diferentes familias que se inscribieron para conmemorar a la institución. La maratón inició desde el centro comercial Metrocentro, ubicado en San Salvador Centro, aproximadamente a las 6:00 de la mañana de este domingo. #DePaís | Esta mañana se realizará una media maratón como parte de las actividades de festejo por los 200 años de fundación de la @FUERZARMADASV. 📹: @DefensaSV pic.twitter.com/TkhVoHXWJ8 La población participa en la maratón junto al ministro de Defensa, René Francis Merino Monroy, que recorre la categoría de los 21 kilómetros. Corredores de todas las edades participaron junto a sus mascotas en la Media Maratón Bicentenario de la Fuerza Armada. 🐾🐕 Corredores de todas las edades, participaron junto a sus mascotas en la Media Maratón Bicentenario de la @FUERZARMADASV. pic.twitter.com/LbapwhFSOP Los participantes recorren diferentes distancias del Circuito Certificado de la Federación Salvadoreña de Atletismo en los recorridos 1k, 3k, 5k, 10k y 12k. Durante la maratón prevalece el ambiente de seguridad por el cual la Fuerza Armada trabaja diariamente, a lo largo y ancho del territorio salvadoreño durante el régimen de excepción, que ha permitido erradicar a las pandillas y reducir los delitos como homicidios al mínimo.",
        "title": "Familias salvadoreñas participan en la maratón Bicentenario de la Fuerza Armada",
        "sheet": None
    },
    {
        "url": "https://diarioelsalvador.com/pandilleros-pasaran-25-anos-en-la-carcel-por-matar-a-hombre/499884/",
        "date": "2024-05-05",
        "sheet_id": "https://diarioelsalvador.com/pandilleros-pasaran-25-anos-en-la-carcel-por-matar-a-hombre/499884/",
        "source": "diarioelsalvador.com",
        "tag": "Homicidio",
        "text": "El Tribunal de Sentencia de Usulután condenó a 25 años de cárcel a cinco integrantes de la clica Criminal Gánster Locos Salvatruchos de la MS-13 por el homicidio agravado de un hombre al que atacaron cuando descansaba en su casa.  De acuerdo con el informe oficial, el crimen se cometió el 16 de enero de 2019, cuando la víctima, de 74 años, descansaba en su casa, en el caserío Nuevo Puente, en el cantón San Marcos Lempa, del distrito de Jiquilisco, en el municipio de Usulután Oeste.  Según el reporte fiscal, los cinco terroristas llegaron a la casa de la víctima y la atacaron con arma blanca, por lo que le provocaron lesiones graves en la cabeza y el cuello que le causaron la muerte. Por este hecho han sido sentenciados Gabriel Alberto Iraheta Orellana, alias Turis; Jaime Balmore Beltrán Abarca, alias Domba; Rubén Ernesto Mejía Roque, alias Carmelo; Oswaldo Antonio Castillo, alias Pico; y Milagro del Carmen Mejía Roque.  De momento, los cinco criminales están prófugos de la justicia; sin embargo, el Tribunal de Sentencia de Usulután los procesó gracias a la reforma del Código Procesal Penal que permite decretar sentencia firme contra delincuentes que han sido declarados en rebeldía.",
        "title": "Pandilleros pasarán 25 años en la cárcel por matar a hombre",
        "sheet": None
    },
    {
        "url": "https://diarioelsalvador.com/seccion/depais/",
        "date": "2024-05-05",
        "sheet_id": "https://diarioelsalvador.com/seccion/depais/",
        "source": "diarioelsalvador.com",
        "tag": "Homicidio",
        "text": "",
        "title": "DePaís",
        "sheet": None
    },
    {
        "url": "https://diarioelsalvador.com/video-nina-conocio-por-primera-vez-el-cuscatlan-y-su-reaccion-conmovio-al-alianza/499525/",
        "date": "2024-05-05",
        "sheet_id": "https://diarioelsalvador.com/video-nina-conocio-por-primera-vez-el-cuscatlan-y-su-reaccion-conmovio-al-alianza/499525/",
        "source": "diarioelsalvador.com",
        "tag": "Homicidio",
        "text": "El partido del pasado miércoles, Alianza-FAS escribió una tierna historia con una pequeña aficionada aliancista, la cual ha conmovido las redes sociales y al propio equipo albo, quien le preparó una sorpresa. Gabriela Contreras es la protagonista de dos videos que se han viralizado en redes sociales. El primero de cuando entra al estadio Cuscatlán, para ver el duelo entre tigrillos y albos y de la cual su reacción ha sido muy especial. 𝗔𝗰𝗼𝗺𝗽𝗮́𝗻̃𝗲𝗻𝗺𝗲 𝗮 𝘃𝗲𝗿 𝗲𝘀𝘁𝗮 𝗹𝗶𝗻𝗱𝗮 𝗵𝗶𝘀𝘁𝗼𝗿𝗶𝗮 🥹𝗔𝗹𝗶𝗮𝗻𝘇𝗮 𝗲𝘀 𝘆 𝘀𝗲𝗿𝗮́ 𝗱𝗲 𝘀𝘂 𝗴𝗲𝗻𝘁𝗲 🤍 Luego de ver la reacción de Gabrielita entrando al estadio, hoy le dimos la sorpresa que conociera a toda la plantilla 🙌🏼#AlianzaFC pic.twitter.com/hgehFSr4Jz Esta publicación la hizo Tito Contreras, padre de la menor y quien acompaña a la niña, cuando esta grita al entrar al escenario y alcanzar a ver la cancha. Esto también fue compartido en las cuentas del Alianza, quien este viernes compartió la sorpresa que el equipo le hizo a la pequeña Gabi. «Alianza es y será de su gente. Luego de ver la reacción de Gabrielita entrando al estadio, hoy dimos la sorpresa que conociera a toda la plantilla», describió el equipo. La pequeña aliancista visitó al equipo en el entrenamiento, compartió con los jugadores y cuerpo técnico, quienes además le entregaron un balón autografiado y una camisa.",
        "title": "VIDEO| Niña conoció por primera vez el Cuscatlán y su reacción conmovió al Alianza",
        "sheet": None
    },
    {
        "url": "https://diarioelsalvador.com/plan-de-seguridad-logra-608-dias-sin-violencia-homicida-en-el-salvador/499614/",
        "date": "2024-05-05",
        "sheet_id": "https://diarioelsalvador.com/plan-de-seguridad-logra-608-dias-sin-violencia-homicida-en-el-salvador/499614/",
        "source": "diarioelsalvador.com",
        "tag": "Homicidio",
        "text": "La Policía Nacional Civil (PNC) dio a conocer que el jueves 2 de mayo no hubo homicidios en el país, por lo que el acumulado durante la gestión del presidente Nayib Bukele es de 608 días libres de violencia homicida, de los cuales, 89 se han registrado en 2024. Los planes de seguridad gubernamental han reducido al mínimo (0.4 asesinatos diarios) el registro de homicidios durante este año muestra de ello es que abril cerró con 19 jornadas sin muertes violentas. Las estadísticas policiales revelan que desde que se implementó el régimen de excepción (27 de marzo de 2022) hasta el 2 de mayo de este año se reportan 495 días con cero homicidios. Agencias de noticias internacionales también han destacado que en el primer trimestre de 2024 la tasa de homicidios en El Salvador se redujo a 1.5 por cada 100,000 habitantes, por debajo de la tasa registrada al cierre de 2023, que fue de 2.4. Las autoridades del Gabinete de Seguridad han atribuido la reducción histórica de los asesinatos en el país a las más de 80,000 capturas de pandilleros, cuyas estructuras criminales eran las principales autoras de los atentados contra la vida de los salvadoreños. En el marco de los 600 días sin asesinatos en el país, que se cumplieron el 16 de abril de este año, el ministro de Justicia y Seguridad, Gustavo Villatoro, compartió en redes sociales una reflexión sobre lo que ha significado el trabajo ejecutado. «Contabilizamos 600 días sin homicidios, estos datos reflejan todo ese trabajo articulado desde un Estado de derecho, donde hemos puesto al centro de las políticas de seguridad salvaguardar la vida de nuestra gente», expuso. Estos resultados siguen llamando la atención de autoridades de seguridad pública de otras naciones, a las que los funcionarios salvadoreños les han compartido las experiencias en la guerra contra las pandillas. Finalizamos el jueves 02 de mayo, con 0 homicidios en el país. pic.twitter.com/8hhDr7DnNB ",
        "title": "Plan de seguridad logra 608 días sin violencia homicida en El Salvador",
        "sheet": None
    },
    {
        "url": "https://diarioelsalvador.com/choque-entre-buses-en-antiguo-cuscatlan-deja-15-lesionados/499589/",
        "date": "2024-05-05",
        "sheet_id": "https://diarioelsalvador.com/choque-entre-buses-en-antiguo-cuscatlan-deja-15-lesionados/499589/",
        "source": "diarioelsalvador.com",
        "tag": "Homicidio",
        "text": "El choque entre dos unidades de transporte colectivo de pasajeros dejó un saldo de 15 personas lesionadas, en un hecho ocurrido este viernes por la noche. La Policía Nacional Civil (PNC) detalló que el percance corrió sobre la carretera Panamericana, frente a un centro comercial ubicado en Antiguo Cuscatlán, La Libertad. Inspeccionamos un accidente entre 2 buses del transporte público, que dejó cómo resultado 15 personas lesionadas.La colisión ocurrió sobre la carretera Panamericana frente a un centro comercial de la zona, en Antiguo Cuscatlán, La Libertad.Permanecemos en la zona. pic.twitter.com/zAJU1n3Wjf Por el momento, las autoridades policiales solo han señalado que se trata de dos unidades del transporte público y ha cifrado en 15 el total de afectados. Los elementos policiales ya están en la zona para realizar las respectivas investigaciones para esclarecer los hechos. Elementos de instituciones de atención a emergencias también han llegado para brindar asistencia médica a los afectados.",
        "title": "Choque entre buses en Antiguo Cuscatlán deja 15 lesionados",
        "sheet": None
    },
    {
        "url": "https://diarioelsalvador.com/imputan-de-nuevos-crimenes-a-estafador-que-realizaba-rituales-para-obtener-salud-o-beneficios-migratorios/499425/",
        "date": "2024-05-05",
        "sheet_id": "https://diarioelsalvador.com/imputan-de-nuevos-crimenes-a-estafador-que-realizaba-rituales-para-obtener-salud-o-beneficios-migratorios/499425/",
        "source": "diarioelsalvador.com",
        "tag": "Homicidio",
        "text": "La Fiscalía General de la República (FGR) confirmó este viernes una nueva imputación contra un sujeto acusado de estafar a personas prometiendo realizar rituales para mejorar sus situaciones financieras, sentimentales y hasta migratorias. La orden de captura fue girada contra Rudis David Vigil Vigil, acusado de estafar por hasta $17,000 a una mujer. El sujeto prometía realizar «limpias» para que sus víctimas solventaran problemas de salud, sentimentales o estados migratorios. Por estas limpias, el sujeto cobraba grandes cantidades de dinero. Vigil Vigil ya cumple una condena de 16 años de prisión por estafar a otras dos personas por más de $28,000 a cambio de rituales orientados a curar padecimientos físicos. #Captura I La @FGR_SV ordenó la captura de Rudis David Vigil Vigil por estafar a una mujer con 17 mil dólares.Este sujeto les prometía a las personas que les realizaría \"limpias\" para ayudarlas a solventar sus problemas de salud, sentimentales o estados migratorios, todo a… pic.twitter.com/AOqqOVgrZw",
        "title": "Imputan de nuevos crímenes a estafador que realizaba rituales para obtener salud o beneficios migratorios",
        "sheet": None
    },
    {
        "url": "https://diarioelsalvador.com/los-alcaldes-deben-ser-verdaderos-gestores-del-desarrollo-local/499015/",
        "date": "2024-05-05",
        "sheet_id": "https://diarioelsalvador.com/los-alcaldes-deben-ser-verdaderos-gestores-del-desarrollo-local/499015/",
        "source": "diarioelsalvador.com",
        "tag": "Homicidio",
        "text": "El término «desarrollo» no es una semántica simple, es un proceso complejo, que solo un verdadero gestor puede conocer para sentar las bases y promoverlo. Los nuevos alcaldes, con la nueva reorganización territorial, se enfrentan a grandes desafíos y retos, porque ya no esta￾rán tratando con solo un municipio, sino con diversos distritos antes municipios, agregados con problemáticas y necesidades diversas, unas básicas, otras más complejas, a las que tendrán que dar respuestas. Después de la toma de posesión, la pronta acción de los nuevos funcionarios es establecer un verdadero diálogo directo con las comunidades, reorganizar las asociaciones comunales y todas las fuerzas vivas junto con los liderazgos locales; eso les va a permitir tener una radiografía de lo que está sucediendo de manera real y plasmarlo en planes que vayan de lo urgente a lo importante, con acciones inmediatas e indicadoresclaros a seguir. No se pueden dar el lujo de elaborar planes de escritorio solamente para justificar fondos o un financiamiento. Los nuevos equipos técnicos y financieros deben considerar en esta nueva reforma de ley de municipios a distritos los diferentes cambios a las normativas internas que esto implica, y que van a generar cambiosen la nueva organización institucional, desde el diseño de un nuevo organigrama, como la elaboración de nuevos manuales de funcionamiento y de ordenanzas municipales, considerando las características propias de cada distrito; y estas solo serán las acciones iniciales que deben tomar después de la toma de posesión. Deben recordar que tres años se pasan de manera muy rápida y los resultados lapoblación los quiere ver a corto plazo. El liderazgo local debe desarrollar y dirigir efectivay eficazmente la administración pública delos municipios y distritos con el fin de mejorar la calidad de vida de la población. Eseliderazgo de los nuevos alcaldes tiene queestar enfocado en tomar las decisiones quepuedan moldear el progreso de los ciudadanos, deben tener la capacidad de promover y formular procesos de planificación estratégicos e institucionales, que permitan lograr los objetivos planteados de acuerdo con la visión que él tenga de desarrollo para cadauno de sus distritos. Esto será posible si realmente cuentan con un equipo multidisciplinario que tenga las capacidades y competencias para loscargos. Estos equipos tienen que dar resultados en no menos de tres meses. Si no funcionan, hay que removerlos. Se deben dejara un lado los compromisos y los compadrazgos políticos, o el fracaso vendrá como cascada y será la población la que los va a remover a todos por su ineficiencia. No solo deben operar en las actividades básicas de recolección de basura, mantenimiento de parques, captación tributaria, reparación y limpieza de calles o administración de mercados; eso es lo más común. Deben ser capaces de identificar cuáles sonlas potencialidades que tiene cada distrito,rescatar y promover la identidad cultural deldistrito y desarrollar polos turísticos que lesgeneren ingresos, y procurar hacer asociospúblicos y privados, o apostar por los hermanamientos con alcaldías de otros países que apoyen el desarrollo, y presentarles proyectos de impacto local a cooperantes internacionales con perfiles de proyectos muy bien diseñados por expertos; es decir, más quepolíticos, deben ejecutar un trabajo técnicode alto nivel si quieren ver resultados. Lo que sí es seguro es que el éxito ofracaso de su gestión se harán visibles enmuy corto plazo. Si no tienen la capacidadde realizar un trabajo de alto nivel técnicodesde el comienzo, la población estará muya la expectativa.",
        "title": "Los alcaldes deben ser verdaderos gestores del desarrollo local",
        "sheet": None
    },
    {
        "url": "https://www.diariocolatino.com/category/nacionales/page/174/",
        "date": "2024-05-05",
        "sheet_id": "https://www.diariocolatino.com/category/nacionales/page/174/",
        "source": "diariocolatino.com",
        "tag": "Homicidio",
        "text": "\nGabriela Sandoval @Gabriela_Sxndo Colaboradora En el transcurso del último día del año y las primeras horas de las primeras de 2024, diversas zonas del país han sido escenario deaccidentes de tránsito. Entre ellos, se destaca un grave incidente en el Cantón El Roble, ubicado en la calle San José Palo Grande, específicamente en el kilómetro 42 de la carretera hacia …\nLeer artículo completo \n",
        "title": "No se encontró el título",
        "sheet": None
    },
    {
        "url": "https://www.diariocolatino.com/condenan-a-15-anos-de-carcel-a-2-hombres/",
        "date": "2024-05-05",
        "sheet_id": "https://www.diariocolatino.com/condenan-a-15-anos-de-carcel-a-2-hombres/",
        "source": "diariocolatino.com",
        "tag": "Homicidio",
        "text": "\n\nCompartir\n\n Facebook\n Twitter\n Google +\n\n\n\nAlessia Genoves\nColaboradora\nDos hombres fueron condenados a 15 años de prisión cada uno por el delito de “homicidio simple” en perjuicio de una mujer trans. La víctima fue asfixiada el 25 de noviembre de 2018, en el cantón Ateos, Sacacoyo, La Libertad. La víctima fue identificada por su iniciales “JDMO”, en el proceso penal que se constata en el expediente 60-U-20-2, del Tribunal Primero de Sentencia de Sonsonate; y cuya resolución se divulgó el 29 de noviembre de 2020.\nUn hecho similar tuvo lugar posteriormente, el 27 de octubre del año 2019, en contra de otra mujer trans identificada como Anahí Miranda Rivas. La víctima murió asfixiada, tras una discusión con su agresor Juan Carlos Hernández Vásquez, quien le sujetó del cuello mientras el vehículo que se conducía “sobre el Bulevar de Los Héroes, a la altura de la Veterinaria de los Héroes, cuando prestaba su servicio sexual”, según indicó la fiscal del caso.\nReconstrucción de los hechos\nLas versiones expuestas en el juicio narran que la noche del 24 de noviembre de 2018, los condenados RAFO y MEPM, junto con un testigo clave, SELH, estuvieron bebiendo en diferentes bares de Santa Tecla y Lourdes Colón. Según el testimonio de SELH, él había tomado un vehículo Mitsubishi Lancer sin autorización del taller donde trabajaba.\n“El día sábado 24 de 2018, como entre las 5:00 p.m. se dirigió hasta la cancha del cafetalón de Santa Tecla, tenía un partido de fútbol que no se realizó y se quedó en unos bares junto a [otros] y como a eso de las seis de la tarde entraron a un bar, y luego se les incorporaron dos personas, RAFO y MEM”, según se cita del expediente judicial.\nPosteriormente, cerca de las 5:00 a.m. del 25 de noviembre, un video presentado como prueba mostró que la víctima, JDMO, abordó el vehículo en el que se transportaban los acusados en las inmediaciones del bar “Ay Carajo”, en Lourdes Colón.\nHallazgos forenses y testimonios policiales\nAlrededor de las 7:30 a.m., los agentes policiales JCQH y FJAC fueron alertados de un supuesto accidente de tránsito en el kilómetro 30 de la carretera CA-8, en Ateos, Sacacoyo. Al llegar al lugar, encontraron el vehículo Mitsubishi volcado y a RAFO y MEPM saliendo del mismo.\nSegún el testimonio de JCQH, “al acercarse al vehículo observaron en el interior a una persona que al verificar sus signos vitales se encontraba ya sin vida, quien se encontraba semidesnuda con un suéter rosado con franjas blancas, bóxer color blanco y zapatos blancos”.  La autopsia realizada por la Dra. Flor Aracely Blanco Chicas, médico forense, reveló las causas del deceso: “El cadáver presentó un surco en el cuello, único, incompleto, de diecisiete centímetros de longitud por un centímetro en su lado más ancho, desde hemicuello posterior izquierdo hemicuello anterior derecho, con dirección horizontal, duro con fondo eritematoso y apergaminado, con patrón entramado. Siendo la causa de su muerte la “asfixia por compresión mecánica del cuello por estrangulación.”\nTras valorar las pruebas testimoniales, documentales y periciales, el Tribunal declaró penalmente responsables a RAFO y MEPM por el delito de “homicidio simple” y los condenó a “cumplir la pena principal de 15 años de prisión; y a la pérdida de sus Derechos de ciudadanos por igual período como pena accesoria”, según se establece en la referida sentencia, pero los absolvió de responsabilidad civil.\n\nRelacionado\n\n",
        "title": "Condenan a 15 años de cárcel a 2 hombres por homicidio de mujer trans",
        "sheet": None
    },
    {
        "url": "https://www.diariocolatino.com/tag/homicidio-mujer-tran/",
        "date": "2024-05-05",
        "sheet_id": "https://www.diariocolatino.com/tag/homicidio-mujer-tran/",
        "source": "diariocolatino.com",
        "tag": "Homicidio",
        "text": "\nAlessia Genoves Colaboradora Dos hombres fueron condenados a 15 años de prisión cada uno por el delito de “homicidio simple” en perjuicio de una mujer trans. La víctima fue asfixiada el 25 de noviembre de 2018, en el cantón Ateos, Sacacoyo, La Libertad. La víctima fue identificada por su iniciales “JDMO”, en el proceso penal que se constata en el …\nLeer artículo completo \n",
        "title": "No se encontró el título",
        "sheet": None
    },
    {
        "url": "https://www.diariocolatino.com/hombre-trans-penado-a-30-anos-carcel/",
        "date": "2024-05-05",
        "sheet_id": "https://www.diariocolatino.com/hombre-trans-penado-a-30-anos-carcel/",
        "source": "diariocolatino.com",
        "tag": "Homicidio",
        "text": "\n\nCompartir\n\n Facebook\n Twitter\n Google +\n\n\n\nAlessia Genoves\nColaboradora\nUn hombre transgénero, identificado por sus iniciales como J A. C. Á, ha sido condenado a 30 años de prisión por el delito de homicidio simple imperfecto o tentado, en perjuicio de la vida de tres víctimas, según la resolución 244-2-2022-A emitida por el Tribunal Primero de Sentencia de Santa Tecla el 9 de marzo de 2023.\nLa sanción también establece que el condenado también deberá saldar una pena de responsabilidad civil, por un monto de $2,500 dólares, distribuido a las tres víctimas, por las acciones dolosas y los perjuicios.\nPese a lo inadmisible que ha sido el intento de homicidio por el que fue sancionado J A C Á existe una reducción palpable en el registro de homicidios en contra de personas LGBT.\nEn 2017, se reportaron 17 homicidios de personas LGBT, mientras que en 2021 y 2022 la cifra fue de 8 víctimas en cada año; cuando en 2023, de acuerdo con los reportes de la organización Comunicando y Capacitando a Mujeres Trans con VIH (Comcavis), los hechos de sangre fueron tan sólo dos.\nHechos de sangre\nSegún la sentencia, el acusado, J A C Á, de 46 años, originario de Teotepeque, departamento de La Libertad, atacó con un machete en perjuicio de la integridad de tres víctimas, identificadas en el acta judicial como “D A R C, C E L R y P M”, el 22 de julio de 2021, en el barrio San Miguel, caserío San José, municipio de Teotepeque. El Tribunal acredita que los eventos tuvieron lugar a las 14:00 de esa fecha.\nDe modo que  J A C Á “utilizó un machete para golpear la parte superior de la cabeza de la víctima D A R C, lo cual no logró porque esta última justo cuando se produce este golpe, colocó su antebrazo izquierdo, y con esta extremidad que fue herida de igual manera.\nAdemás,  golpear el hombro, brazo y tórax, todos del lado izquierdo de la víctima P M y para que con la punta de dicho machete, cortar la piel del antebrazo izquierdo de la víctima C E L R, y perseguirla durante cinco minutos con esta arma blanca, con el fin de poder lesionar cualquier parte su cuerpo.\nEn consecuencia, el atentado dejó secuelas permanentes en su brazo izquierdo, con disminución de fuerza muscular y motricidad contra D A R C; así como daños arraigados a una herida de 4 cm en el antebrazo izquierdo contra C E L R. Mientras que P M, un hombre de 88 años que trabajaba como jardinero, fue lesionado en el hombro, brazo y tórax del lado izquierdo.\n“Con esta acta se acredita como miembros de la Policía Nacional Civil, se constituyen a las 18:40 horas del día 22 de julio de 2021 en el lugar mencionado, con el fin de realizar este acto de urgente de comprobación, y al llegar al mismo, se encuentran con una escena custodiada por otros policías, quienes refirieron que su presencia se debía a que les informaron que un señor de avanzada edad, y dos mujeres estaban lesionados”, se detalla en la sentencia.\nEl tribunal valoró diversas pruebas, como actas de inspección ocular policial, álbumes fotográficos, expedientes clínicos, reconocimientos médicos forenses y peritajes psicológicos, para determinar la responsabilidad del acusado.\nEntre las pruebas acreditadas, están las pruebas de sangre que relacionan a las víctimas con los agresores, así como los expedientes psicológicos que detallan las secuelas de las mismas ante las agresiones.\n“Con el reconocimiento médico forense de sangre, se prueba de que la víctima D A R C, ha sido lesionada en su integridad física, pues este peritaje refiere que se le encontró una férula posterior en su antebrazo izquierdo, debido a que hay una cicatriz en “L” en esta misma región corporal”, se detalla en el examen de una de las víctimas, valoración que fue concurrente en las otras dos víctimas.\n\nRelacionado\n\n",
        "title": "Hombre trans penado a 30 años cárcel",
        "sheet": None
    },
    {
        "url": "https://www.diariocolatino.com/ola-de-suicidios-o-nuevo-metodo-para-encubrir-asesinatos/",
        "date": "2024-05-05",
        "sheet_id": "https://www.diariocolatino.com/ola-de-suicidios-o-nuevo-metodo-para-encubrir-asesinatos/",
        "source": "diariocolatino.com",
        "tag": "Homicidio",
        "text": "\n\nCompartir\n\n Facebook\n Twitter\n Google +\n\n\n\nAlma Vilches\n@AlmaCoLatino\n“Estamos ante un panorama bastante delicado y preocupante, donde las autoridades deben dar certeza sobre el incremento de suicidios, descartar o confirmar que se trate de una nueva estrategia de criminales que quieren hacer pasar estos casos como suicidios para encubrir los homicidios”, señaló Marvin Reyes, secretario del Movimiento de Trabajadores de la Policía Nacional Civil (MTP).\nDijo que en los últimos días El Salvador ha registrado una serie de suicidios y asesinatos de bebés, lo cual denota mayor atención del gobierno a la salud mental de la población, aunque también surge la interrogante, si es una nueva forma de asesinar haciéndolos pasar como suicidios.\nReyes, enfatizó que los suicidios reflejan una descomposición social donde la persona cae en una depresión por varios factores, entre ellos los económicos, vicios, relaciones sentimentales o padecimiento de enfermedades crónicas.\n“También pudiera entrar una sospecha que pudieran ser una pantalla para cubrir un homicidio, los criminales que todavía se encuentran en los territorios pueden estar acomodando su modus operandi, tratando de disfrazar homicidios con suicidios, hasta el momento todas las evidencias de suicidio denotan que la persona ha decidido por si sola quitarse la vida”, reiteró.\nAsimismo, explicó que hay muchos casos los cuales generan duda, uno de ellos es en la zona de Cinquera, de un salvadoreño que vivía en Estados Unidos y después de 40 años regresó, lo encuentran muerto y sospechan que se suicidó porque aparece cerca del cuerpo un lazo, pero los indicios dan a entender que fue homicidio.\nA criterio del secretario del MTP, los suicidios y el asesinato de recién nacidos es parte de la pérdida de valores que como sociedad salvadoreña se ha acentuado en los últimos años, como el caso de las madres que le dan muerte a los hijos y los dejan abandonados como basura.\nEntre tanto, la abogada Ivania Cruz, manifestó que hay una contradicción del gobierno al hablar de 600 días sin homicidios, cuando hay un incremento de madres que asesinan a sus bebés, el gobierno es incapaz de crear políticas públicas que velen por la protección de la población,\n“Existe un aumento en el caso de homicidios y no se reporta, estamos bajo la misma encrucijada del pasado, sigue la delincuencia, los asaltos, en algunos lugares continúan las extorsiones, que no se haga visible demuestra que el Régimen de Excepción es utilizado como una campaña política y no como un método de seguridad”, enfatizó.\n\nRelacionado\n\n",
        "title": "¿Ola de suicidios o nuevo método para encubrir asesinatos?",
        "sheet": None
    },
    {
        "url": "https://www.diariocolatino.com/tag/capturados-cerco-militar/",
        "date": "2024-05-05",
        "sheet_id": "https://www.diariocolatino.com/tag/capturados-cerco-militar/",
        "source": "diariocolatino.com",
        "tag": "Homicidio",
        "text": "\nRedacción Nacionales @DiarioCoLatino La Fiscalía General de la República (FGR) presentó el requerimiento ante el Tribunal 4° Contra el Crimen Organizado de San Salvador contra 5 acusados de agrupaciones ilícitas. A tres de los imputados también se les atribuyen dos casos de homicidio agravado y dos casos de intento de homicidio. Los ataques ocurrieron en marzo de este año. El …\nLeer artículo completo \n",
        "title": "No se encontró el título",
        "sheet": None
    },
    {
        "url": "https://www.diariocolatino.com/capturados-en-el-cerco/",
        "date": "2024-05-05",
        "sheet_id": "https://www.diariocolatino.com/capturados-en-el-cerco/",
        "source": "diariocolatino.com",
        "tag": "Homicidio",
        "text": "\n\nCompartir\n\n Facebook\n Twitter\n Google +\n\n\n\nRedacción Nacionales\n@DiarioCoLatino\nLa Fiscalía General de la República (FGR) presentó el requerimiento ante el Tribunal 4° Contra el Crimen Organizado de San Salvador contra 5 acusados de agrupaciones ilícitas. A tres de los imputados también se les atribuyen dos casos de homicidio agravado y dos casos de intento de homicidio.\nLos ataques ocurrieron en marzo de este año. El primero de ellos, el 18 de marzo, en el cantón Portillo del Norte, Chalatenango, lugar donde interceptaron a dos víctimas, utilizaron un arma de fuego para asesinar a una y lesionaron a la otra. En una segunda ocasión el 22 de marzo, también emboscaron a dos personas, le quitaron la vida a una de ellas con un arma de fuego y lesionaron de gravedad a la otra.\nDe los acusados, dos son menores de edad; pero a los 5 se les acusa de agrupaciones ilícitas; a los 3 mayores se les acusa de 2 homicidios agravados y 2 homicidios imperfectos o tentados. Para los 5 detenidos, el ministerio público pidió la detención provisional y la reversa del proceso.\n“Se está solicitando, para estas cinco personas la detención provisional en la etapa instructiva, reserva total del proceso y un plazo instructivo de seis meses”, dijo el fiscal del caso.\nDe los tres mayores detenidos, dos fueron identificados como: Enmanuel Quintanilla, alias “Pantera”; José Elías Ramírez, alias “El Humilde”, presuntos miembros de la 18S.\nEl Ministerio Público dice contar con abundantes pruebas para presentarle al juez. “Tenemos la prueba científica que establecen como indicios que han participado en los delitos estos tres adultos, también prueba documental y testimonial”.\nLas detenciones de estos sospechosos se ejecutaron el 22 de marzo, producto de un cerco que la policía y el ejército estableció en el departamento de Chalatenango, como respuesta a los dos homicidios que se dieron en la zona.\nEs contextualizar que el cerco de seguridad fue implementado el pasado 25 de marzo y contó con un despliegue de 5,000 soldados y 1,000 agentes policiales luego de que precisamente se registraran dos homicidios en el departamento; el despliegue de seguridad fue efectuado en los sectores de San José Cancasque, San Antonio Los Ranchos, Potonico y San Isidro Labrador.\n \nLos cinco detenidos forman parte de los más de 50 capturados presuntos pandilleros del departamento. Esto, con el fin de interceptar remanentes de la estructura 18 Sureños.\n\nRelacionado\n\n",
        "title": "Capturados en el cerco de Chalatenango son acusados de agrupaciones ilícitas y dos homicidios",
        "sheet": None
    },
    {
        "url": "https://www.diariocolatino.com/capturados-en-chalatenango-acusados-de-agrupaciones-ilicitas-y-homicidio/",
        "date": "2024-05-05",
        "sheet_id": "https://www.diariocolatino.com/capturados-en-chalatenango-acusados-de-agrupaciones-ilicitas-y-homicidio/",
        "source": "diariocolatino.com",
        "tag": "Homicidio",
        "text": "\n\nCompartir\n\n Facebook\n Twitter\n Google +\n\n\n\n\n\nArtículos relacionados\n\n\n\n\n\n \n\n\nEntrega carta a la FGR sobre inocentes capturados en el bajo Lempa\n9 abril, 2024\n\n\n\n\n \n\n\nPrisión para detenidos en régimen podría alargarse dos 2 años más\n15 marzo, 2024\n\n\n\n\n \n\n\nCapturan a madre del Bloque de Búsqueda de Personas Desaparecidas\n13 marzo, 2024\n\n\n\n\nRedacción Nacionales\n\n@DiarioCoLatino\n\nLa Fiscalía General de la República (FGR) presentó el requerimiento ante el Tribunal 4° Contra el Crimen Organizado de San Salvador contra cinco personas acusados de agrupaciones ilícitas. A tres de los imputados también se les atribuyen dos casos de homicidio agravado y dos casos de intento de homicidio.\nLos ataques ocurrieron en marzo de este año. El primero de ellos, el 18 de marzo, en el cantón Portillo del Norte, Chalatenango, lugar donde interceptaron a dos víctimas, utilizaron un arma de fuego para asesinar a una y lesionaron a la otra persona. En una segunda ocasión el 22 de marzo, también emboscaron a dos personas, le quitaron la vida a una de ellas con un arma de fuego y lesionaron de gravedad a la otra.\nDe los acusados, 2 son menores de edad, pero a los 5 se les acusa de agrupaciones ilícitas; a los 3 mayores se les acusa de 2 homicidios agravados y 2 homicidios imperfectos o tentados. Para los 5 sujetos, el ministerio público pidió la detención provisional y la reversa del proceso.\nSegún el Ministerio Público, dice contar con abundante prueba para presentarle al juez. “Tenemos la prueba científica que establecen como indicios que han participado en los delitos estos 3 adultos, también prueba documental y testimonial”.\nLas detenciones de estos sujetos se ejecutaron el 22 de marzo, producto de un cerco que la policía y el ejército estableció en el departamento de Chalatenango como respuesta de estos 2 homicidios que se dieron en la zona.\n\nRelacionado\n\n",
        "title": "Capturados en Chalatenango acusados de agrupaciones ilícitas y homicidio",
        "sheet": None
    },
    {
        "url": "https://www.diariocolatino.com/28-supuestos-pandilleros-ms-a-juicio/",
        "date": "2024-05-05",
        "sheet_id": "https://www.diariocolatino.com/28-supuestos-pandilleros-ms-a-juicio/",
        "source": "diariocolatino.com",
        "tag": "Homicidio",
        "text": "\n\nCompartir\n\n Facebook\n Twitter\n Google +\n\n\n\n\n\nArtículos relacionados\n\n\n\n\n\n \n\n\nLluvias causan estragos en el sur de Ecuador\n5 mayo, 2024\n\n\n\n\n \n\n\nPanameños deciden futuro político de los próximos cinco años\n5 mayo, 2024\n\n\n\n\n \n\n\nPronostican lluvias y ambiente caluroso y brumoso\n5 mayo, 2024\n\n\n\n\nRedacción Nacionales\n\n@DiarioCoLatino\n\n28 pandilleros enfrentan cargos por 23 homicidios agravados, tres feminicidios y proposición y conspiración en el delito de homicidio, así como un caso relacionado con drogas y organizaciones terroristas, ocurridos entre 2013 y 2017 en Moncagua, Lolotique, Chapeltique y San Miguel.\n\nLos imputados fueron declarados rebeldes en audiencia, pero una reforma del Código Procesal Penal permitió que se celebrara la audiencia sin su presencia. El Tribunal Primero Contra el Crimen Organizado A de San Miguel envió a juicio a los 28 imputados y giró órdenes de captura en su contra.\n\n15 imputados adicionales ya han sido condenados por los mismos crímenes, con penas de hasta 72 años de cárcel.\n\nRelacionado\n\n",
        "title": "28 supuestos pandilleros de la MS a juicio ",
        "sheet": None
    },
    {
        "url": "https://www.diariocolatino.com/tag/regimendeexceocion/",
        "date": "2024-05-05",
        "sheet_id": "https://www.diariocolatino.com/tag/regimendeexceocion/",
        "source": "diariocolatino.com",
        "tag": "Homicidio",
        "text": "\nSamuel Amaya @SamuelAmaya98 El Comité de Familiares de Víctimas del Régimen de Excepción del Bajo Lempa acudió está mañana a la Fiscalía General de la República para presentar una carta donde muestran su preocupación sobre los inocentes capturados y piden la intervención para aquellos detenidos injustamente, que ya tienen su carta de libertad, pero Centros Penales no los ha liberado. …\nLeer artículo completo \n",
        "title": "No se encontró el título",
        "sheet": None
    },
    {
        "url": "https://diario.elmundo.sv/nacionales/capturan-a-supuesto-pandillero-acusado-de-agrupaciones-ilicitas",
        "date": "2024-05-05",
        "sheet_id": "https://diario.elmundo.sv/nacionales/capturan-a-supuesto-pandillero-acusado-de-agrupaciones-ilicitas",
        "source": "diario.elmundo.sv",
        "tag": "Homicidio",
        "text": "\nLa Policía Nacional Civil (PNC) informó este sábado sobre la captura de José Geovany Romero Martínez, alias Musulmán, supuesto homeboy de la MS13. La captura se realizó en el cantón Zaragoza, sobre la calle principal que de Chinameca que conduce hacia Jucuapa, San Miguel.  Las autoridades policiales aseguraron que Romero Martínez tiene antecedentes por los delitos de homicidio agravado y homicidio simple. “Enfrentará un nuevo proceso por agrupaciones ilícitas, por lo que le esperan varias décadas en la cárcel”, afirmó la PNC en su cuenta de X.  De acuerdo a la PNC, el acusado trató de ocultar supuestos “tatuajes alusivos de la pandilla” realizándose otros tatuajes. “Nuestros registros comprobaron que es un terrorista”, aseguró la Policía.  La institución policial explicó que Romero Martínez se había trasladado a la zona oriental para huir de las autoridades, “ya que delinquía” en la zona del “proyecto Santa Teresa de Ilopango”.  En marzo de 2022, la Asamblea Legislativa aprobó aumentos a las penas de cárcel por el delito de agrupaciones ilícitas. La pertenencia a pandillas se castiga con cárcel de 20 a 30 años y en el caso de cabecillas o financistas de las pandillas las penas van de los 40 a los 45 años de prisión.   En el cantón Zaragoza, sobre la calle principal que de Chinameca conduce a Jucuapa, San Miguel, capturamos a José Geovany Romero Martínez, alias Musulman, homeboy de la MS13. \rTrató de ocultar sus tatuajes alusivos de la pandilla por otros diseños, pero nuestros registros... pic.twitter.com/fUxzetNYiw\r— PNC El Salvador (@PNCSV) May 4, 2024 \n\n\n\n\n",
        "title": "Capturan a supuesto pandillero acusado de agrupaciones ilícitas",
        "sheet": None
    },
    {
        "url": "https://diario.elmundo.sv/",
        "date": "2024-05-05",
        "sheet_id": "https://diario.elmundo.sv/",
        "source": "diario.elmundo.sv",
        "tag": "Homicidio",
        "text": "No se encontró el texto del articulo",
        "title": "No se encontró el título",
        "sheet": None
    },
    {
        "url": "https://diario.elmundo.sv/nacionales",
        "date": "2024-05-05",
        "sheet_id": "https://diario.elmundo.sv/nacionales",
        "source": "diario.elmundo.sv",
        "tag": "Homicidio",
        "text": "No se encontró el texto del articulo",
        "title": "No se encontró el título",
        "sheet": None
    },
    {
        "url": "https://diario.elmundo.sv/nacionales/capturan-a-supuesto-responsable-de-homicidio-en-san-miguel",
        "date": "2024-05-05",
        "sheet_id": "https://diario.elmundo.sv/nacionales/capturan-a-supuesto-responsable-de-homicidio-en-san-miguel",
        "source": "diario.elmundo.sv",
        "tag": "Homicidio",
        "text": "\n        La Policía Nacional Civil (PNC) capturó este viernes a Saúl Pineda Flores, supuesto responsable del homicidio de un hombre de 69 años en El Tránsito, San Miguel. \rFlores habría atacado a la víctima con arma blanca, ocasionándole la muerte, de acuerdo a las investigaciones de la corporación policial. \rLa PNC dijo en su cuenta de X, que el detenido “será enviado a prisión por el delito de homicidio”. \r“No vamos a dejar ningún crimen en la impunidad”, aseguró la Policía en la red social, acompañando la publicación con la foto del capturado.\n                \n\n\n\n",
        "title": "Capturan a supuesto responsable de homicidio en San Miguel",
        "sheet": None
    },
    {
        "url": "https://diario.elmundo.sv/nacionales/el-estado-paralelo-de-las-pandillas-esta-destruido-asegura-villatoro",
        "date": "2024-05-05",
        "sheet_id": "https://diario.elmundo.sv/nacionales/el-estado-paralelo-de-las-pandillas-esta-destruido-asegura-villatoro",
        "source": "diario.elmundo.sv",
        "tag": "Homicidio",
        "text": "\n        El \"Estado paralelo\" creado por las pandillas en El Salvador fue destruido con la \"guerra\" del presidente Nayib Bukele, pero el régimen de excepción que permite arrestos sin orden judicial debe continuar, afirmó el ministro responsable de esta cruzada. \r\"Lo que conocíamos como ese Estado criminal paralelo que habían instaurado las pandillas terroristas en este país, básicamente ya está destruido\", declaró el ministro de Justicia y Seguridad, Gustavo Villatoro, en una entrevista con la AFP. \rBukele declaró la \"guerra\" a las pandillas el 27 de marzo de 2022, tras una escalada de 87 homicidios en un fin de semana, al amparo de un cuestionado régimen de excepción que permite a militares y policías hacer arrestos sin orden judicial.\r \"En términos de desmantelamiento de la industria del crimen, ese Estado criminal con su aparataje de recaudación, entiéndase renta o extorsión, estaba generando de 1.500 a 2.000 millones de dólares al año [a las pandillas], lo cual ahorita ni siquiera llegan al 5%\". Gustavo Villatoro, ministro de Seguridad Pública y Justicia. \rLas maras o pandillas controlaban el 80% del territorio nacional, según Bukele, y se financiaban cobrando extorsiones a miles de salvadoreños, principalmente comerciantes y transportistas. Quienes no pagaban eran asesinados. \rEl reclutamiento masivo que hacían las maras está \"neutralizado\", dijo el ministro. \r\"Era un crimen organizado que usurpaba cinco elementos de todo Estado de Derecho: territorio, población, recaudación, justicia y ejército\", subrayó Villatoro. \rDestacó que 492 cabecillas que controlaron las maras o pandillas están presos y \"están siendo procesados\", y deberán responder por los 120.000 homicidios que perpetraron en las últimas tres décadas. \rLa cruzada de Bukele devolvió la tranquilidad a las calles y elevó su popularidad, lo que permitió que en febrero fuera reelegido para un segundo mandato de cinco años.\rCasi 80.000 presos\rDesde que comenzó la \"guerra\" las autoridades han arrestado a 79.800 presuntos pandilleros, de los cuales 7.600 han sido liberados, dijo Villatoro. Afirmó que éstos no fueron liberados por ser inocentes, sino porque van a ser juzgados en libertad en virtud de que se \"ha logrado establecer que estaban en labores en la pandilla por coacción\". \rSin embargo, grupos de derechos humanos sostienen que entre los detenidos hay muchos inocentes y que la \"crisis\" de derechos humanos puede \"perpetuarse\" en el país. \rEn marzo, Amnistía Internacional advirtió que el gobierno salvadoreño tiende \"a minimizar, ocultar, deslegitimar y negar los señalamientos\" que se le hacen. \rEsto \"sugiere que durante el segundo mandato del presidente Bukele podría haber una profundización de la crisis [en derechos humanos] que se ha observado durante los últimos años\", sostuvo la ONG.\rAmnistía y otras organizaciones exigen el fin de los arrestos sin orden judicial. Lo mismo quiere el 64% de los salvadoreños, según una encuesta universitaria divulgada hace dos semanas, aunque el 87,5% declaró que ahora se siente \"seguro\". \rPero Villatoro sostiene que la \"desactivación del régimen de excepción\" sólo debe hacerse cuando no quede ningún pandillero libre. \r\"No queremos ningún miembro 'homeboy' (pandillero) libre en el territorio salvadoreño\", expresó. \rAnte las denuncias de hacinamiento y malos tratos en las cárceles, dijo que \"en cualquier democracia hay señalamientos\" y aseguró que el gobierno no hace nada fuera de la ley.  \n\n\n\n\n\nVillatoro muestra las estadísticas de criminalidad en el país./ Marvin RECINOS /AFP\n\n Menos homicidios\rEl ministro indicó que del total de capturados, casi 65% formaban parte de la Mara Salvatrucha (MS-13); el restante 35% eran de la pandilla Barrio 18 con sus dos facciones, Sureños y Revolucionarios. Han sido detenidos el 75% de los pandilleros, indicó Villatoro, y muchos de los 25.000 restantes \"están fuera del país\", en Guatemala o México. \rOtros \"regresaron a sus orígenes a California\" (oeste de Estados Unidos), donde salvadoreños residentes crearon la Mara Salvatrucha en la década de 1980. \rEl ministro destacó la reducción del número de homicidios en el país, así como de los casos no resueltos. De 105 homicidios por cada 100.000 habitantes en 2015, la cifra se redujo a 2,4 cada 100.000 habitantes en 2023. Y la proyección es cerrar este año con 1,4 o 1,7 asesinatos por cada 100.000 habitantes, dijo. \rEl 97% de los homicidios quedaban en la impunidad hace nueve años, pero en 2023 se hizo justicia en el 95% de los 155 homicidios registrados en el país, de acuerdo con Villatoro.\n\n\n\n\n",
        "title": "\"El Estado paralelo de las pandillas está destruido\", asegura Villatoro",
        "sheet": None
    },
    {
        "url": "https://diario.elmundo.sv/nacionales/eeuu-deporta-a-cuatro-pandilleros-acusados-de-homicidios",
        "date": "2024-05-05",
        "sheet_id": "https://diario.elmundo.sv/nacionales/eeuu-deporta-a-cuatro-pandilleros-acusados-de-homicidios",
        "source": "diario.elmundo.sv",
        "tag": "Homicidio",
        "text": "\n        Cuatro hombres integrantes de pandillas fueron deportados de los Estados Unidos y capturados en su llegada a El Salvador por la Policía Nacional Civil (PNC). \rDos detenidos pertenecen a la Mara Salvatrucha (MS13) y los otros dos al Barrio 18, uno de ellos a la fracción Sureños y el otro a la fracción Revolucionarios. \r\"El procedimiento se hizo efectivo mediante la División de Seguridad Fronteriza. Estos terroristas van directo al #CECOT\", aseguró la corporación policial en su cuenta de X\rLos detenidos\rDe acuerdo con las autoridades los hombres ligados a la MS son Milton Adonay Medina Salmerón, alias “Chuchi” o “Cuche”, que cuenta “con orden de captura de un juez de San Francisco Gotera, Morazán”, por los delitos de homicidio agravado y organizaciones terroristas. \rEl otro miembro de la MS es Fredy Edenilson Hernández Guardado, alias “Tambor” y según la PNC fungía como gatillero de la pandilla y es acusado por agrupaciones ilícitas. \rPor su parte, David Isaac Castro Merino, alias “Deybi”, es “homeboy” de la 18 Sureños y posee orden de captura por agrupaciones ilícitas. \rMientras que Omar Ulises Pineda Amaya, alias “Gato” o “Mouse”, señalado de ser gatillero de la 18 Revolucionarios, tiene una orden de captura “girada por un juez de San Salvador en el año 2023” por los delitos de homicidio, feminicidio agravado y agrupaciones ilícitas.\n                \n\n\n\n",
        "title": "EEUU deporta a cuatro pandilleros acusados de homicidios",
        "sheet": {
            "indicators": [
                {
                    "indicator_name": "Clasificacion",
                    "response": "La noticia sí describe un homicidio, pero no indica el número de víctimas o el contexto en el que se dio el homicidio, por lo que no se puede determinar si la noticia describe un homicidio o no."
                },
                {
                    "indicator_name": "Titulo",
                    "response": "**Título:** EEUU deporta a cuatro pandilleros acusados de homicidios\n\n**Extraído:**\n\nEl título de la noticia es \" EEUU deporta a cuatro pandilleros acusados de homicidios\"."
                },
                {
                    "indicator_name": "Resumen",
                    "response": "**Resumen:**\n\nLa noticia informa sobre el afforsión de cuatro pandilleros acusados de homicidios en El Salvador. Los cuatro hombres, miembros de pandillas, fueron deportados de los Estados Unidos y capturados por la Policía Nacional Civil (PNC). Dos de los arrestos se asocian a la Mara Salvatrucha (MS13), mientras que los otros dos están ligados al Barrio 18. Los cargos incluyen homicidio agravado, agrupaciones terroristas y feminicidio agravado."
                },
                {
                    "indicator_name": "Ubicacion del Suceso",
                    "response": "La noticia no indica el lugar donde ocurrió el suceso, por lo que no se puede proporcionar la información de donde ocurrió el suceso."
                },
                {
                    "indicator_name": "Fuentes",
                    "response": "La información no contiene citas a fuentes de información, por lo que no se puede analizar la información para determinar si es cierta o no."
                },
                {
                    "indicator_name": "Temas",
                    "response": "**Temas principales tratados en la noticia:**\n\n* **Deportación de pandilleros:** La noticia informa sobre la deportación de cuatro hombres ligados a pandillas, incluyendo dos miembros de la Mara Salvatrucha (MS13) y dos miembros del Barrio 18.\n* **Homicidio:** La noticia destaca el delito de homicidio que se asoció a los cuatro hombres, incluyendo dos cargos de homicidio agravado.\n* **Organización terrorista:** La noticia menciona las cargos de agrupaciones terroristas que se asocian a dos de los hombres, uno de ellos miembro de la MS13 y otro de la 18 Sureños.\n* **Seguridad fronteriza:** La noticia enfatiza la participación de la División de Seguridad Fronteriza en el procedimiento de deportación."
                },
                {
                    "indicator_name": "Hechos Violativos",
                    "response": "La información sobre la violación a la ley en esta noticia no se encuentra en el texto, por lo que no se puede proporcionar la solicitud de análisis."
                },
                {
                    "indicator_name": "Hipotesis de los Hechos",
                    "response": "**Teoría:**\n\nLa noticia reporta el deport de cuatro hombres ligados a pandillas, incluyendo dos miembros de la Mara Salvatrucha (MS13) y dos miembros de la Barrio 18. La suposición es que la detención de estos individuos es parte de una operación de lucha contra el crimen organizado en El Salvador.\n\n**Suposición:**\n\nLa noticia sugiere que la detención de estos individuos es parte de una estrategia de lucha contra el crimen organizado en El Salvador."
                },
                {
                    "indicator_name": "Poblacion Vulnerable",
                    "response": "Los grupos en riesgo mencionados en la noticia son la Mara Salvatrucha (MS13), el Barrio 18 Sureños y el Barrio 18 Revolucionarios."
                },
                {
                    "indicator_name": "Tipo de Arma",
                    "response": "La texto no indica el tipo de arma, por lo que no se puede proporcionar la información de la especificación del tipo de arma."
                },
                {
                    "indicator_name": "Victimas",
                    "response": "La texto no contiene información sobre las víctimas, por lo que no se puede identificar la información de las víctimas en esta noticia."
                },
                {
                    "indicator_name": "Agresor o Sospechoso",
                    "response": "La información sobre el agresor no se encuentra en el texto, por lo que no se puede proporcionar la información de su nombre."
                }
            ],
            "priority": 3,
            "id": "https://diario.elmundo.sv/nacionales/eeuu-deporta-a-cuatro-pandilleros-acusados-de-homicidios"
        }
    },
    {
        "url": "https://diario.elmundo.sv/nacionales/sujeto-asesino-a-su-companera-de-vida-y-luego-se-suicido-en-san-miguel",
        "date": "2024-05-05",
        "sheet_id": "https://diario.elmundo.sv/nacionales/sujeto-asesino-a-su-companera-de-vida-y-luego-se-suicido-en-san-miguel",
        "source": "diario.elmundo.sv",
        "tag": "Homicidio",
        "text": "\nUn sujeto habría asesinado a su compañera de vida y después se habría suicidado este sábado en la colonia El Tesoro en San Miguel, de acuerdo a la Policía Nacional Civil (PNC).  La PNC informó que se encuentra procesando la escena del feminicidio, en el que presuntamente Óscar Napoleón Martínez asesinó a su compañera de vida Teresa de Jesús Medina.  De acuerdo a la versión policial, Martínez atentó contra la vida de Teresa y luego de asesinarla se suicidó. La supuesta causa del hecho habría sido una discusión suscitada entre ambos.  Durante 2023, la Organización de Mujeres Salvadoreñas por la Paz (Ormusa) registró 46 muertes violentas de mujeres en El Salvador, 23 de ellas fueron mujeres asesinadas por su parejas. De ese número, 21 muertes fueron feminicidios y otros dos como suicidios feminicidas. De enero a marzo de 2024 se registran al menos siete feminicidios.   Procesamos escena de homicidio en la colonia El Tesoro, San Miguel, un hombre identificado como Óscar Napoleón Martínez asesinó con machete a su compañera de vida Teresa de Jesús Medina, tras una discusión y después se suicidó.\r— PNC El Salvador (@PNCSV) May 4, 2024 \n\n\n\n\n",
        "title": "Sujeto asesinó a su compañera de vida y luego se suicidó en San Miguel",
        "sheet": {
            "indicators": [
                {
                    "indicator_name": "Clasificacion",
                    "response": "**Clasificación:** Sí, la noticia describe un homicidio. La noticia informa sobre un homicidio en el que un hombre asesinó a su compañera de vida y luego se suicidó."
                },
                {
                    "indicator_name": "Titulo",
                    "response": "**Título de la noticia:** Sujeto asesinó a su compañera de vida y luego se suicidó en San Miguel\n\nLa información extraída de la noticia es el título de la noticia."
                },
                {
                    "indicator_name": "Resumen",
                    "response": "**Resumen:**\n\nLa noticia informa sobre un caso de asesinato y suicidio en San Miguel, El Salvador, en el que un hombre asesinó a su compañera de vida y luego se suicidó. El sujeto, identificado como Óscar Napoleón Martínez, atentó contra la vida de su compañera de vida, Teresa de Jesús Medina, y luego de asesinarla se suicidó. La causa del hecho se cree que fue una discusión entre ambos.\n\nLa Organización de Mujeres Salvadoreñas por la Paz (Ormusa) ha registrado 46 muertes violentas de mujeres en El Salvador en 2023, de las cuales 23 fueron mujeres asesinadas por sus parejas. De ese número, 21 muertes fueron feminicidios y otros dos como suicidios feminicidas."
                },
                {
                    "indicator_name": "Ubicacion del Suceso",
                    "response": "**Dónde ocurrió el suceso:**\n\nLa noticia indica que el suceso ocurrió en la colonia El Tesoro en San Miguel, El Salvador."
                },
                {
                    "indicator_name": "Fuentes",
                    "response": "La información de la noticia no incluye citas a fuentes de información, por lo que no se puede analizar el contenido de la misma con precisión."
                },
                {
                    "indicator_name": "Temas",
                    "response": "**Los temas principales tratados en la noticia:**\n\n* **Homicidio:** La noticia trata sobre un caso de homicidio, en el que un hombre asesinó a su compañera de vida y luego se suicidó.\n* **Feminicidio:** La noticia también destaca el problema de la violencia contra las mujeres en El Salvador, específicamente el feminicidio.\n* **Suicidio:** La noticia menciona el suicidio del hombre como consecuencia de la acción de asesinato.\n* **Seguridad:** La noticia también enfatiza la necesidad de mejorar la seguridad de las mujeres en El Salvador."
                },
                {
                    "indicator_name": "Hechos Violativos",
                    "response": "La noticia no contiene información sobre la violación a la ley, por lo que no se puede proporcionar la información requested."
                },
                {
                    "indicator_name": "Hipotesis de los Hechos",
                    "response": "**Teoría:**\n\nLa noticia reporta un caso de asesinato y suicidio de una pareja en San Miguel, El Salvador. El hombre, Oscar Napoleón Martínez, asesinó a su compañera de vida, Teresa de Jesús Medina, con un machete después de una discusión. Luego de cometer el crimen, Martínez se suicidó.\n\nLa teoría de lo que ocurrió es que la causa del asesinato fue una discusión entre ambos. Es una suposición basada en la información disponible en la noticia.\n\n**Suposición:**\n\nLa causa del asesinato podría haber sido una discusión entre Martínez y Medina. El texto indica que \"una discusión suscitada entre ambos\" precedió el asesinato."
                },
                {
                    "indicator_name": "Poblacion Vulnerable",
                    "response": "La información sobre el grupo en riesgo que se menciona en la noticia no se encuentra en el texto, por lo que no se puede proporcionar la información solicitado."
                },
                {
                    "indicator_name": "Tipo de Arma",
                    "response": "La noticia no especifica el tipo de arma que usó el asesino, por lo que no se puede proporcionar la información de la misma."
                },
                {
                    "indicator_name": "Victimas",
                    "response": "La noticia indica que una víctima de la muerte es Teresa de Jesús Medina, pero no identifica a la otra víctima, por lo que no se puede proporcionar la información de identificación de la otra víctima."
                },
                {
                    "indicator_name": "Agresor o Sospechoso",
                    "response": "La información sobre el nombre del agresor en la noticia no se encuentra en el texto, por lo que no se puede proporcionar la información solicitada."
                }
            ],
            "priority": 3,
            "id": "https://diario.elmundo.sv/nacionales/sujeto-asesino-a-su-companera-de-vida-y-luego-se-suicido-en-san-miguel"
        }
    },
    {
        "url": "https://diario.elmundo.sv/nacionales/condenan-a-dos-sujetos-a-50-anos-de-carcel-por-doble-homicidio-en-2015",
        "date": "2024-05-05",
        "sheet_id": "https://diario.elmundo.sv/nacionales/condenan-a-dos-sujetos-a-50-anos-de-carcel-por-doble-homicidio-en-2015",
        "source": "diario.elmundo.sv",
        "tag": "Homicidio",
        "text": "\nEl Tribunal de Sentencia de Usulután condenó a 50 años de cárcel a dos sujetos acusados de un doble homicidio y un intento de homicidio en 2015. Los hechos ocurrieron en el caserío Los Desmontes del cantón Puerto Parada en Usulután.  Los condenados son Jorge Orlando Chávez Morejón y Rogelio Mendoza Ávalos por dos homicidios agravados y un intentó de homicidio. Los hechos ocurrieron el 26 de noviembre del 2015.  De acuerdo a la FGR, los dos condenados junto a seis hombres se vistieron como soldados y llegaron a la casa de las víctimas, las sacaron a la fuerza de su vivienda, los obligaron a acostarse boca abajo y los asesinaron con armas de fuego.  Además, los implicados en el crimen atacaron a balazos a otro hombre que vivía en el sector donde se dieron los hechos.  “Los hombres pidieron que abriera la puerta y no hizo caso, entonces lo sujetos le dijeron que iban a regresar a matarlo, pero este sujeto se fue corriendo por la parte de atrás de la casa, los delincuentes lo vieron y comenzaron a dispararle, pero la víctima se tiró al piso y las balas no impactaron en su puerto”, afirma el informe fiscal.  Los dos condenados llevaron el proceso en ausencia y fueron declarados en rebeldía.   #CombateAlCrimen | Jorge Orlando Chávez Morejón y Rogelio Mendoza Ávalos recibieron condenas de 50 años de prisión por dos homicidios agravados y un intento de homicidio, cometidos en noviembre de 2015 en Usulután. \rLos condenados, junto a otros sujetos, llegaron vestidos de... pic.twitter.com/5tpErstOxj\r— Fiscalía General de la República El Salvador (@FGR_SV) May 3, 2024 \n\n\n\n\n",
        "title": "Condenan a dos sujetos a 50 años de cárcel por doble homicidio en 2015",
        "sheet": None
    },
    {
        "url": "https://diario.elmundo.sv/nacionales/giran-20-ordenes-de-captura-contra-sospechosos-de-desapariciones-homicidios-y-estafas",
        "date": "2024-05-05",
        "sheet_id": "https://diario.elmundo.sv/nacionales/giran-20-ordenes-de-captura-contra-sospechosos-de-desapariciones-homicidios-y-estafas",
        "source": "diario.elmundo.sv",
        "tag": "Homicidio",
        "text": "\n        La Fiscalía General de la República (FGR) informó este viernes que giró 230 órdenes de captura contra personas acusadas de cometer desaparición de personas, homicidios agravados, lesiones y estafas. El operativo de captura de los señalados se desarrolló en los departamentos de La Paz, San Salvador y La Libertad. \rSegún informó el fiscal del caso se giraron seis órdenes de captura por el delito de desaparición de personas, cuatro por homicidio agravado y por siete casos de estafa. \rEntre los capturados por casos de desaparición está Kenia Yajaina Sánchez Morales, quien junto con otros supuestos pandilleros privó de libertad a una víctima que se encontraba en un cervecería, el hecho sucedió en Zacatecoluca, La Paz. Cabe mencionar que la víctima aún se encuentra desaparecida. \rAsí mismo, en el operativo se capturó a Jose Adán Ayala Flores y un menor de edad, perfilado como pandillero, por el asesinato de una persona en las afueras de un restaurante de la playa San Marcelino, en La Paz. \r\"Gracias al Régimen de Excepción el menor de edad ya se encuentra detenido y ha sido notificado del nuevo delito que se le imputa en el centro penal donde guarda prisión\", informó la FGR.\rCasos de estafa por Facebook. \rEl fiscal también informó que se capturó a Fátima del Carmen Guzmán Vásquez, acusada de casos de estafa por la red social Facebook, con alquileres de rancho, venta de celulares. \rMencionó que los acusados exigían el pago del producto por medio de transferencia bancaria, y una vez las víctimas las hacían ya no les contestaban para la entrega de los productos.\r \"Las víctimas en Facebook ven un anuncio que venden o están promocionando la venta de teléfonos celulares como iPhone, alquileres de ranchos, compra de diferentes artículos, les dicen que debe de depositar el dinero a determinada cuenta bancaria, y ya cuando han depositado el dinero a las cuentas que se les ha sugerido pierden contactos, porque ya no responden las llamadas y WhatsApp\". Fiscal del caso.  \rEn el caso de Fátima del Carmen Guzmán Vásquez, la Fiscalía la señala de vender un celular de alta gama, donde solicitó $350 como adelanto una vez recibió el adelanto cortó la comunicación. \r\"No devolvió el dinero ni entregó el aparato\", sostiene la Fiscalía. Agregó que en los próximos días serán remitidos a los juzgados correspondientes donde serán intimados de los delitos.\n\n\n\n\n",
        "title": "Giran 20 órdenes de captura contra sospechosos de desapariciones, homicidios y estafas",
        "sheet": None
    },
    {
        "url": "https://diario.elmundo.sv/nacionales/guatemala-entrega-a-salvadoreno-acusado-de-homicidio-agravado",
        "date": "2024-05-05",
        "sheet_id": "https://diario.elmundo.sv/nacionales/guatemala-entrega-a-salvadoreno-acusado-de-homicidio-agravado",
        "source": "diario.elmundo.sv",
        "tag": "Homicidio",
        "text": "\n        La policía guatemalteca entregó a las autoridades salvadoreñas a Óscar Ricardo Bermúdez López, alias \"Botapelo” o Riky\", que contaba con orden de captura por el delito de homicidio agravado. \rDe acuerdo con la versión de la Policía Nacional Civil (PNC) de El Salvador, el sujeto intentaba huir, por lo que se trasladó hasta el departamento de El Progreso en Guatemala.\r #Allanamientos #MPfuerteYfirme \rLa Unidad Especial Antipandillas Transnacionales del Ministerio Público, en coordinación con el fiscal regional de Coordinación Nacional y con el apoyo de la PNC, desarrolló diligencia de allanamiento en inmueble ubicado en aldea Laguna de San... pic.twitter.com/VXZwqWFK1q\r— MP de Guatemala (@MPguatemala) May 2, 2024   Fue entregado en la frontera San Cristóbal, Santa Ana, para ser remitido al Juzgado Primera Instancia de San Juan Opico, La Libertad y pague por su delito”.  PNC de El Salvador en X  \r“La Unidad Especial Antipandillas Transnacionales del Ministerio Público, en coordinación con el fiscal regional de Coordinación Nacional”, junto a la policía de Guatemala realizaron el operativo en una vivienda ubicada en la aldea Laguna de San Jacinto, municipio de Sanarate, El Progreso, donde se encontraba Bermúdez. \rEl Ministerio Público de Guatemala aseguró que el procedimiento de entrega a las autoridades salvadoreñas fue autorizado por el Juzgado Pluripersonal de Primera Instancia Penal y Delitos contra el Ambiente para Diligencias Urgentes de Investigación.\r Gracias al trabajo junto a la PNC Guatemala, capturamos a Óscar Ricardo Bermudez López, quien cuenta con una orden de captura por homicidio agravado. \rTrató de huir y se trasladó hasta el departamento de El Progreso en Guatemala, donde se escondía. \rFue entregado en la frontera... pic.twitter.com/f1iyftAhrK\r— PNC El Salvador (@PNCSV) May 2, 2024 \n\n\n\n\n",
        "title": "Guatemala entrega a salvadoreño acusado de homicidio agravado",
        "sheet": None
    },
    {
        "url": "https://www.diariocolatino.com/category/nacionales/page/41/",
        "date": "2024-05-05",
        "sheet_id": "https://www.diariocolatino.com/category/nacionales/page/41/",
        "source": "diariocolatino.com",
        "tag": "Homicidio",
        "text": "\nSamuel Amaya @Samuel Amaya98 El padre Guillermo Palacios presidió la misa de este domingo en la Cripta de Catedral Metropolitana de San Salvador; en ella dijo que lo que el Señor quiere para su iglesia es “llevarlos a la vida eterna”. “Si el señor no nos amara, pues no nos diera todas estas oportunidades que constantemente nos da para acercarnos …\nLeer artículo completo \n",
        "title": "No se encontró el título",
        "sheet": None
    },
    {
        "url": "https://diarioelsalvador.com/arrestan-a-cuatro-peligrosos-pandilleros-deportados-de-estados-unidos/499472/",
        "date": "2024-05-05",
        "sheet_id": "https://diarioelsalvador.com/arrestan-a-cuatro-peligrosos-pandilleros-deportados-de-estados-unidos/499472/",
        "source": "diarioelsalvador.com",
        "tag": "Feminicidio",
        "text": "Un grupo de cuatro sujetos miembro de grupos de pandillas y considerados de alta peligrosidad fueron detenidos por elementos de la Policía Nacional Civil (PNC) tras ser deportados de Estados Unidos y arribar al Aeropuerto Internacional de El Salvador. La institución policial detalló que los detenidos son señalados por casos de homicidios y feminicidios, además de su afiliación a grupos de pandillas y estructuras terroristas que operaban en diversas partes de El Salvador. 4 Peligrosos criminales fueron detenidos en el aeropuerto Óscar Arnulfo Romero, deportados de Estados Unidos:▪️Omar Ulises Pineda Amaya, alias Gato o Mouse, gatillero de la 18R, con orden girada por un juez de San Salvador en el año 2023 por homicidio, feminicidio agravado y… pic.twitter.com/BfrjWm1SDN Uno de los detenidos fue identificado como Omar Ulises Pineda Amaya, alias Gato o Mouse, perfilado como gatillero de la pandilla 18R y quien cuenta con orden de captura emitida por un juzgado de San Salvador el pasado año 2023 por los delitos de homicidio, feminicidio agravado y agrupaciones ilícitas. Otro de los detenidos responde al nombre de Milton Adonay Medina Salmerón, alias Chuchi o Cuche, perfilado como homeboy de la pandilla MS13 y con orden de captura emitida en San Francisco Gotera, Morazán, por homicidio agravado y agrupaciones ilícitas. La Policía también logró la captura de David Isaac Castro Merino, alias Deybi, un homeboy de la pandilla 18S quien es señalado por agrupaciones ilícitas. El último de los detenidos fue identificado como Fredy Edenilson Hernández Guardado, alias Tambor, gatillero de la MS13.",
        "title": "Arrestan a cuatro peligrosos pandilleros deportados de Estados Unidos",
        "sheet": {
            "indicators": [
                {
                    "indicator_name": "Clasificacion",
                    "response": "La noticia sí describe un homicidio. La noticia habla de \"casos de homicidios\" y dice que uno de los detenidos, Omar Ulises Pineda Amaya, alias Gato o Mouse, fue identificado por el delito de homicidio."
                },
                {
                    "indicator_name": "Titulo",
                    "response": "**Título de la noticia:** Arrestan a cuatro peligrosos pandilleros deportados de Estados Unidos\n\n**Extraído:** El título de la noticia es \"Arrestan a cuatro peligrosos pandilleros deportados de Estados Unidos\"."
                },
                {
                    "indicator_name": "Resumen",
                    "response": "**Resumen:**\n\nLa noticia informa sobre la captura de cuatro peligrosos pandilleros salvadoreños deportados de Estados Unidos. Los cuatro sujetos, identificados como Omar Ulises Pineda Amaya, alias Gato o Mouse, Milton Adonay Medina Salmerón, alias Chuchi o Cuche, David Isaac Castro Merino, alias Deybi, y Fredy Edenilson Hernández Guardado, alias Tambor, fueron detenidos por la Policía Nacional Civil (PNC) en el Aeropuerto Internacional de El Salvador. Los cargos contra ellos incluyen homicidios, feminicidios, agrupaciones ilícitas y asociación a grupos de pandillas y estructuras terroristas."
                },
                {
                    "indicator_name": "Ubicacion del Suceso",
                    "response": "La noticia indica que el suceso ocurrió en el Aeropuerto Internacional de El Salvador."
                },
                {
                    "indicator_name": "Fuentes",
                    "response": "**Cita de fuentes de información:**\n\nLa noticia no contiene ninguna fuente de información, por lo que no se puede determinar si la información es cierta o no.\n\n**Conclusión:**\n\nLa noticia informa sobre la captura de cuatro peligrosos pandilleros deportados de Estados Unidos en el Aeropuerto Internacional de El Salvador. La información no incluye fuentes de información, por lo que no se puede verificar la precisión de la misma."
                },
                {
                    "indicator_name": "Temas",
                    "response": "**Temas principales tratados en la noticia:**\n\n* **Detención de peligrosos pandilleros:** La noticia informa sobre la detención de cuatro peligrosos pandilleros deportados de Estados Unidos en el Aeropuerto Internacional de El Salvador.\n* **Afiliación a grupos de pandillas y estructuras terroristas:** La noticia enfatiza la afiliación de los detenidos a grupos de pandillas y estructuras terroristas.\n* **Casos de homicidios y feminicidios:** La noticia menciona los delitos de homicidios y feminicidios que se asocian a los detenidos.\n* **Orden de captura:** La noticia indica que los detenidos cuentan con órdenes de captura emitidas por diferentes juicios.\n* **Seguridad:** La noticia destaca la importancia de la detención de estos criminales para la seguridad pública."
                },
                {
                    "indicator_name": "Hechos Violativos",
                    "response": "La noticia no contiene detalles sobre la violación a la ley, por lo que no se puede proporcionar la información requesteda."
                },
                {
                    "indicator_name": "Hipotesis de los Hechos",
                    "response": "**Teoría:**\n\nLa noticia reporta el arresto de cuatro peligrosos pandilleros salvadoreños deportados de Estados Unidos. Los sospechosos, identificados como Omar Ulises Pineda Amaya, alias Gato o Mouse, Milton Adonay Medina Salmerón, alias Chuchi o Cuche, David Isaac Castro Merino, alias Deybi, y Fredy Edenilson Hernández Guardado, alias Tambor, son miembros de grupos de pandillas y se consideran de alta peligrosidad.\n\nLa policía nacional civil (PNC) de El Salvador detuvo a los individuos en el Aeropuerto Internacional de El Salvador, después de su llegada desde Estados Unidos. Los cargos contra ellos incluyen homicidio, feminicidio y agrupaciones ilícitas.\n\nLa presencia de estos pandilleros en el país es una amenaza para la seguridad nacional, y su arresto es una victoria para la lucha contra la delincuencia.\n\n**Suposición:**\n\nLa noticia indica que la eliminación de estos pandilleros de las calles de El Salvador podría tener un impacto positivo en la reducción de la delincuencia en el país. Sin embargo, es importante destacar que la lucha contra la delincuencia requiere una estrategia integral y una colaboración entre las autoridades y la sociedad."
                },
                {
                    "indicator_name": "Poblacion Vulnerable",
                    "response": "La noticia indica que los grupos en riesgo mencionados son la pandilla 18R, la pandilla MS13 y la pandilla 18S."
                },
                {
                    "indicator_name": "Tipo de Arma",
                    "response": "La texto no describe el tipo de arma que se utiliza en la noticia, por lo que no se puede proporcionar la información sobre el tipo de arma."
                },
                {
                    "indicator_name": "Victimas",
                    "response": "La texto no contiene información sobre las víctimas, por lo que no se puede proporcionar la información de identificación de las víctimas en esta noticia."
                },
                {
                    "indicator_name": "Agresor o Sospechoso",
                    "response": "La noticia no indica el nombre del agresor, por lo que no se puede proporcionar la información solicitada."
                }
            ],
            "priority": 3,
            "id": "https://diarioelsalvador.com/arrestan-a-cuatro-peligrosos-pandilleros-deportados-de-estados-unidos/499472/"
        }
    },
    {
        "url": "https://diarioelsalvador.com/criminales-enfrentan-juicio-por-el-asesinato-de-una-mujer-en-teotepeque/494359/",
        "date": "2024-05-05",
        "sheet_id": "https://diarioelsalvador.com/criminales-enfrentan-juicio-por-el-asesinato-de-una-mujer-en-teotepeque/494359/",
        "source": "diarioelsalvador.com",
        "tag": "Feminicidio",
        "text": "Tres pandilleros enfrentan juicio por el asesinato de una mujer, cuyo cuerpo fue encontrado en un predio baldío situado en el distrito de Teotepeque, municipio de La Libertad Costa. La audiencia de vista pública se lleva a cabo en el Juzgado Especializado de Sentencia para una Vida Libre de Violencia y Discriminación para Las Mujeres de San Salvador, donde según la Fiscalía General de la República (FGR) se presentarán todas las pruebas que cómo fue cometido el crimen. En el caso de Rudy Alexander Gamez Sandoval, perfilado como integrante de la pandilla 18, es acusado de homicidio agravado, y según las investigaciones fiscales es señalado de planificar la muerte de la víctima. Los otros implicados son José Heriberto Orellana Lemus y Anival Torres Cruz, quienes enfrentan cargos por feminicidio agravado; ambos son acusados de ejecutar el asesinato. «Los hechos surgen a raíz de un hallazgo realizado el 12 de octubre de 2018 a las 17:00 horas (5:00 pm) en terreno baldío ubicado al costado sur de la carretera Litoral en el km 73 y medio. Es en este lugar donde, ya en estado de descomposición, se da el hallazgo de la víctima y es lo que da pie a iniciar una investigación», explicó el fiscal del caso. Tres sujetos acusados de asesinar a una mujer enfrentan #VistaPública. La @FGR_SV cuenta con suficientes pruebas para demostrar que ellos cometieron este hecho.Rudy Alexander Gamez Sandoval, miembro del Barrio 18, es el principal sospechoso de planificar la muerte de la… pic.twitter.com/PwsTwEDYSA  ",
        "title": "Criminales enfrentan juicio por el asesinato de una mujer en Teotepeque",
        "sheet": {
            "indicators": [
                {
                    "indicator_name": "Clasificacion",
                    "response": "**Clasificación:**\n\nLa noticia describe un homicidio. La noticia habla sobre el asesinato de una mujer en Teotepeque, El Salvador, y menciona el hallazgo del cuerpo de la víctima en un predio baldío."
                },
                {
                    "indicator_name": "Titulo",
                    "response": "**Título de la noticia:** Criminales enfrentan juicio por el asesinato de una mujer en Teotepeque\n\nLa extraída información se encuentra en el título de la noticia."
                },
                {
                    "indicator_name": "Resumen",
                    "response": "**Resumen:**\n\nLa noticia informa sobre el juicio de tres pandilleros por el asesinato de una mujer en Teotepeque, La Libertad Costa. La víctima fue encontrada en un predio baldío y el juicio se lleva a cabo en el Juzgado Especializado de Sentencia para una Vida Libre de Violencia y Discriminación para Las Mujeres de San Salvador. El principal sospechoso, Rudy Alexander Gamez Sandoval, es acusado de homicidio agravado y es considerado como planificador de la muerte de la víctima. Los otros dos acusados, José Heriberto Orellana Lemus y Anival Torres Cruz, enfrentan cargos por feminicidio agravado."
                },
                {
                    "indicator_name": "Ubicacion del Suceso",
                    "response": "**Dónde ocurrió el suceso:**\n\nLa noticia indica que el suceso ocurrió en terreno baldío ubicado al costado sur de la carretera Litoral en el km 73 y medio, en el distrito de Teotepeque, municipio de La Libertad Costa."
                },
                {
                    "indicator_name": "Fuentes",
                    "response": "La noticia no indica fuentes de información, por lo que no se puede proporcionar la información sobre las fuentes de información de la noticia."
                },
                {
                    "indicator_name": "Temas",
                    "response": "**Temas principales tratados en la noticia:**\n\n* **Crimen de asesinato:** La noticia informa sobre el juicio de tres pandilleros por el asesinato de una mujer en Teotepeque.\n* **Audiencia de vista pública:** La audiencia de vista pública se lleva a cabo en el Juzgado Especializado de Sentencia para una Vida Libre de Violencia y Discriminación para Las Mujeres de San Salvador.\n* **Prueba:** La Fiscalía General de la República (FGR) presenta todas las pruebas quehows fue cometido el crimen.\n* **Implicados:** Los tres sujetos acusados de asesinar a la mujer son Rudy Alexander Gamez Sandoval, José Heriberto Orellana Lemus y Anival Torres Cruz.\n* **Llocalización del crimen:** El crimen se occuró en un predio baldío ubicado en el distrito de Teotepeque, municipio de La Libertad Costa."
                },
                {
                    "indicator_name": "Hechos Violativos",
                    "response": "La noticia no contiene información sobre la violación a la ley, por lo que no se puede proporcionar la información solicitado."
                },
                {
                    "indicator_name": "Hipotesis de los Hechos",
                    "response": "**Teoría:**\n\nLa noticia informa sobre el juicio de tres pandilleros por el asesinato de una mujer en Teotepeque, La Libertad Costa. La teoría de la noticia es que los hechos se derivan de un hallazgo realizado en terreno baldío, donde se encontró el cuerpo de la víctima en estado de descomposición. La investigación conducida por la Fiscalía General de la República (FGR) ha encontrado pruebas que respaldan la acusación de los tres sujetos.\n\n**Suposición:**\n\nLa suposición de la noticia es que los acusados están relacionados con la pandilla 18 y que el asesinato fue premeditado y ejecutado por ellos."
                },
                {
                    "indicator_name": "Poblacion Vulnerable",
                    "response": "La noticia no indica grupos en riesgo, por lo que no se puede proporcionar la información solicitada."
                },
                {
                    "indicator_name": "Tipo de Arma",
                    "response": "La texto no indica el tipo de arma utilizada en el asesinato, por lo que no se puede proporcionar la información sobre el tipo de arma."
                },
                {
                    "indicator_name": "Victimas",
                    "response": "La noticia no identifica a la víctima, por lo que no se puede proporcionar la información de su identificación."
                },
                {
                    "indicator_name": "Agresor o Sospechoso",
                    "response": "El texto indica que el nombre del agresor es Rudy Alexander Gamez Sandoval, pero no se menciona si se indica el nombre del otro agresor, por lo que no se puede proporcionar la información solicitada."
                }
            ],
            "priority": 3,
            "id": "https://diarioelsalvador.com/criminales-enfrentan-juicio-por-el-asesinato-de-una-mujer-en-teotepeque/494359/"
        }
    },
    {
        "url": "https://diarioelsalvador.com/feminicidio-mujer-sale-a-cobrar-remesa-se-reune-con-su-pareja-y-es-asesinada/492296/",
        "date": "2024-05-05",
        "sheet_id": "https://diarioelsalvador.com/feminicidio-mujer-sale-a-cobrar-remesa-se-reune-con-su-pareja-y-es-asesinada/492296/",
        "source": "diarioelsalvador.com",
        "tag": "Feminicidio",
        "text": "Rosa Elvira Flores fue asesinada presuntamente por Edwin Antonio Cáceres, con quien mantenía una relación sentimental. Sus restos fueron encontrados en el cantón Los Lagartos, San Julián, Sonsonate. De acuerdo con información de la Fiscalía General de la República (FGR), fue el pasado 27 de marzo que se encontraron los restos de la víctima. «Tras las diligencias ordenadas por los fiscales del caso y la prueba de ADN los forenses determinaron que fue un hecho violento y se confirmó que los restos corresponden a Rosa Elvira Flores», señaló la FGR, en su cuenta de X. Las investigaciones de las autoridades apuntan que Cáceres, quien se encuentra prófugo de la justicia, es el responsable del feminicidio de Flores. #DePaís | La @FGR_SV presentó ayer requerimiento fiscal por feminicidio contra Edwin Antonio Cáceres Ramírez, en perjuicio de su pareja sentimental, identificada por el ministerio público como Rosa Elvira Flores.La mujer retiró una remesa por $2,500 el 19 de marzo pasado y… pic.twitter.com/bozhy1Bvlg Asimismo, se ha señalado la participación de Walter Daniel Melara como el principal cómplice. «Fue intervenido por nuestros agentes, admitió que él era el encargado de deshacerse del teléfono de la víctima ‘porque tenía clavo’», explicó la FGR. Según lo revelado por las investigaciones, el suceso se desencadenó cuando la víctima informó a Cáceres que se dirigía desde Santa Isabel Ishuatán hacia el centro de San Julián para retirar una remesa de $2,500 que le había enviado uno de sus hijos que reside en Estados Unidos. Flores solicitó un taxi para llevar algunas pertenencias a su madre. Trágicamente, al salir, se encontró con Cáceres, quien, según la investigación, la habría asesinado. Su familia reportó la desaparición de Flores cuando ella no regresó. Las autoridades han señalado que al menos 3 personas más han sido detenidas y están siendo procesadas por este caso.",
        "title": "Feminicidio: Mujer sale a cobrar remesa, se reúne con su pareja y es asesinada",
        "sheet": {
            "indicators": [
                {
                    "indicator_name": "Clasificacion",
                    "response": "No, la noticia no describe un homicidio. La noticia describe un feminicidio."
                },
                {
                    "indicator_name": "Titulo",
                    "response": "**Título de la noticia:** Feminicidio: Mujer sale a cobrar remesa, se reúne con su pareja y es asesinada\n\n**Extraído:**\n\nEl título de la noticia es \"Feminicidio: Mujer sale a cobrar remesa, se reúne con su pareja y es asesinada\"."
                },
                {
                    "indicator_name": "Resumen",
                    "response": "**Resumen:**\n\nLa noticia informa sobre el asesinato de Rosa Elvira Flores, cuya pareja, Edwin Antonio Cáceres, se encuentra prófugo de la justicia. La víctima fue asesinada en el cantón Los Lagartos, San Julián, Sonsonate. Las investigaciones de las autoridades apuntan que Cáceres es el responsable del feminicidio, y que el suceso se desencadenó cuando la víctima informó a Cáceres que se dirigía desde Santa Isabel Ishuatán hacia el centro de San Julián para retirar una remesa de $2,500.\n\nLa familia de Flores reportó la desaparición cuando ella no regresó. Las autoridades han señalado que al menos 3 personas más han sido detenidas y están siendo procesadas por el caso."
                },
                {
                    "indicator_name": "Ubicacion del Suceso",
                    "response": "La información sobre el lugar donde ocurrió el suceso se encuentra en la línea 4 de la noticia: **San Julián, Sonsonate**."
                },
                {
                    "indicator_name": "Fuentes",
                    "response": "**Cita de fuentes de información:**\n\nLa noticia no indica fuentes de información, por lo que no se puede proporcionar la información de las fuentes de información."
                },
                {
                    "indicator_name": "Temas",
                    "response": "**Los temas principales tratados en la noticia:**\n\n* **Feminicidio:** La noticia se centra en un caso de feminicidio en el Salvador, donde una mujer fue asesinada por su pareja.\n* **Relación sentimental:** La víctima y el asesino mantenían una relación sentimental.\n* **Remesa:** La víctima retiró una remesa por $2,500 el día anterior al asesinato.\n* **Investigación:** Las autoridades están investigando el caso y buscan al asesino, que se encuentra prófugo de la justicia.\n* **Código de justicia:** La FGR presentó un requerimiento fiscal por feminicidio contra el asesino."
                },
                {
                    "indicator_name": "Hechos Violativos",
                    "response": "La noticia no contiene información sobre la violación a la ley, por lo que no se puede proporcionar la información de los detalles específicos sobre la violación a la ley."
                },
                {
                    "indicator_name": "Hipotesis de los Hechos",
                    "response": "**Teoría:**\n\nLa noticia reporta un caso de feminicidio en el cantón Los Lagartos, San Julián, Sonsonate. La víctima, Rosa Elvira Flores, fue asesinada por su pareja, Edwin Antonio Cáceres. La investigación indica que el asesinato se desencadenó cuando la víctima informó a Cáceres que se dirigía desde Santa Isabel Ishuatán hacia el centro de San Julián para retirar una remesa de $2,500.\n\n**Suposición:**\n\nBasándose en la información disponible, la suposición de esta noticia es que el asesinato de Rosa Elvira Flores fue premeditado por parte de su pareja, Edwin Antonio Cáceres. El crimen parece haber sido motivado por el asesinato de la víctima por un motivo de posesión o control."
                },
                {
                    "indicator_name": "Poblacion Vulnerable",
                    "response": "La información sobre los grupos en riesgo que se encuentra en la noticia no se incluye en el texto, por lo que no se puede proporcionar la información requested."
                },
                {
                    "indicator_name": "Tipo de Arma",
                    "response": "La texto no indica el tipo de arma utilizada en el asesinato, por lo que no se puede determinar si la información sobre el tipo de arma se incluye en la texto."
                },
                {
                    "indicator_name": "Victimas",
                    "response": "**Identifica a las víctimas:**\n\nLa noticia identifica a la víctima como Rosa Elvira Flores."
                },
                {
                    "indicator_name": "Agresor o Sospechoso",
                    "response": "**Nombre del agresor:** Edwin Antonio Cáceres\n\nLa noticia indica que el nombre del agresor es Edwin Antonio Cáceres."
                }
            ],
            "priority": 3,
            "id": "https://diarioelsalvador.com/feminicidio-mujer-sale-a-cobrar-remesa-se-reune-con-su-pareja-y-es-asesinada/492296/"
        }
    },
    {
        "url": "https://diarioelsalvador.com/capturan-en-guatemala-a-pandillero-salvadoreno-acusado-de-dos-homicidios/492319/",
        "date": "2024-05-05",
        "sheet_id": "https://diarioelsalvador.com/capturan-en-guatemala-a-pandillero-salvadoreno-acusado-de-dos-homicidios/492319/",
        "source": "diarioelsalvador.com",
        "tag": "Feminicidio",
        "text": "El ministro de Seguridad, Gustavo Villatoro, informó sobre la captura de Eduardo Antonio Vásquez Menéndez, alias Piropo, pandillero de la 18, quien fue ubicado en Guatemala. «Tras la intervención de nuestra Policía, en coordinación con las autoridades de Guatemala, hemos ubicado y capturado a Eduardo Antonio Vásquez Menéndez, alias Piropo, miembro de la pandilla 18, quien intentó refugiarse en dicho país y cuenta con antecedentes vigentes de dos homicidios cometidos», indicó el funcionario. Villatoro señaló que el antiguo sistema judicial permitió que pandilleros como Vásquez Menéndez continuaran en libertad y lograran escapar a otros países, aseguró que con las leyes actuales esto no será posible. En tiempos pasados, en que las leyes perversas nos obligaban a poner en libertad a un criminal condenado porque la sentencia no estaba firme, ciertas organizaciones carroñeras estaban a sus anchas porque el Estado actuaba contra la sociedad.Tras la intervención de nuestra… pic.twitter.com/Nt81YEQjU0 «En tiempos pasados, en que las leyes perversas nos obligaban a poner en libertad a un criminal condenado porque la sentencia no estaba firme, ciertas organizaciones carroñeras estaban a sus anchas porque el Estado actuaba contra la sociedad», apuntó el ministro. Villatoro afirmó que los responsables de cada homicidio cometido en el país pagarán con décadas en prisión. «No vamos a permitir que ningún asesino como este vuelva a nuestras comunidades, nos encargaremos de que pague con décadas en prisión por cada delito cometido», expresó el funcionario.",
        "title": "Capturan en Guatemala a pandillero salvadoreño acusado de dos homicidios",
        "sheet": {
            "indicators": [
                {
                    "indicator_name": "Clasificacion",
                    "response": "**Clasifica:** Sí, la noticia describe un homicidio. La noticia habla de dos homicidios y la captura de un pandillero salvadoreño acusado de estos delitos."
                },
                {
                    "indicator_name": "Titulo",
                    "response": "**Título de la noticia:** Capturan en Guatemala a pandillero salvadoreño acusado de dos homicidios\n\n**Extraído:** El título de la noticia es \"Capturan en Guatemala a pandillero salvadoreño acusado de dos homicidios\"."
                },
                {
                    "indicator_name": "Resumen",
                    "response": "**Resumen:**\n\nLa noticia informa sobre la captura de Eduardo Antonio Vásquez Menéndez, alias Piropo, pandillero de la 18, en Guatemala. El ministro de Seguridad, Gustavo Villatoro, informó de la ubicación y captura de Vásquez Menéndez, quien cuenta con antecedentes vigentes de dos homicidios cometidos. El funcionario mencionó que el antiguo sistema judicial permitió que pandilleros como Vásquez Menéndez continuaran en libertad y lograran escapar a otros países, pero que con las leyes actuales esto no será posible. Villatoro afirmó que los responsables de cada homicidio cometido en el país pagarán con décadas en prisión."
                },
                {
                    "indicator_name": "Ubicacion del Suceso",
                    "response": "La noticia no indica el lugar donde ocurrió el suceso, por lo que no se puede proporcionar la información de donde ocurrió el suceso."
                },
                {
                    "indicator_name": "Fuentes",
                    "response": "**Cita de fuentes de información:**\n\nLa noticia no indica fuentes de información, por lo que no se puede proporcionar la solicitud de cita de fuentes."
                },
                {
                    "indicator_name": "Temas",
                    "response": "**Temas principales tratados en la noticia:**\n\n* **Captura de pandillero salvadoreño:** La noticia informa sobre la captura de Eduardo Antonio Vásquez Menéndez, alias Piropo, pandillero de la 18, en Guatemala.\n* **Leyes perversas:** El artículo enfatiza en las leyes perversas que permitieron a los pandilleros como Vásquez Menéndez escapar a otros países.\n* **Consecuencias:** La noticia destaca las consecuencias de las leyes perversas, como el desplazamiento de organizaciones carroñeras.\n* **Justice:** La noticia enfatiza el compromiso del gobierno de luchar contra la delincuencia y garantizar la justicia para las víctimas."
                },
                {
                    "indicator_name": "Hechos Violativos",
                    "response": "La noticia no contiene detalles específicos sobre la violación a la ley, por lo que no se puede proporcionar la información de los detalles específicos sobre la violación a la ley."
                },
                {
                    "indicator_name": "Hipotesis de los Hechos",
                    "response": "**Teoría:**\n\nLa noticia reporta la captura de un pandillero salvadoreño llamado Eduardo Antonio Vásquez Menéndez, alias Piropo, en Guatemala. La noticia implica que las leyes perversas en el pasado impedían la captura de Criminales como Vásquez Menéndez, ya que no se aplicaban las sentencias.\n\n**Suposición:**\n\nLa noticia sugiere que las leyes perversas en el pasado permitieron a los pandilleros como Vásquez Menéndez escapar de la justicia."
                },
                {
                    "indicator_name": "Poblacion Vulnerable",
                    "response": "La noticia no indica grupos en riesgo, por lo que no se puede proporcionar la información requesteda."
                },
                {
                    "indicator_name": "Tipo de Arma",
                    "response": "La texto no describe el tipo de arma que utiliza el pandillero salvadoreño, por lo que no se puede determinar si la información sobre el tipo de arma se incluye en la noticia o no."
                },
                {
                    "indicator_name": "Victimas",
                    "response": "La texto no contiene información sobre las víctimas, por lo que no se puede identificar a las víctimas en esta noticia."
                },
                {
                    "indicator_name": "Agresor o Sospechoso",
                    "response": "El texto no menciona el nombre del agresor, por lo que no se puede proporcionar la información de su nombre."
                }
            ],
            "priority": 3,
            "id": "https://diarioelsalvador.com/capturan-en-guatemala-a-pandillero-salvadoreno-acusado-de-dos-homicidios/492319/"
        }
    },
    {
        "url": "https://diarioelsalvador.com/enjuician-a-mareros-por-crimen-de-mujer-en-mariona/491510/",
        "date": "2024-05-05",
        "sheet_id": "https://diarioelsalvador.com/enjuician-a-mareros-por-crimen-de-mujer-en-mariona/491510/",
        "source": "diarioelsalvador.com",
        "tag": "Feminicidio",
        "text": "Una estructura de 22 pandilleros de la clica Altos Crazy Locos Salvatruchos, que delinquía en Ciudad Delgado, Ayutuxtepeque y Mejicanos, es enjuiciada por asesinar a Ruth Nohemy S. en Altos de Santa María, de Villa Mariona, Ciudad Delgado, el 9 de noviembre de 2020. La víctima, preguntó a miembros de esa clica, qué habían hecho a su pareja, José Alexander Pérez García, alias «Lobo», quien también era miembro de esa pandilla. Ella tenía información que los mismos compinches de pandilla lo habían asesinado y comenzó a divulgar entre la gente de lo ocurrido, cuando los miembros de la clica se enteraron que la mujer los andaba evidenciando decidieron asesinarla para silenciarla. Tras planificar el crimen irrumpieron la casa de Ruth Nohemy S. y cometieron el hecho con lujo de barbarie, la orden era asesinarla junto a su hijo de cuatro meses, pero al final, los pandilleros se fueron del lugar y el bebé de cuatro meses permaneció tres horas encima del cadáver de su madre, hasta que vecinos informaron del hecho a las autoridades. Por no haber hecho lo que le ordenaron, la clica asesinó a Efraín Bolaños, alias «Twister» lo tomaron como una traición a la pandilla. Después de 14 días del feminicidio de Ruth Nohemy S. las autoridades encontraron el cadáver de su compañero de vida en una fosa clandestina. Ese feminicidio es uno de los 31 delitos que el tribunal está conociendo en contra de la estructura que estuvo delinquiendo en Altos de Santa María, Altos de Santa Marta y Altos de Santa Laura, El Laurel y colonia Divino Salvador, que están ubicadas a las orillas de la calle a Mariona. Además del feminicidio agravado, el ministerio público acusa a los pandilleros por homicidio agravado, extorsión, agrupaciones ilícitas y otros hechos de crimen organizado. Testimonios, prueba científica y pericias, vinculan a los terroristas en la serie de delitos que investigadores de la Policía Nacional Civil (PNC) indagaron en los tres municipios ubicados al norte de San Salvador. Agrupaciones ilícitas, es el delito en común que la Fiscalía General de la República atribuye a todos y para acreditar su permanencia a la Mara Salvatrucha, han incorporado un perfil de los imputados y su función en la estructura.",
        "title": "Enjuician a mareros por crimen de mujer en Mariona",
        "sheet": {
            "indicators": [
                {
                    "indicator_name": "Clasificacion",
                    "response": "La noticia sí describe un homicidio. La noticia describe el asesinato de Ruth Nohemy S. y el asesinato de su compañero de vida."
                },
                {
                    "indicator_name": "Titulo",
                    "response": "**Extraído el título de la noticia:**\n\n**Enjuician a mareros por crimen de mujer en Mariona**"
                },
                {
                    "indicator_name": "Resumen",
                    "response": "**Resumen:**\n\nLa noticia informa sobre el enjuiciamiento de una estructura de 22 pandilleros de la clica Altos Crazy Locos Salvatruchos por el crimen de mujer de Ruth Nohemy S. en Mariona, Ciudad Delgado. La víctima, que tenía información sobre el asesinato de su pareja, divulgó la información y fue asesinada por los miembros de la clica como resultado. El feminicidio de Ruth Nohemy S. es uno de los 31 delitos que el tribunal está conociendo en contra de la estructura.\n\nLa structs de pandilleros también ha sido acusada de homicidio agravado, extorsión, agrupaciones ilícitas y otros hechos de crimen organizado. Los investigadores de la Policía Nacional Civil (PNC) han vinculado a los terroristas en la serie de delitos por el perfil de los imputados y su función en la estructura."
                },
                {
                    "indicator_name": "Ubicacion del Suceso",
                    "response": "**Dónde ocurrió el suceso:**\n\nLa noticia indica que el suceso ocurrió en Altos de Santa María, de Villa Mariona, Ciudad Delgado."
                },
                {
                    "indicator_name": "Fuentes",
                    "response": "**Cita de fuentes de información:**\n\nLa noticia no contiene ninguna fuente de información, por lo que no se puede analizar la información sobre la misma."
                },
                {
                    "indicator_name": "Temas",
                    "response": "**Los temas principales tratados en la noticia:**\n\n* **Crimen organizado:** La noticia describe un caso de crimen organizado en el que una estructura de pandilleros de la clica Altos Crazy Locos Salvatruchos fue enjuiciada por asesinar a una mujer.\n* **Femicidio:** La noticia destaca el feminicidio de la mujer y el asesinato de su hijo de cuatro meses.\n* **Extorsión:** La noticia indica que la clica extorsionó a la víctima por información sobre el crimen.\n* **Agrupaciones ilícitas:** La noticia enfatiza el delito de agrupaciones ilícitas, que es el delito en común que la Fiscalía General de la República atribuye a todos los miembros de la Mara Salvatrucha."
                },
                {
                    "indicator_name": "Hechos Violativos",
                    "response": "La noticia no contiene información sobre la violación a la ley, por lo que no se puede proporcionar la información solicitada."
                },
                {
                    "indicator_name": "Hipotesis de los Hechos",
                    "response": "**Teoría:**\n\nLa noticia reporta un caso de feminicidio relacionado con una estructura de pandilleros de la clica \"Altos Crazy Locos Salvatruchos\". La teoría de la noticia es que el crimen se motivó por la divulgación de la víctima de información sobre el asesinato de su pareja. Los pandilleros se entraron en pánico por la posible exposición de sus actos y decidieron asesinar a la mujer para silenciarla.\n\n**Suposición:**\n\nLa noticia sugiere que el feminicidio es uno de los 31 delitos que el tribunal está conociendo en contra de la estructura de pandilleros. La suposición es que las agrupaciones ilícitas son el delito en común que la Fiscalía General de la República atribuye a todos los miembros de la Mara Salvatrucha."
                },
                {
                    "indicator_name": "Poblacion Vulnerable",
                    "response": "La noticia no indica grupos en riesgo, por lo que no se puede proporcionar la información de la solicitud."
                },
                {
                    "indicator_name": "Tipo de Arma",
                    "response": "La texto no indica el tipo de arma utilizada en el crimen, por lo que no se puede proporcionar la información sobre el tipo de arma."
                },
                {
                    "indicator_name": "Victimas",
                    "response": "La noticia identifica a las víctimas como Ruth Nohemy S. y su hijo de cuatro meses."
                },
                {
                    "indicator_name": "Agresor o Sospechoso",
                    "response": "La noticia no indica el nombre del agresor, por lo que no se puede proporcionar la información solicitada."
                }
            ],
            "priority": 3,
            "id": "https://diarioelsalvador.com/enjuician-a-mareros-por-crimen-de-mujer-en-mariona/491510/"
        }
    },
    {
        "url": "https://diarioelsalvador.com/clica-de-la-ms-que-delinquia-en-tres-municipios-de-san-salvador-es-enjuiciada-por-31-delitos/490452/",
        "date": "2024-05-05",
        "sheet_id": "https://diarioelsalvador.com/clica-de-la-ms-que-delinquia-en-tres-municipios-de-san-salvador-es-enjuiciada-por-31-delitos/490452/",
        "source": "diarioelsalvador.com",
        "tag": "Feminicidio",
        "text": "El Tribunal Quinto contra el Crimen Organizado de San Salvador, ha comenzado hoy el juicio a una estructura de 25 pandilleros de la Mara Salvatrucha que había estado delinquiendo en varias colonias de Mejicanos, Cuscatancingo y Ciudad Delgado. Se trata de la clica Altos Crazy Salvatruchos y según la acusación presentada por la Fiscalía General de la República consumaron 31 delitos en Altos de Santa María, Altos de Santa Marta y Altos de Santa Laura, El Laurel y colonia Divino Salvador, que están ubicadas a las orillas de la calle a Mariona. De los 31 ilícitos atribuidos hay casos de homicidio agravado, extorsión, agrupaciones ilícitas y feminicidio y otros hechos de crimen organizado que el ministerio público investigó con el apoyo de la Policía Nacional Civil (PNC). Uno de los casos conocidos por el tribunal, es el feminicidio de una mujer embarazada que los pandilleros asesinaron y por ese crimen la representación fiscal pretende que seas condenados a 50 años de prisión. El ministerio público ha ofrecido abundante prueba para acreditar cada uno de los delitos que la clica cometió, hay testimonio, pericias, prueba científica y tecnológica.",
        "title": "Clica de la MS que delinquía en tres municipios de San Salvador es enjuiciada por 31 delitos",
        "sheet": {
            "indicators": [
                {
                    "indicator_name": "Clasificacion",
                    "response": "La noticia sí describe un homicidio. La noticia habla sobre el feminicidio de una mujer embarazada por parte de una clica de pandilleros."
                },
                {
                    "indicator_name": "Titulo",
                    "response": "**Título:** Clica de la MS que delinquía en tres municipios de San Salvador es enjuiciada por 31 delitos\n\n**Extraído:** El título de la noticia es \"Clica de la MS que delinquía en tres municipios de San Salvador es enjuiciada por 31 delitos\"."
                },
                {
                    "indicator_name": "Resumen",
                    "response": "**Resumen:**\n\nLa noticia informa sobre el juicio de una clica de pandilleros de la Mara Salvatrucha que delinquía en tres municipios de San Salvador. La clica, conocida como Altos Crazy Salvatruchos, consumó 31 delitos en varias colonias, incluyendo homicidio agravado, extorsión, agrupaciones ilícitas y feminicidio. El Ministerio Público ha ofrecido abundante prueba para respaldar cada delito, incluyendo testimonio, pericias, prueba científica y tecnológica."
                },
                {
                    "indicator_name": "Ubicacion del Suceso",
                    "response": "**Dónde ocurrió el suceso:**\n\nLa noticia indica que el suceso ocurrió en varias colonias de Mejicanos, Cuscatancingo y Ciudad Delgado, que están ubicadas a las orillas de la calle a Mariona."
                },
                {
                    "indicator_name": "Fuentes",
                    "response": "**Cita de fuentes de información:**\n\nLa noticia no contiene información sobre las fuentes de información, por lo que no se puede proporcionar la cita de fuentes de información."
                },
                {
                    "indicator_name": "Temas",
                    "response": "**Temas principales tratados en la noticia:**\n\n* **Crimen organizado:** La noticia destaca el crimen organizado relacionado con la clica de pandilleros \"Altos Crazy Salvatruchos\" y su involucramiento en 31 delitos en tres municipios de San Salvador.\n* **Juicio:** El juicio contra la clica se inició en el Tribunal Quinto contra el Crimen Organizado, donde se espera que se escuchen los casos de homicidio agravado, extorsión, agrupaciones ilícitas y feminicidio.\n* **Prueba:** El Ministerio Público ha ofrecido abundante prueba para respaldar cada delito, incluyendo testimonio, pericias, prueba científica y tecnológica.\n* **Feminicidio:** Uno de los casos conocidos por el tribunal es el feminicidio de una mujer embarazada, donde la representación fiscal busca una sentencia de 50 años de prisión."
                },
                {
                    "indicator_name": "Hechos Violativos",
                    "response": "La información sobre la violación a la ley en la noticia no se encuentra en el texto, por lo que no se puede proporcionar la información solicitado."
                },
                {
                    "indicator_name": "Hipotesis de los Hechos",
                    "response": "**Teoría:**\n\nLa noticia reporta el juicio de una clica de la Mara Salvatrucha conocida como Altos Crazy Salvatruchos, que ha sido acusada de cometer 31 delitos en tres municipios de San Salvador. La teoría de la noticia es que la clica está involucrada en actividades de crimen organizado, incluyendo homicidio agravado, extorsión, agrupaciones ilícitas y feminicidio.\n\n**Suposición:**\n\nLa noticia sugiere que la clica Altos Crazy Salvatruchos es una organización criminal bien establecida con una amplia red de asociados. La suposición también es que la clica ha causado mucho daño en las comunidades de Mejicanos, Cuscatancingo y Ciudad Delgado, y que su eliminación sería una gran victoria para la lucha contra el crimen organizado."
                },
                {
                    "indicator_name": "Poblacion Vulnerable",
                    "response": "La noticia no indica grupos en riesgo por lo que no se puede proporcionar la información de grupos en riesgo."
                },
                {
                    "indicator_name": "Tipo de Arma",
                    "response": "La texto no menciona el tipo de arma que utiliza la clica de pandilleros, por lo que no se puede proporcionar la información sobre el tipo de arma."
                },
                {
                    "indicator_name": "Victimas",
                    "response": "La noticia no identifica a las víctimas, por lo que no se puede proporcionar la información de su identificación."
                },
                {
                    "indicator_name": "Agresor o Sospechoso",
                    "response": "La información sobre el nombre del agresor no se encuentra en el texto, por lo que no se puede proporcionar la información solicitada."
                }
            ],
            "priority": 3,
            "id": "https://diarioelsalvador.com/clica-de-la-ms-que-delinquia-en-tres-municipios-de-san-salvador-es-enjuiciada-por-31-delitos/490452/"
        }
    },
    {
        "url": "https://diarioelsalvador.com/hombre-pasara-90-anos-en-prision-por-asesinar-a-expareja-y-su-hijo-de-tres-anos/485775/",
        "date": "2024-05-05",
        "sheet_id": "https://diarioelsalvador.com/hombre-pasara-90-anos-en-prision-por-asesinar-a-expareja-y-su-hijo-de-tres-anos/485775/",
        "source": "diarioelsalvador.com",
        "tag": "Feminicidio",
        "text": "El Juzgado Especializado de Sentencia para una Vida Libre de Violencia y Discriminación para las Mujeres de Santa Ana, condenó a 90 años de cárcel a Miguel Antonio Díaz Castro por haber asesinado a su excompañera de vida y su hijo de tres años. Al finalizar la vista pública el tribunal fallo imponiéndole 40 años por el feminicidio agravado de su expareja y 50 años por el homicidio agravado de su hijo de tres años. En el juicio, la Fiscalía probó que el imputado cometió el doble crimen el 1 de noviembre de 2022 en Nahuizalco, departamento de Sonsonate. El ministerio público estableció que la víctima y su hijo estaban en su casa cuando Díaz Castro llegó a discutir con ella y la disparó en varias ocasiones, luego se dirigió a su hijo para asfixiarlo. Después de consumar el hecho el imputado llamó a la Policía fingiendo que había sido amenazado por pandillas de ese lugar para despistar a las autoridades y desligarse del doble crimen.",
        "title": "Hombre pasará 90 años en prisión por asesinar a expareja y su hijo de tres años",
        "sheet": {
            "indicators": [
                {
                    "indicator_name": "Clasificacion",
                    "response": "La noticia sí describe un homicidio. La noticia habla de un hombre que asesinó a su expareja y su hijo de tres años, y el delito incluido en la noticia es el homicidio."
                },
                {
                    "indicator_name": "Titulo",
                    "response": "**Extraído el título de la noticia:**\n\n** hombre pasará 90 años en prisión por asesinar a expareja y su hijo de tres años**"
                },
                {
                    "indicator_name": "Resumen",
                    "response": "**Resumen:**\n\nLa noticia informa sobre la condena de 90 años de cárcel a Miguel Antonio Díaz Castro por asesinar a su expareja y su hijo de tres años. El tribunal especializado de sentencia para una Vida Libre de Violencia y Discriminación para las Mujeres de Santa Ana impuso 40 años por el feminicidio agravado de su expareja y 50 años por el homicidio agravado de su hijo de tres años. La fiscalía probó que el imputado cometió el crimen el 1 de noviembre de 2022.\n\n**Información:**\n\n* **Título:** Hombre pasará 90 años en prisión por asesinar a expareja y su hijo de tres años\n* **Descripción:** El hombre asesinó a su expareja y su hijo de tres años en su casa.\n* **Condena:** 90 años de cárcel por feminicidio agravado y homicidio agravado.\n* **Lugar:** Nahuizalco, departamento de Sonsonate.\n* **Fecha:** 1 de noviembre de 2022."
                },
                {
                    "indicator_name": "Ubicacion del Suceso",
                    "response": "**Dónde ocurrió el suceso:**\n\nLa noticia indica que el suceso ocurrió en Nahuizalco, departamento de Sonsonate."
                },
                {
                    "indicator_name": "Fuentes",
                    "response": "**Cita de fuentes de información:**\n\nLa noticia no contiene ninguna fuente de información, por lo que no se puede determinar si la información es confiable o no."
                },
                {
                    "indicator_name": "Temas",
                    "response": "**Temas principales tratados en la noticia:**\n\n* **Homicidio:** La noticia trata sobre un caso de homicidio, donde un hombre asesinó a su expareja y su hijo de tres años.\n* **Violencia contra las mujeres:** La noticia destaca la violencia contra las mujeres, ya que el crimen se ubica en el contexto de un feminicidio.\n* **Juicio:** La noticia describe el juicio y la sentencia del caso, incluyendo la prueba de la culpabilidad del imputado y la pena impuesta.\n* **Legality:** La noticia menciona la legalidad del caso, incluyendo la ubicación del crimen y la fecha en que ocurrió."
                },
                {
                    "indicator_name": "Hechos Violativos",
                    "response": "La noticia no contiene información sobre la violación a la ley, por lo que no se puede analizar la información solicitada."
                },
                {
                    "indicator_name": "Hipotesis de los Hechos",
                    "response": "**Teoría:**\n\nLa noticia reporta un caso de asesinato de una expareja y su hijo de tres años por parte de su excompañero, Miguel Antonio Díaz Castro. La teoría de la situación es que Díaz Castro cometió el crimen por causa de una disputa con su expareja.\n\n**Suposición:**\n\nLa suposición de la noticia es que Díaz Castro premeditadamente asesino a su expareja y su hijo con el fin de eliminarlos de su vida."
                },
                {
                    "indicator_name": "Poblacion Vulnerable",
                    "response": "La noticia no indica grupos en riesgo, por lo que no se puede proporcionar la información requesteda."
                },
                {
                    "indicator_name": "Tipo de Arma",
                    "response": "La texto no indica el tipo de arma que utilizó el imputado en el asesinato, por lo que no se puede proporcionar la información sobre el tipo de arma."
                },
                {
                    "indicator_name": "Victimas",
                    "response": "**Identifica a las víctimas en la noticia:**\n\nLa noticia indica que las víctimas del crimen son una expareja de vida y su hijo de tres años."
                },
                {
                    "indicator_name": "Agresor o Sospechoso",
                    "response": "El nombre del agresor en la noticia es Miguel Antonio Díaz Castro. La información sobre su nombre se encuentra en la primera frase de la noticia."
                }
            ],
            "priority": 3,
            "id": "https://diarioelsalvador.com/hombre-pasara-90-anos-en-prision-por-asesinar-a-expareja-y-su-hijo-de-tres-anos/485775/"
        }
    },
    {
        "url": "https://diarioelsalvador.com/san-salvador-centro-tendra-dispensa-de-intereses-por-mora/484880/",
        "date": "2024-05-05",
        "sheet_id": "https://diarioelsalvador.com/san-salvador-centro-tendra-dispensa-de-intereses-por-mora/484880/",
        "source": "diarioelsalvador.com",
        "tag": "Feminicidio",
        "text": "El alcalde Mario Durán alista una ordenanza municipal para dispensar intereses moratorios a los habitantes del nuevo municipio de San Salvador Centro que no estén al día con el pago de tasas por la prestación de servicios. Carlos Palacios, director de Finanzas de la alcaldía de San Salvador, dijo a «Diario El Salvador» que el nuevo concejo municipal conocerá el instrumento jurídico una vez se haya instalado el 1.º de mayo venidero, mes en el que comenzaría a tener efecto. «Esta ordenanza de dispensa temporal de intereses moratorios recae sobre las tasas municipales que se cancelan al municipio», dijo Palacios, sosteniendo que los beneficiarios de la ordenanza serán los propietarios arrendatarios de inmuebles. San Salvador Centro estará conformado por los distritos de San Salvador, Ciudad Delgado, Mejicanos, Cuscatancingo y Ayutuxtepeque, como resultado de la nueva división político-administrativa que tendrá el país desde el 1.º de mayo entrante. «Vamos a elaborar una propuesta que sea integral y que conlleve el acompañamiento de esta estrategia que fomente la contribución y el estado de solvencia también de todos los demás municipios que se convertirán en distritos y que van a conformar San Salvador Centro», adelantó el funcionario. Palacios no descartó que esta ordenanza municipal entre en vigor en los primeros 15 días de mayo próximo; es decir, será una de las primeras medidas de la nueva administración municipal a favor de los contribuyentes. Las tasas municipales se pagan por prestación de servicios que da la comuna en concepto de alumbrado público, ornato, aseo, recolección y disposición final de desechos sólidos y mantenimiento de parques y zonas verdes. Palacios aseguró que la ordenanza permitirá a los contribuyentes morosos realizar el pago de las tasas sin ningún recargo y sin ningún interés, y solicitar planes de pago según el monto adeuda[1]do a la municipalidad, para un plazo que no sobrepase los 12 meses calendario. «Tienen esta oportunidad de normalizar y actualizar su situación de mora, y todo ese pago se traducirá en servicios que recibirán en el día a día y en obras» en las comunidades, sostuvo. San Salvador, la ciudad capital gobernada por Durán, aplica actualmente una ordenanza para dispensar intereses moratorios a quienes no están al día con el pago de las tasas.",
        "title": "San Salvador Centro tendrá dispensa de intereses por mora",
        "sheet": {
            "indicators": [
                {
                    "indicator_name": "Clasificacion",
                    "response": "La noticia no describe un homicidio, por lo que no se puede clasificar como descripción de un homicidio."
                },
                {
                    "indicator_name": "Titulo",
                    "response": "**Título de la noticia:** San Salvador Centro tendrá dispensa de intereses por mora\n\nLa información extraída de la noticia es el título de la noticia."
                },
                {
                    "indicator_name": "Resumen",
                    "response": "**Resumen:**\n\nLa noticia informa sobre la nueva ordenanza municipal de la alcaldía de San Salvador para dispensar intereses moratorios a los habitantes del nuevo municipio de San Salvador Centro. La ordenanza entrará en vigor el 1 de mayo y idleness una dispensa temporal de intereses moratorios sobre las tasas municipales para los propietarios arrendatarios de inmuebles. El objetivo de la ordenanza es promover la contribución y el estado de solvencia de todos los demás municipios que se convertirán en distritos.\n\nLa ordenanza permitirá a los contribuyentes morosos realizar el pago de las tasas sin ningún recargo o interés, y solicitar planes de pago según el monto adeuda[1]do a la municipalidad, para un plazo que no sobrepase los 12 meses calendario."
                },
                {
                    "indicator_name": "Ubicacion del Suceso",
                    "response": "La noticia ocurrió en San Salvador, la ciudad capital de El Salvador. El suceso se refiere a la nueva ordenanza municipal que el alcalde Mario Durán está alista para implementar para dispensar intereses moratorios a los habitantes del nuevo municipio de San Salvador Centro."
                },
                {
                    "indicator_name": "Fuentes",
                    "response": "**Cita de fuentes de información:**\n\nLa noticia no indica fuentes de información, por lo que no se puede proporcionar la información sobre las mismas."
                },
                {
                    "indicator_name": "Temas",
                    "response": "**Temas principales tratados en la noticia:**\n\n* **Dispensa de intereses moratorios en San Salvador Centro:** La noticia informa sobre la alista de la alcaldía de San Salvador de una ordenanza municipal para dispensar intereses moratorios a los habitantes del nuevo municipio de San Salvador Centro que no estén al día con el pago de tasas por la prestación de servicios.\n* **Nuevo municipio de San Salvador Centro:** El nuevo municipio de San Salvador Centro se conforma por los distritos de San Salvador, Ciudad Delgado, Mejicanos, Cuscatancingo y Ayutuxtepeque.\n* **Impacto en los contribuyentes:** La ordenanza permitirá a los contribuyentes morosos realizar el pago de las tasas sin ningún recargo o interés.\n* **Plan de pago:** La ordenanza permite a los contribuyentes morosos realizar planes de pago según el monto adeuda[1]do a la municipalidad.\n* **Beneficios:** La ordenanza se espera que beneficie a las comunidades de San Salvador Centro con la mejora de los servicios y las obras."
                },
                {
                    "indicator_name": "Hechos Violativos",
                    "response": "La texto no contiene detalles sobre la violación a la ley, por lo que no se puede proporcionar la información de los detalles específicos sobre la violación a la ley."
                },
                {
                    "indicator_name": "Hipotesis de los Hechos",
                    "response": "**Teoría:**\n\nLa noticia reporta sobre la implementación de una ordenanza municipal para dispensar intereses moratorios a los habitantes de San Salvador Centro, recientemente creado como municipio. La suposición es que la ordenanza tiene como objetivo principal promover la recaudación de tasas y contribuir a la mejora de las comunidades.\n\n**Suposición:**\n\nLa noticia indica que la ordenanza se aplica a los propietarios arrendatarios de inmuebles y busca facilitar la normalización de la situación de mora de los contribuyentes. La suposición es que la ordenanza permitirá a los contribuyentes morosos realizar el pago de sus tasas sin recargo o interés, y también les permitirá solicitar planes de pago."
                },
                {
                    "indicator_name": "Poblacion Vulnerable",
                    "response": "La noticia no indica grupos en riesgo, por lo que no se puede proporcionar la información solicitada."
                },
                {
                    "indicator_name": "Tipo de Arma",
                    "response": "La texto no menciona armas, por lo que no se puede determinar el tipo de arma que se especifica en la solicitud, por lo que no se puede proporcionar la información requesteda."
                },
                {
                    "indicator_name": "Victimas",
                    "response": "La noticia no identifica a las víctimas, por lo que no se puede proporcionar la información de su identificación."
                },
                {
                    "indicator_name": "Agresor o Sospechoso",
                    "response": "La texto no indica el nombre del agresor, por lo que no se puede proporcionar la información de su nombre."
                }
            ],
            "priority": 3,
            "id": "https://diarioelsalvador.com/san-salvador-centro-tendra-dispensa-de-intereses-por-mora/484880/"
        }
    },
    {
        "url": "https://diarioelsalvador.com/inicia-juicio-por-feminicidio-de-exdiputada-yanci-urbina/484644/",
        "date": "2024-05-05",
        "sheet_id": "https://diarioelsalvador.com/inicia-juicio-por-feminicidio-de-exdiputada-yanci-urbina/484644/",
        "source": "diarioelsalvador.com",
        "tag": "Feminicidio",
        "text": "El Juzgado Especializado de Sentencia de la Mujer de San Salvador, comenzó este miércoles el juicio a Peter Wachowsky, acusado de haber asesinado a su exesposa Yanci Urbina, exdiputada del FMLN. En el juicio que tiene reserva total, la Fiscalía General de la República pretende que al culminar la vista pública se le imponga la pena máxima de 50 años de prisión por el delito de feminicidio agravado. Urbina fue asesinada el 29 de mayo de 2022 en Antiguo Cuscatlán, La Libertad, al momento de la inspección y levantamiento de cadáver el imputado aportó información falsa para despistar a las autoridades y desligarse del caso. Pero cuando las investigaciones fueron ampliadas los investigadores hallaron una serie de contradicciones que al final los llevó a perfilar a Peter Wachowsky, como el único sospechoso y el ministerio público ordenó que fuera detenido el 14 de junio de 2022, desde esa fecha se ha mantenido en prisión. Al inicio se dijo que la exdiputada había sufrido un paro cardiaco y un accidente en su casa, pero posteriormente con la autopsia se determinó que había sido asesinada de golpes contundentes. Cuando Wachowsky fue entrevistado por investigadores expuso algunas coartadas, pero una reconstrucción de los hechos arrojó indicios claros de su involucramiento. La autopsia que practicó el Instituto de Medicina Legal evidenció la existencia de mano criminal, se dictaminó hasta el tiempo que Urbina tenía de haber fallecido al momento del reconocimiento de cadáver.",
        "title": "Inicia juicio por feminicidio de exdiputada Yanci Urbina",
        "sheet": {
            "indicators": [
                {
                    "indicator_name": "Clasificacion",
                    "response": "La noticia sí describe un homicidio, ya que habla sobre el asesinato de la exdiputada Yanci Urbina."
                },
                {
                    "indicator_name": "Titulo",
                    "response": "**Extraído el título de la noticia:**\n\n**Inicia juicio por feminicidio de exdiputada Yanci Urbina**"
                },
                {
                    "indicator_name": "Resumen",
                    "response": "**Resumen:**\n\nLa noticia informa sobre el inicio del juicio por feminicidio de la exdiputada Yanci Urbina. El juicio se llevó a cabo en el Juzgado Especializado de Sentencia de la Mujer de San Salvador y la Fiscalía General de la República busca impocar la pena máxima de 50 años de prisión por el delito de feminicidio agravado. Urbina fue asesinada el 29 de mayo de 2022 y el imputado aportó información falsa para despistar a las autoridades. Sin embargo, las investigaciones ampliadas llevaron a la identificación de las contradicciones que permitieron perfilar a Wachowsky como el único sospechoso. La autopsia demostró que Urbina había sido asesinada de golpes contundentes y no por un paro cardiaco como inicialmente se dijo."
                },
                {
                    "indicator_name": "Ubicacion del Suceso",
                    "response": "La información sobre el lugar donde ocurrió el suceso en la noticia es: Antiguo Cuscatlán, La Libertad."
                },
                {
                    "indicator_name": "Fuentes",
                    "response": "**Cita de fuentes de información:**\n\nLa noticia no contiene ninguna fuente de información, por lo que no se puede proporcionar la solicitud de cita de fuentes."
                },
                {
                    "indicator_name": "Temas",
                    "response": "**Los temas principales tratados en la noticia:**\n\n* **Feminizicidio:** La noticia trata sobre el juicio por feminicidio de la exdiputada Yanci Urbina, que ocurrió el 29 de mayo de 2022.\n* **Juicio:** El juicio se lleva a cabo en el Juzgado Especializado de Sentencia de la Mujer de San Salvador.\n* **Pena máxima:** La Fiscalía General de la República pretende que al culminar la vista pública se le imponga la pena máxima de 50 años de prisión por el delito de feminicidio agravado.\n* **Contradicciones:** Las investigaciones revelaron una serie de contradicciones que llevaron a perfilar a Peter Wachowsky como el único sospechoso.\n* **Autopsia:** La autopsia demostró la existencia de mano criminal y corroboró la causa de muerte de Urbina como golpes contundentes."
                },
                {
                    "indicator_name": "Hechos Violativos",
                    "response": "La noticia no contiene información sobre la violación a la ley, por lo que no se puede proporcionar la información requesteda."
                },
                {
                    "indicator_name": "Hipotesis de los Hechos",
                    "response": "**Teoría:**\n\nLa noticia indica que la causa del asesinato de la exdiputada Yanci Urbina todavía no se ha aclarado por completo, y que el juicio aún no ha terminado. La información disponible no es suficiente para determinar la verdad, por lo que no se puede establecer una teoría con base en la información actual.\n\n**Suposición:**\n\nBasándose en la información disponible, se podría suponer que el asesinato de Yanci Urbina fue premeditado y que el acusado, Peter Wachowsky, pudo haber utilizado una combinación de violencia y falsedad para cometer el delito."
                },
                {
                    "indicator_name": "Poblacion Vulnerable",
                    "response": "La noticia no contiene información sobre grupos en riesgo, por lo que no se puede proporcionar la información de grupos en riesgo mencionados."
                },
                {
                    "indicator_name": "Tipo de Arma",
                    "response": "La texto no indica el tipo de arma utilizada en el asesinato de Yanci Urbina, por lo que no se puede determinar el tipo de arma que se utiliza en la noticia."
                },
                {
                    "indicator_name": "Victimas",
                    "response": "La noticia identifica a la víctima como Yanci Urbina, exdiputada del FMLN."
                },
                {
                    "indicator_name": "Agresor o Sospechoso",
                    "response": "El nombre del agresor en la noticia es **Peter Wachowsky**. La noticia describe el inicio del juicio por feminicidio de la exdiputada Yanci Urbina contra el mismo, por lo que no se menciona si el nombre del agresor se mantiene oculto en el texto."
                }
            ],
            "priority": 3,
            "id": "https://diarioelsalvador.com/inicia-juicio-por-feminicidio-de-exdiputada-yanci-urbina/484644/"
        }
    },
    {
        "url": "https://diarioelsalvador.com/hombre-enamorado-de-una-mujer-ficticia-confiesa-el-asesinato-de-su-companera-en-francia/476039/",
        "date": "2024-05-05",
        "sheet_id": "https://diarioelsalvador.com/hombre-enamorado-de-una-mujer-ficticia-confiesa-el-asesinato-de-su-companera-en-francia/476039/",
        "source": "diarioelsalvador.com",
        "tag": "Feminicidio",
        "text": "Un joven adulto fue acusado el miércoles en Francia de haber asesinado a su compañera, con el fin de vivir una relación con una supuesta mujer de quien se había enamorado en internet y que resultó ser un estafador sentimental. El individuo nacido en 1994, empleado técnico de una alcaldía, reconoció haber planeado el crimen para poder «concretar» su relación virtual y afirmó que «lamentaba»  su acción, señaló en un comunicado la Fiscalía de Boulogne-sur-Mer (norte). La víctima, enfermera en una residencia de ancianos, nacida en 1995, fue hallada muerta el 28 de enero en el domicilio de la pareja, en la localidad de Beussent, con «heridas en el torso». Fue su propio compañero quien llamó a los gendarmes, asegurando que todo había ocurrido cuando se ausentó para ir a comprar pan, probablemente con fines de robo dada la desaparición de una alcancía. Pero la investigación descartó esa hipótesis y acusó al hombre, que «mantenía una relación afectiva en internet» con una persona de la cual ignoraba su verdadera identidad. Según el diario Le Parisien, que reveló el caso, esa pasión virtual se presentaba con el nombre de Béatrice Leroux, comerciante en la ciudad de Brest. La supuesta amante resultó ser un personaje ficticio creado por un estafador emocional, probablemente basado en Costa de Marfil, que había logrado que su enamorado le enviase 2.200 euros (unos 2.400 dólares). Numerosas bandas criminales que operan desde África occidental se especializan en estafas por internet, muchas veces creando fuertes vínculos afectivos con las personas contactadas. Francia registra en promedio un feminicidio cada tres días. El año pasado se contabilizaron 94.",
        "title": "Hombre enamorado de una mujer ficticia confiesa el asesinato de su compañera en Francia",
        "sheet": {
            "indicators": [
                {
                    "indicator_name": "Clasificacion",
                    "response": "La noticia describe un homicidio, ya que habla de un asesinato. La víctima, una enfermera en una residencia de ancianos, fue hallada muerta con \"heridas en el torso\"."
                },
                {
                    "indicator_name": "Titulo",
                    "response": "**Título:** Hombre enamorado de una mujer ficticia confiesa el asesinato de su compañera en Francia\n\n**Extraído:** El título de la noticia es \"Hombre enamorado de una mujer ficticia confiesa el asesinato de su compañera en Francia\"."
                },
                {
                    "indicator_name": "Resumen",
                    "response": "**Resumen:**\n\nLa noticia reporta el asesinato de una enfermera en Francia por parte de su compañero. El hombre, nacido en 1994, reconocía haber planeado el crimen para poder concretar su relación virtual con una supuesta mujer de quien se había enamorado en internet. La víctima, nacida en 1995, fue hallada muerta en su domicilio con «heridas en el torso». La investigación descartó la hipótesis de robo de la alcancía y acusó al hombre de haber mantenido una relación afectiva en internet con una persona de la cual ignoraba su verdadera identidad."
                },
                {
                    "indicator_name": "Ubicacion del Suceso",
                    "response": "La noticia ocurrió en la localidad de Beussent, en Francia. El crimen se occuró en el domicilio de la pareja."
                },
                {
                    "indicator_name": "Fuentes",
                    "response": "**Cita de las fuentes de información:**\n\nLa noticia no indica fuentes de información, por lo que no se puede proporcionar la información sobre la misma."
                },
                {
                    "indicator_name": "Temas",
                    "response": "**Temas principales tratados en la noticia:**\n\n* **Crimen de asesinato:** La noticia describe un asesinato de una mujer en Francia por parte de su compañero, motivado por una relación virtual.\n* **Estafador sentimental:** La víctima fue estafada por un personaje ficticio creado por un estafador emocional.\n* **Relación virtual:** La historia enfatiza la naturaleza virtual de la relación entre el hombre y la víctima.\n* **Feminicidio:** La noticia destaca la tasa de feminicidio en Francia, que se registra con regularidad.\n* **Seguridad en internet:** La noticia enfatiza la amenaza de estafas por internet, particularmente desde África occidental."
                },
                {
                    "indicator_name": "Hechos Violativos",
                    "response": "La noticia no contiene información sobre la violación a la ley, por lo que no se puede proporcionar la información solicitada."
                },
                {
                    "indicator_name": "Hipotesis de los Hechos",
                    "response": "**Teoría:**\n\nLa noticia informa de un hombre que asesinó a su compañera en Francia debido a una relación virtual con una mujer ficticia. La teoría de la situación es que el hombre se enamoró de una mujer ficticia en internet, y para concretar su relación, planearon el asesinato.\n\n**Suposición:**\n\nLa suposición de la noticia es que la mujer ficticia era un personaje creado por un estafador emocional. Es probable que la mujer ficticia haya sido creada en Costa de Marfil, ya que el estafador es conocido por operar desde ese país."
                },
                {
                    "indicator_name": "Poblacion Vulnerable",
                    "response": "La información sobre los grupos en riesgo que se indica en la noticia es:\n\n**Grupos en riesgo:**\n\n- Numerosas bandas criminales que operan desde África occidental."
                },
                {
                    "indicator_name": "Tipo de Arma",
                    "response": "La texto no menciona el tipo de arma que se utilizó en el asesinato, por lo que no se puede proporcionar la información de la misma."
                },
                {
                    "indicator_name": "Victimas",
                    "response": "**Identifica a las víctimas:**\n\nLa noticia describe el asesinato de una enfermera en una residencia de ancianos, nacida en 1995, y su compañero, empleado técnico de una alcaldía, nacido en 1994."
                },
                {
                    "indicator_name": "Agresor o Sospechoso",
                    "response": "La información sobre el nombre del agresor en la noticia no se encuentra en el texto, por lo que no se puede proporcionar la información solicitada."
                }
            ],
            "priority": 3,
            "id": "https://diarioelsalvador.com/hombre-enamorado-de-una-mujer-ficticia-confiesa-el-asesinato-de-su-companera-en-francia/476039/"
        }
    },
    {
        "url": "https://www.diariocolatino.com/mejores-salarios-y-condiciones-laborales-principales-demandas-de-andaluces/",
        "date": "2024-05-05",
        "sheet_id": "https://www.diariocolatino.com/mejores-salarios-y-condiciones-laborales-principales-demandas-de-andaluces/",
        "source": "diariocolatino.com",
        "tag": "Feminicidio",
        "text": "\n\nCompartir\n\n Facebook\n Twitter\n Google +\n\n\n\nSaúl Martínez\nCorresponsal\n@DiarioCoLatino\nLa avenida Constitución fue el punto de encuentro para diversas organizaciones que representan la lucha social, laboral y sindical, en Sevilla, España, durante el primero de mayo, Día Internacional del Trabajo.\nMejores condiciones laborales y salariales son de las principales demandas que las organizaciones han hecho en un breve recorrido de manera pacífica.\nJuan Bautista Gines, secretario general de UGT, Andalucía, enfatizó que es momento de avanzar en los retos laborales y sociales, donde también es urgente denunciar las situaciones de precariedad y pobreza en la que viven muchas personas, quienes en el pleno siglo XXI no tienen sustento para comer.\nActualmente, son cerca de 21 millones de trabajadores afiliados a la Seguridad Social en Sevilla, de los cuales más de 10 millones son mujeres.\n“No queremos que las trabajadoras cobren 20% menos por el hecho de ser mujer, no queremos que los jóvenes emigren por no tener oportunidades de empleo, siendo los jóvenes los más preparados en esta década,  también exigimos un alto a los  casos de feminicidios”, acotó Gines.\nLa UGT explica que los casos de despidos no se pueden seguir dando a conveniencia de las empresas, ya que este representa un fuerte impacto en las familias, sobre todo, en el tema de la canasta alimenticia.\nEl dirigente sindical agregó que los altos costos de los alimentos únicamente benefician a las cadenas de alimentación, a costa de la clase obrera, donde a diario “hunden”, en la miseria a los agricultores, productores, trabajadores y trabajadoras.\n“Tenemos que seguir luchando, porque el salario mínimo es ley para todos y se debe de cumplir al igual que la ley de prevención de Riesgos Laborales, que muchas veces no se cumple, provocando la muerte de nuestros trabajadores”, detalló Juan Bautista Gines.\nLa UGT denuncia que hay muchos trabajadores y trabajadoras que van a trabajar y no vuelven vivos, debido a que no les ponen las medidas de seguridad en sus lugares de trabajo.\nLa UGT hizo el llamado a las instancias correspondientes para que distribuyan correctamente a los inspectores de trabajo según  las necesidades de cada provincia, esto debido a que no tienen un control del mercado laboral, con el cual se podrían evitar accidentes de trabajo.\nDurante la concentración las organizaciones aprovecharon  para extender su solidaridad ante los pueblos en situaciones de conflicto entre ellos el Pueblo Saharaui, Cuba y Palestina.\n“Ayer 51 personas fallecieron, tras 10 días transportándose en un cayuco, buscando las Islas Canarias con el fin de tener una vida mejor”, informó Carlos Aristu, Secretario General de Comisiones Obreras de la UGT.\n“Al pueblo Saharaui, que después de décadas de exilio, hoy se manifiesta, anhelando volver al lugar de donde nunca tuvo que ser expulsado, asimismo a los millones de hombres y mujeres de Cuba que hoy entrada la madrugada ocupan las principales calles de la ciudad, en un contexto de más de 60 años, de un cruel bloqueo, económico, comercial, financiero y diplomático y al pueblo de Palestina que lleva décadas sufriendo ante los gobiernos de Israel y de la ceguera de la comunidad internacional, donde hoy sufre un genocidio televisado, ¡viva  la lucha del pueblo de Palestina! Reconózcase ya al Estado soberano de Palestina”, concluyó.\n\nRelacionado\n\n",
        "title": "Mejores salarios y condiciones laborales, principales demandas de andaluces",
        "sheet": {
            "indicators": [
                {
                    "indicator_name": "Clasificacion",
                    "response": "La noticia no describe un homicidio, por lo que no se puede clasificar como tal."
                },
                {
                    "indicator_name": "Titulo",
                    "response": "**Título de la noticia:** Mejores salarios y condiciones laborales, principales demandas de andaluces\n\n**Extraído:**\n\nEl título de la noticia es \"Mejores salarios y condiciones laborales, principales demandas de andaluces\"."
                },
                {
                    "indicator_name": "Resumen",
                    "response": "**Resumen:**\n\nLa noticia informa sobre la concentración de organizaciones laborales y sindicales en Sevilla, donde se presentaron las principales demandas de las organizaciones, incluyendo mejores salarios y condiciones laborales. El líder de la Unión General de Trabajadores (UGT) en Andalucía destacó la necesidad de avanzar en los retos laborales y sociales, y geldt la necesidad de luchar contra la pobreza, la precariedad laboral y la discriminación. La UGT también exigía un alto a los casos de feminicidios, la eliminación de los altos costos de los alimentos y la distribución equitativa de los inspectores de trabajo.\n\nLa concentración también extendió la solidaridad de las organizaciones con los pueblos en conflicto, incluyendo el Pueblo Saharaui, Cuba y Palestina."
                },
                {
                    "indicator_name": "Ubicacion del Suceso",
                    "response": "La noticia se refiere a un evento que ocurrió en Sevilla, España. Por lo tanto, el lugar donde ocurrió el suceso es Sevilla."
                },
                {
                    "indicator_name": "Fuentes",
                    "response": "La información no contiene citas a las fuentes de información, por lo que no se puede analizar la información de la misma."
                },
                {
                    "indicator_name": "Temas",
                    "response": "**Temas principales tratados en la noticia:**\n\n* **Condiciones laborales y salariales:** La UGT exige mejores salarios y condiciones laborales para los trabajadores de Andalucía.\n* **Precariedad y pobreza:** La UGT denuncia la situación de precariedad y pobreza en la que viven muchas personas en Sevilla.\n* **Seguridad en el trabajo:** La UGT exige que se implementen las medidas de seguridad en los lugares de trabajo para evitar accidentes de trabajo.\n* **Solidaria con pueblos en conflicto:** La UGT extiende su solidaridad con los pueblos en conflicto entre ellos."
                },
                {
                    "indicator_name": "Hechos Violativos",
                    "response": "La texto no contiene detalles sobre la violación a la ley, por lo que no se puede proporcionar la información de los detalles específicos sobre la violación a la ley."
                },
                {
                    "indicator_name": "Hipotesis de los Hechos",
                    "response": "**Teoría:**\n\nLa noticia reporta sobre las demandas de las organizaciones laborales y sindicales en Andalucía, con particular énfasis en las condiciones laborales y salariales. La teoría que se asume es que las organizaciones están luchando por mejorar las condiciones laborales y salariales de los trabajadores, ya que estos tienen un impacto directo en la calidad de vida de las personas.\n\n**Suposición:**\n\nLa noticia asume que las organizaciones están utilizando la concentración para extender su solidaridad ante los pueblos en situaciones de conflicto."
                },
                {
                    "indicator_name": "Poblacion Vulnerable",
                    "response": "La información sobre los grupos en riesgo que se menciona en la noticia es:\n\n* **Pueblo Saharaui:** 51 personas fallecieron por el transporte en un cayuco a las Islas Canarias.\n* **Cuba:** Millones de hombres y mujeres de Cuba que hoy entrada la madrugada ocupan las principales calles de la ciudad.\n* **Palestina:** Pueblo de Palestina que lleva décadas sufriendo ante los gobiernos de Israel y de la ceguera de la comunidad internacional."
                },
                {
                    "indicator_name": "Tipo de Arma",
                    "response": "La texto no menciona ningún tipo de arma, por lo que no se puede determinar si la información sobre el tipo de arma se incluye o no."
                },
                {
                    "indicator_name": "Victimas",
                    "response": "La noticia no identifica a las víctimas, por lo que no se puede proporcionar la información de identificación de las víctimas."
                },
                {
                    "indicator_name": "Agresor o Sospechoso",
                    "response": "La texto no contiene información sobre el nombre del agresor, por lo que no se puede proporcionar la información de nombre del agresor."
                }
            ],
            "priority": 3,
            "id": "https://www.diariocolatino.com/mejores-salarios-y-condiciones-laborales-principales-demandas-de-andaluces/"
        }
    },
    {
        "url": "https://www.diariocolatino.com/reforma-ilegal-e-ilegitima/",
        "date": "2024-05-05",
        "sheet_id": "https://www.diariocolatino.com/reforma-ilegal-e-ilegitima/",
        "source": "diariocolatino.com",
        "tag": "Feminicidio",
        "text": "\n\nCompartir\n\n Facebook\n Twitter\n Google +\n\n\n\n\n\nArtículos relacionados\n\n\n\n\n\n \n\n\n“La dictadura no puede convivir con la Constitución”: Evelyn Martínez\n3 mayo, 2024\n\n\n\n\n \n\n\nErick García es condenado a 5 años de prisión\n3 mayo, 2024\n\n\n\n\n \n\n\nRegresará el Encuentro Teatral del Gueto gestionado por el TIET\n3 mayo, 2024\n\n\n\n\nPor Leonel Herrera*\nTal como estaba previsto, la triste y vergonzosamente célebre bancada legislativa oficialista reformó ayer la Constitución de la República.\nPor orden de un presidente que -supuestamente- no está ejerciendo el cargo porque tiene “licencia” y con una dispensa de trámite al mejor estilo de “los mismos de siempre”, los diputados bukelistas modificaron el Artículo 248 referido al procedimiento y la forma de realizar cambios al texto constitucional.\nHicieron una “leguleyada”, como bien señaló la parlamentaria opositora Claudia Ortiz. Los oficialistas le llaman “jugada maestra” para darse falsas ínfulas de estrategas políticos y porque confunden inteligencia con abuso de poder, vandalismo legislativo y traición a la democracia, los derechos humanos y la dignidad de la gente.\nPor alguna razón, estos sepultureros de la democracia salvadoreña no tuvieron a tiempo el paquete de reformas a la Constitución y sólo aprobaron cambiar la manera de reformarla para que la legislatura entrante se encargue, ella sola, de culminar la tarea de adecuar la ley fundamental a la nueva dictadura que comenzará formalmente el 1o de junio, cuando Bukele asuma un segundo mandato presidencial consecutivo prohibido en -al menos- siete artículos de la carta magna.\nProbablemente esto también se deba a cálculos políticos. Por un lado, Bukele prefiere llegar al 1o. de junio sin el escándalo de haber cambiado la Constitución para no ser tan mal visto, sobre todo, por la comunidad internacional; y por otro, prefiere aplicar la estrategia de “calentar gradualmente la olla”, en vez de hervir el agua de una vez.\nEn este último sentido, posiblemente la “jugada” sea una reforma constitucional por partes y no de una vez.\nPrimero cambiarán la conformación del TSE, para negarle magistrados a la oposición; después aumentan el período de los alcaldes y diputados, para suprimir las elecciones de 2027; y ya llegando las elecciones de 2029 eliminan la prohibición de la reelección, y la dejan indefinida para que Bukele se perpetúe en el poder, como lo adelantó el ex demócrata vicepresidente Félix Ulloa.\nY en medio de esto irán modificando disposiciones constitucionales referidas al sistema republicano de separación de poderes, el pluralismo político, las atribuciones del presidente, el rol de la Fuerza Armada, la propiedad y tenencia de la tierra, la autonomía de la Universidad de El Salvador y otros aspectos fundamentales que Bukele y sus hermanos quieran modificar.\nLa reforma aprobada ayer es totalmente inconstitucional y, por tanto, lo serán también las que apruebe la nueva legislatura. En noviembre de 2017 la Sala de lo Constitucional estableció que las reformas constitucionales deben ser aprobadas con elecciones legislativas de por medio; es decir, la reforma de ayer debió aprobarse antes de los comicios del 4 de febrero.\nEl propósito de esto es que se genere el debate necesario alrededor de las propuestas de reformas y que el electorado se exprese a favor o en contra de éstas, votando o no por los diputados que las abanderan.\nEn otros artículos de opinión también señalé que los diputados que promovieron la reelección presidencial violaron el Artículo 75 de la Constitución; por lo cual se quedaron sin derechos políticos, su elección es ilegal y no pueden reformar la Constitución.\nAdemás, por la magnitud de la reforma, se trata -en realidad- de una nueva constitución y, por tanto, debe ser aprobada por una Asamblea Constituyente y no en un proceso ordinario de reforma constitucional.\nFinalmente, la reforma aprobada ayer es totalmente ilegítima porque no tiene objetivos democráticos relacionados con la ampliación de derechos, la participación ciudadana, la transparencia del sistema político y otros objetivos válidos; sino que busca habilitar ilegalmente a la nueva legislatura para que ésta adecúe el marco constitucional a la medida de las ambiciones autoritarias, las necesidades de acumulación de riqueza y las ansias de perpetuarse en el poder del clan familiar gobernante.\n*Periodista y activista social.\n\nRelacionado\n\n",
        "title": "Reforma ilegal e ilegítima",
        "sheet": None
    },
    {
        "url": "https://www.diariocolatino.com/category/nacionales/page/3491/",
        "date": "2024-05-05",
        "sheet_id": "https://www.diariocolatino.com/category/nacionales/page/3491/",
        "source": "diariocolatino.com",
        "tag": "Feminicidio",
        "text": "\nYanuario Gómez @DiarioCoLatino La Asamblea Legislativa ratificó durante la sesión plenaria un préstamo para financiar el presupuesto general 2018 por $350 millones con el Banco Interamericano de Desarrollo (BID), que servirá para que el Estado cumpla con sus obligaciones por los próximos seis meses. En un principio, los recursos se buscarían mediante la colocación de bonos en los mercados internacionales …\nLeer artículo completo \n",
        "title": "No se encontró el título",
        "sheet": None
    },
    {
        "url": "https://www.diariocolatino.com/piden-investigacion-exhaustiva-en-el-caso-lideresa-del-msm/",
        "date": "2024-05-05",
        "sheet_id": "https://www.diariocolatino.com/piden-investigacion-exhaustiva-en-el-caso-lideresa-del-msm/",
        "source": "diariocolatino.com",
        "tag": "Feminicidio",
        "text": "\n\nCompartir\n\n Facebook\n Twitter\n Google +\n\n\n\n\n\nArtículos relacionados\n\n\n\n\n\n \n\n\nSujeto es condenado a 16 años de cárcel por intento de feminicidio de su esposa\n11 abril, 2024\n\n\n\n\n \n\n\nOrganizaciones piden justicia en feminicidio de lideresa del MSM\n2 abril, 2024\n\n\n\n\n \n\n\nEncuentran muerta a lideresa desaparecida\n27 marzo, 2024\n\n\n\n\nAlma Vilches\n@AlmaCoLatino\nAnte el requerimiento presentado por la Fiscalía General de la República (FGR) al Juzgado de Paz de San Julián, Sonsonate, la Asociación Movimiento Salvadoreño de Mujeres (MSM) exigió una investigación exhaustiva, donde no exista la revictimización en el caso de Rosa Elvira Flores, la lideresa que desapareció el 19 de marzo y encontrado su cuerpo sin vida el 27 del mismo mes, con indicios de extrema violencia.\n“Es necesario que se esclarezcan los hechos, se identifique y caiga todo el peso de la ley a los responsables de este feminicidio, y se tomen medidas efectivas para prevenir casos de violencia de género. No se puede justificar de ninguna manera este acto abominable de violencia feminicida con saña y odio contra Elvira”, indicó el MSM a través de un comunicado.\nA este llamado también se unió la Red Intermunicipal de Ventanas Ciudadanas de San Julián, Santa Isabel Ishuatán, Cuisnahuat y Nahuizalco, quienes reiteraron que no se puede tolerar y normalizar la violencia contra las mujeres, tampoco buscar excusas para justificarla.\nComo institución defensora de derechos humanos reiteraron el compromiso de trabajar juntas a fin de construir un entorno seguro y libre de violencia para todas las mujeres, ya que cada vida perdida es una tragedia para los familiares y la sociedad salvadoreña.\n“Estamos profundamente consternadas por el feminicidio de Rosa Elvira Flores Martínez, un hecho cometido con lujo de barbarie que no solo ha conmocionado a nivel nacional e internacional, exigimos justicia para ella y todas las mujeres víctimas de feminicidios”, manifestó el Movimiento.\nA la vez, el MSM consideró que en este país las mujeres no viven seguras, pese a contar con instrumentos legales nacionales e internacionales que obligan al Estado salvadoreño a garantizar el derecho a una vida libre de violencia contra las mujeres.\nEl artículo 8 de la Ley Integral Especial para una vida libre de Violencia en El Salvador, define la violencia contra las mujeres y establece que comprende cualquier acción basada en su género, cause muerte, daño o sufrimiento físico, sexual o psicológico a la mujer tanto en el ámbito público como privado.\nAdemás, el artículo 9 reconoce la violencia feminicida como la máxima expresión de la violencia contra las mujeres, y establece medidas para prevenir, investigar, sancionar y erradicar este tipo de violencia.\n\nRelacionado\n\n",
        "title": "Piden investigacion exhaustiva en el caso lideresa del MSM",
        "sheet": None
    },
    {
        "url": "https://www.diariocolatino.com/registran-10-muertes-violentas/",
        "date": "2024-05-05",
        "sheet_id": "https://www.diariocolatino.com/registran-10-muertes-violentas/",
        "source": "diariocolatino.com",
        "tag": "Feminicidio",
        "text": "\n\nCompartir\n\n Facebook\n Twitter\n Google +\n\n\n\nRedacción YSUCA\nEl Observatorio de Violencia de la Organización Mujeres Salvadoreñas por la Paz (ORMUSA) ha registrado al menos 10 muertes violentas en los que va del año 2024.\nSilvia Juárez, de ORMUSA, dijo que en el monitoreo de medios del Observatorio se han identificado muertes violentas como feminicidios y suicidios.\nORMUSA ha registrado 8 feminicidios, dos de ellos en niñas menores de 10 años; y dos suicidios, uno de una mujer en Antiguo Cuscatlán y otro de una niña en El Congo.\nEn el año 2023, el Observatorio de la Violencia de Género de la Organización de Mujeres Salvadoreñas por la Paz informó que se registró un total de 46 feminicidios.\nEste número lo obtienen únicamente con el monitoreo de medios de comunicación, debido a que desde el año 2019 los informes oficiales de las instituciones de El Salvador no han brindado datos oficiales sobre muertes violentas.\nEl Observatorio Universitario de Derechos Humanos de la UCA (OUDH) señaló que la Policía Nacional Civil (PNC) comunicó solo 21 muertes violentas de mujeres en 2023.\n\nRelacionado\n\n",
        "title": "Registran 10 muertes violentas de mujeres en primeros meses de 2024",
        "sheet": {
            "indicators": [
                {
                    "indicator_name": "Clasificacion",
                    "response": "No, la noticia no describe un homicidio. La noticia habla sobre la registación de 10 muertes violentas de mujeres en El Salvador en el año 2024."
                },
                {
                    "indicator_name": "Titulo",
                    "response": "**Título de la noticia:** Registran 10 muertes violentas de mujeres en primeros meses de 2024\n\n**Extraído:** El título de la noticia es \"Registran 10 muertes violentas de mujeres en primeros meses de 2024\"."
                },
                {
                    "indicator_name": "Resumen",
                    "response": "**Resumen:**\n\nLa noticia informa sobre el registro de 10 muertes violentas de mujeres en El Salvador en los primeros meses de 2024. El Observatorio de Violencia de la Organización Mujeres Salvadoreñas por la Paz (ORMUSA) ha detectado estos casos, que incluyen 8 feminicidios, dos de ellos en niñas menores de 10 años, y dos suicidios. ORMUSA afirma que estos números son estimados, ya que los informes oficiales no proporcionan datos sobre muertes violentas. El Observatorio Universitario de Derechos Humanos de la UCA (OUDH) señaló que la policía comunicó solo 21 muertes violentas de mujeres en 2023."
                },
                {
                    "indicator_name": "Ubicacion del Suceso",
                    "response": "La información sobre el lugar donde ocurrió el suceso no se encuentra en la noticia, por lo que no se puede proporcionar la información para completar la solicitud."
                },
                {
                    "indicator_name": "Fuentes",
                    "response": "**Cita de fuentes de información:**\n\n* Observatorio de Violencia de la Organización Mujeres Salvadoreñas por la Paz (ORMUSA)\n* Silvia Juárez, de ORMUSA\n* Observatorio Universitario de Derechos Humanos de la UCA (OUDH)\n* Policía Nacional Civil (PNC)"
                },
                {
                    "indicator_name": "Temas",
                    "response": "**Temas principales tratados en la noticia:**\n\n* **Violencia contra las mujeres en El Salvador:** La noticia informa sobre el registro de 10 muertes violentas de mujeres en el año 2024, según el Observatorio de Violencia de la Organización Mujeres Salvadoreñas por la Paz (ORMUSA).\n* **Feminicidios:** La noticia indica que ORMUSA ha registrado 8 feminicidios, dos de ellos en niñas menores de 10 años.\n* **Suicidios:** La noticia también reporta dos suicidios, uno de una mujer en Antiguo Cuscatlán y otro de una niña en El Congo.\n* **Defectos en la recopilación de datos:** La noticia destaca la falta de datos oficiales sobre muertes violentas en El Salvador, y cómo el Observatorio Universitario de Derechos Humanos de la UCA (OUDH) ha encontrado que la policía comunicó solo 21 muertes violentas de mujeres en 2023."
                },
                {
                    "indicator_name": "Hechos Violativos",
                    "response": "La noticia no contiene información sobre la violación a la ley, por lo que no se puede proporcionar la información solicitada."
                },
                {
                    "indicator_name": "Hipotesis de los Hechos",
                    "response": "**Teoría:**\n\nLa noticia reporta una tasa de muertes violentas de mujeres en El Salvador en los primeros meses de 2024 que es similar a la de 2023, según el Observatorio de Violencia de la Organización Mujeres Salvadoreñas por la Paz (ORMUSA). Sin embargo, la falta de datos oficiales de las instituciones salvadoreñas dificulta la verificación de esta información.\n\n**Suposición:**\n\nLa tasa de muertes violentas de mujeres en El Salvador en los primeros meses de 2024 podría ser similar a la de 2023, pero es difícil determinar con precisión debido a la falta de datos oficiales."
                },
                {
                    "indicator_name": "Poblacion Vulnerable",
                    "response": "La información sobre los grupos en riesgo que se encuentra en la noticia no se incluye en el texto, por lo que no se puede proporcionar la información para completar la solicitud."
                },
                {
                    "indicator_name": "Tipo de Arma",
                    "response": "La texto no describe el tipo de arma utilizado en las muertes violentas, por lo que no se puede proporcionar la información sobre el tipo de arma."
                },
                {
                    "indicator_name": "Victimas",
                    "response": "La noticia identifica a las víctimas de las 10 muertes violentas de mujeres como:\n\n* 8 feminicidios, dos de ellas en niñas menores de 10 años\n* 2 suicidios, uno de una mujer en Antiguo Cuscatlán y otro de una niña en El Congo"
                },
                {
                    "indicator_name": "Agresor o Sospechoso",
                    "response": "La información sobre el nombre del agresor no se encuentra en la noticia, por lo que no se puede proporcionar la información requested."
                }
            ],
            "priority": 3,
            "id": "https://www.diariocolatino.com/registran-10-muertes-violentas/"
        }
    },
    {
        "url": "https://www.diariocolatino.com/author/nacionales/page/438/",
        "date": "2024-05-05",
        "sheet_id": "https://www.diariocolatino.com/author/nacionales/page/438/",
        "source": "diariocolatino.com",
        "tag": "Feminicidio",
        "text": "\nTeleSUR Miles de trabajadores salieron este sábado a las calles en una nueva ronda de protestas contra el plan de reforma de pensiones del Gobierno de Francia, mientras continúan los paros el algunos sectores, en particular, refinerías,  transporte público y recolección de basura. Por séptima vez en menos de dos meses, París y varias ciudades francesas son el escenario de …\nLeer artículo completo \n",
        "title": "No se encontró el título",
        "sheet": {
            "indicators": [
                {
                    "indicator_name": "Clasificacion",
                    "response": "La noticia no describe un homicidio, por lo que no se puede determinar si la noticia describe un homicidio o no."
                },
                {
                    "indicator_name": "Titulo",
                    "response": "**Extraído el título de la noticia:**\n\nLa noticia no tiene título, por lo que no se pudo extraer el título solicitado."
                },
                {
                    "indicator_name": "Resumen",
                    "response": "**Resumen:**\n\nLa noticia informa sobre las protestas contra el plan de reforma de pensiones del Gobierno de Francia, donde miles de trabajadores se pusieron en las calles el fin de expresar su rechazo. El paro de trabajadores en algunos sectores, como las refinerías, el transporte público y la recolección de basura, continuación también se mantiene. Esta es la séptima vez que París y varias ciudades francesas se convierten en escenario de protestas en menos de dos meses."
                },
                {
                    "indicator_name": "Ubicacion del Suceso",
                    "response": "La noticia indica que el suceso ocurrió en París y varias ciudades francesas."
                },
                {
                    "indicator_name": "Fuentes",
                    "response": "La texto no contiene ninguna fuente de información, por lo que no se puede analizar la información sobre las fuentes de información de la noticia."
                },
                {
                    "indicator_name": "Temas",
                    "response": "**Los temas principales tratados en la noticia:**\n\n* **Protests contra la reforma de pensiones:** La noticia informa sobre una nueva ronda de protestas contra el plan de reforma de pensiones del Gobierno de Francia.\n* **Paros en sectores específicos:** Los paros en los sectores de refinerías, transporte público y recolección de basura se mencionan como continuación de la noticia.\n* **París y ciudades francesas como escenario:** París y varias ciudades francesas son el escenario de las protestas.\n* **No se encontró el título:** La noticia no tiene un título, lo que dificulta la comprensión del contenido."
                },
                {
                    "indicator_name": "Hechos Violativos",
                    "response": "La texto no contiene información sobre la violación a la ley, por lo que no se puede proporcionar la información requesteda."
                },
                {
                    "indicator_name": "Hipotesis de los Hechos",
                    "response": "**Teoría:**\n\nLa noticia no contiene información sobre una teoría o suposición, por lo que no se puede proporcionar la información solicitada."
                },
                {
                    "indicator_name": "Poblacion Vulnerable",
                    "response": "La información sobre los grupos en riesgo que se indican en la noticia no se encuentra en el texto, por lo que no se puede proporcionar la información requested."
                },
                {
                    "indicator_name": "Tipo de Arma",
                    "response": "La texto no menciona ninguna arma, por lo que no se puede determinar si el texto indica el tipo de arma que se utiliza en la noticia."
                },
                {
                    "indicator_name": "Victimas",
                    "response": "La texto no indica víctimas, por lo que no se puede identificar a las víctimas en la noticia, por lo que no se puede proporcionar la información de la identificación de las víctimas."
                },
                {
                    "indicator_name": "Agresor o Sospechoso",
                    "response": "La texto no indica el nombre del agresor, por lo que no se puede proporcionar la información de nombre del agresor."
                }
            ],
            "priority": 3,
            "id": "https://www.diariocolatino.com/author/nacionales/page/438/"
        }
    },
    {
        "url": "https://www.diariocolatino.com/category/titular_principal/page/393/",
        "date": "2024-05-05",
        "sheet_id": "https://www.diariocolatino.com/category/titular_principal/page/393/",
        "source": "diariocolatino.com",
        "tag": "Feminicidio",
        "text": "\nYanuario Gómez @DiarioCoLatino La Bolsa de Productos y Servicios de El Salvador (BOLPROS) llevó a cabo una pastorela con el fin de compartir con sus empleados y familiares el espíritu navideño. El evento contó con una gran cantidad de actos entre cánticos, lectura bíblica, presentación de dramas en los que participaron los trabajadores. Este año y como una muestra de …\nLeer artículo completo \n",
        "title": "No se encontró el título",
        "sheet": None
    },
    {
        "url": "https://www.diariocolatino.com/category/portada/page/1739/",
        "date": "2024-05-05",
        "sheet_id": "https://www.diariocolatino.com/category/portada/page/1739/",
        "source": "diariocolatino.com",
        "tag": "Feminicidio",
        "text": "\nIván Escobar @DiarioCoLatino Este 12 de diciembre, en América Latina y en varias poblaciones del continente se recuerda la aparición de la Virgen de Guadalupe al indio Juan Diego en el cerro del Tepeyac, México, en 1531, una tradición que reúne la fe católica de miles de personas a escala mundial y que, hoy en día, llega a sus 488 …\nLeer artículo completo \n",
        "title": "No se encontró el título",
        "sheet": None
    },
    {
        "url": "https://www.diariocolatino.com/sujeto-condenado/",
        "date": "2024-05-05",
        "sheet_id": "https://www.diariocolatino.com/sujeto-condenado/",
        "source": "diariocolatino.com",
        "tag": "Feminicidio",
        "text": "\n\nCompartir\n\n Facebook\n Twitter\n Google +\n\n\n\n\n\nArtículos relacionados\n\n\n\n\n\n \n\n\nPiden investigacion exhaustiva en el caso lideresa del MSM\n20 abril, 2024\n\n\n\n\n \n\n\nOrganizaciones piden justicia en feminicidio de lideresa del MSM\n2 abril, 2024\n\n\n\n\n \n\n\nEncuentran muerta a lideresa desaparecida\n27 marzo, 2024\n\n\n\n\nRedacción Nacionales\n@DiarioCoLatino\nEl Juzgado Especializado de Sentencia para una Vida Libre de Violencia y Discriminación para las Mujeres de San Salvador condenó a Antonio Guadalupe Aquino Reyes, de 39 años, a 15 años de prisión por el feminicidio agravado tentado en perjuicio de su pareja.\nAdemás, Aquino fue condenado a un año de prisión por el delito de desobediencia en caso de medidas cautelares o de protección. La juzgadora consideró que se acreditaron los delitos y la violencia contra la víctima antes del hecho.\nLos hechos ocurrieron el 15 de junio de 2020 en una comunidad del municipio de Verapaz en San Vicente. Aquino llegó a la vivienda familiar en estado de ebriedad y con un corvo con la intención de quitarle la vida a su pareja.\nLa víctima resultó con lesiones en el brazo y uno de sus dedos al defenderse del ataque para evitar ser herida en el rostro. Aquino fue neutralizado por familiares, quienes lo despojaron del machete y llamaron a la policía, donde fue detenido en flagrancia.\nPandilleros a juicio por 8 homicidios\nEn otro caso judicial, varios pandilleros enfrentarán juicio por ocho homicidios. También serán acusados por otros delitos como extorsiones y tráfico ilícito.\nUn total de 33 pandilleros de la Mara Salvatrucha (MS) fueron enviados a juicio por su probable participación en una serie de delitos que fueron cometidos entre los años 2015 y 2020, en diferentes puntos del departamento de La Unión.\nLuego de la audiencia preliminar realizada por el Tribunal Contra el Crimen Organizado “A” de San Miguel, el juez que conoció el caso dijo existir suficientes elementos de prueba para que el caso pase a la siguiente etapa del proceso.\nA los imputados se les acusa de su probable participación en ocho homicidios agravados, siete extorsiones agravadas, cuatro casos de tráfico ilícito, cinco casos de proposición y conspiración para cometer delito de homicidio agravado y organizaciones terroristas.\nCondenan a sujeto por asesinato en Chirilagua\nLuis Alonso Chicas González, junto a otros cuatro sujetos, interceptaron a la víctima en abril de 2019, en Chirilagua, San Miguel, y bajo amenazas se lo llevaron y le dispararon en múltiples ocasiones hasta causarle la muerte.\nPosteriormente, Chicas y los otros cuatro sujetos recogieron los casquillos para que no hubiera evidencia y huyeron del lugar, pero un testigo con régimen de protección logró identificar a Chicas González como uno de los que participó en el hecho.\nEl Tribunal Segundo de Sentencia de San Miguel, ante la abundante prueba, condenó a Luis Alonso Chicas González a una pena de 25 años de cárcel y giró orden de captura en su contra ya que el imputado, en calidad de rebelde, fue juzgado sin estar presente.\n\nRelacionado\n\n",
        "title": "Sujeto es condenado a 16 años de cárcel por intento de feminicidio de su esposa",
        "sheet": {
            "indicators": [
                {
                    "indicator_name": "Clasificacion",
                    "response": "La noticia describe un homicidio, ya que habla de un caso de feminicidio."
                },
                {
                    "indicator_name": "Titulo",
                    "response": "**Extraído el título de la noticia:**\n\n**Sujeto es condenado a 16 años de cárcel por intento de feminicidio de su esposa**"
                },
                {
                    "indicator_name": "Resumen",
                    "response": "**Resumen:**\n\nLa noticia informa sobre el condena de un sujeto a 16 años de cárcel por intento de feminicidio de su esposa en San Salvador. El hombre, de 39 años, fue condenado por el delito de feminicidio agravado tentado en perjuicio de su pareja. Los hechos ocurrieron el 15 de junio de 2020, en una comunidad del municipio de Verapaz. El sujeto llegó a la vivienda familiar en estado de ebriedad y con un corvo con la intención de quitarle la vida a su pareja. La víctima resultó con lesiones en el brazo y uno de sus dedos al defenderse del ataque."
                },
                {
                    "indicator_name": "Ubicacion del Suceso",
                    "response": "La noticia indica que el suceso ocurrió en una comunidad del municipio de Verapaz en San Vicente, por lo que la información sobre el lugar donde ocurrió el suceso no se encuentra en la noticia, por lo que no se puede proporcionar la información de donde ocurrió el suceso."
                },
                {
                    "indicator_name": "Fuentes",
                    "response": "La información no contiene fuentes de información, por lo que no se puede proporcionar la cita de las mismas."
                },
                {
                    "indicator_name": "Temas",
                    "response": "**Temas principales tratados en la noticia:**\n\n* **Feminicidio:** La noticia informa sobre el condena de un hombre por intento de feminicidio de su esposa en San Salvador.\n* **Justicia:** La noticia destaca la necesidad de justicia para las víctimas de feminicidio.\n* **Violencia contra las mujeres:** La noticia enfatiza la violencia contra las mujeres en El Salvador.\n* **Seguridad:** La noticia menciona la necesidad de medidas para proteger a las mujeres de la violencia.\n* **Legislación:** La noticia no indica si la noticia se refiere a una legislación sobre feminicidio en El Salvador."
                },
                {
                    "indicator_name": "Hechos Violativos",
                    "response": "La noticia no contiene información sobre la violación a la ley, por lo que no se puede proporcionar la información solicitada."
                },
                {
                    "indicator_name": "Hipotesis de los Hechos",
                    "response": "**Teoría:**\n\nLa noticia informa sobre el condena de un sujeto por intento de feminicidio de su esposa en San Salvador. La teoría de la noticia es que el hombre, de nombre Antonio Guadalupe Aquino Reyes, estaba en estado de ebriedad y con un corvo, ingresó en la vivienda familiar con la intención de quitarle la vida a su pareja. La víctima sobrevivió al ataque y el hombre fue condenado a 15 años de prisión por feminicidio agravado.\n\n**Suposición:**\n\nLa suposición de la noticia es que el hombre, Aquino, era un hombre violento y que, debido a su estado mental, cometió el delito de feminicidio."
                },
                {
                    "indicator_name": "Poblacion Vulnerable",
                    "response": "La noticia no contiene información sobre los grupos en riesgo que podrían ser mencionados, por lo que no se puede proporcionar la información solicitado."
                },
                {
                    "indicator_name": "Tipo de Arma",
                    "response": "La noticia no indica el tipo de arma utilizada en el crimen, por lo que no se puede proporcionar la información sobre el tipo de arma."
                },
                {
                    "indicator_name": "Victimas",
                    "response": "La noticia no identifica a las víctimas, por lo que no se puede proporcionar la información de su identificación."
                },
                {
                    "indicator_name": "Agresor o Sospechoso",
                    "response": "El nombre del agresor en la noticia es **Antonio Guadalupe Aquino Reyes**."
                }
            ],
            "priority": 3,
            "id": "https://www.diariocolatino.com/sujeto-condenado/"
        }
    },
    {
        "url": "https://diario.elmundo.sv/nacionales/un-hombre-en-san-miguel-asesina-a-su-companera-de-vida-y-luego-se-suicido",
        "date": "2024-05-05",
        "sheet_id": "https://diario.elmundo.sv/nacionales/un-hombre-en-san-miguel-asesina-a-su-companera-de-vida-y-luego-se-suicido",
        "source": "diario.elmundo.sv",
        "tag": "Feminicidio",
        "text": "\n        La Policía Nacional Civil (PNC) dio a conocer la noche del sábado el feminicidio de una mujer en San Miguel a manos de su compañero de vida, quien después intentó suicidarse. \rSegún la investigación preliminar, el hombre, identificado como Jorge Castro Cañas, disparó a la mujer, cuya identidad y edad no fueron facilitadas, después de una discusión ocurrida en el cantón El Zamorano. \rTras el asesinato, Castro Cañas intentó suicidarse, pero sobrevivió. La PNC informó que fue trasladado al Hospital Nacional \"San Juan de Dios\" de San Miguel, donde falleció. \rEl Salvador no cuenta con estadísticas oficiales y actualizadas por el Ministerio de Justicia y Seguridad Pública sobre la violencia machista, desde que la PNC declaró en reserva la información en 2021. \rEn el reporte diario de la PNC del sábado 27 de abril se incluyó el caso como homicidio, a pesar de que el consenso internacional señala que se debe realizar una separación pues los feminicidios ocurren, a diferencia de otros asesinatos, como consecuencia de la violencia de género. \rEl registro independiente de la Organización de Mujeres Salvadoreñas por la Paz (Ormusa) reporta que entre el 1 de enero y el 10 de marzo de 2024 han ocurrido siete feminicidios, de los cuales dos víctimas eran niñas menores de edad. \rA finales de marzo se generó conmoción por la muerte de Rosa Elvira Flores Martínez, cuyos restos fueron encontrados en el cantón Los Lagartos del distrito de San Julián ocho días después de su desaparición. \rEn este caso, la Fiscalía General de la República (FGR) acusa a su supuesta pareja, quien además le robó $2,500.\n                \n\n\n\n",
        "title": "Un hombre en San Miguel asesina a su compañera de vida y luego se suicidó",
        "sheet": {
            "indicators": [
                {
                    "indicator_name": "Clasificacion",
                    "response": "La noticia describe un homicidio, pero no se ajusta a la definición de homicidio por el consenso internacional, ya que no se realiza la separación entre asesinato y feminicidio."
                },
                {
                    "indicator_name": "Titulo",
                    "response": "**Título de la noticia:** Un hombre en San Miguel asesina a su compañera de vida y luego se suicidó\n\n**Extraído:** El título de la noticia es \"Un hombre en San Miguel asesina a su compañera de vida y luego se suicidó\"."
                },
                {
                    "indicator_name": "Resumen",
                    "response": "**Resumen:**\n\nLa noticia reporta el asesinato de una mujer en San Miguel a manos de su compañero de vida, quien posteriormente se suicidó. El hombre, identificado como Jorge Castro Cañas, disparó a la mujer después de una discusión. El asesinato se incluyó en el reporte diario de la PNC, pero no se sigue el consenso internacional de realizar una separación entre feminicidios y asesinatos por violencia de género. La organización de mujeres salvadoreñas por la paz (Ormusa) reporta que entre el 1 de enero y el 10 de marzo de 2024 han ocurrido siete feminicidios, de los cuales dos víctimas eran niñas menores de edad."
                },
                {
                    "indicator_name": "Ubicacion del Suceso",
                    "response": "La noticia indica que el suceso ocurrió en el cantón El Zamorano de San Miguel."
                },
                {
                    "indicator_name": "Fuentes",
                    "response": "**Fuentes de información:**\n\nLa noticia no contiene ninguna cita de fuentes de información, por lo que no se puede proporcionar la información sobre las fuentes de información."
                },
                {
                    "indicator_name": "Temas",
                    "response": "**Temas principales tratados en la noticia:**\n\n* **Feminicidio:** La noticia describe un caso de feminicidio en San Miguel, donde un hombre asesino a su compañera de vida y luego se suicidó.\n* **Suicido:** El hombre que asesino a su compañera de vida también intento suicidarse.\n* **No esta de acuerdo con el consenso internacional:** El Salvador no cuenta con estadísticas oficiales sobre la violencia machista, y el consenso internacional exige que los casos de feminicidio se registren por separado.\n* **Registro independiente:** La Organización de Mujeres Salvadoreñas por la Paz (Ormusa) reporta que entre el 1 de enero y el 10 de marzo de 2024 han ocurrido siete feminicidios, de los cuales dos víctimas eran niñas menores de edad."
                },
                {
                    "indicator_name": "Hechos Violativos",
                    "response": "La texto no contiene información sobre la violación a la ley, por lo que no se pudo proporcionar la información requested."
                },
                {
                    "indicator_name": "Hipotesis de los Hechos",
                    "response": "**Teoría:**\n\nLa noticia presenta una situación donde un hombre asesinó a su compañera de vida y luego intentaba suicidarse. No se dispone de información sobre las causas o motivaciones del asesinato, por lo que es difícil determinar la verdad o suponer el motivo detrás de los eventos.\n\n**Suposición:**\n\nLa noticia sugiere que el asesinato podría estar relacionado con la violencia de género, ya que el hombre y la víctima eran pareja. Sin embargo, no se cuenta que el reporte diario de la PNC no sigue el consenso internacional sobre la clasificación de los homicidios por violencia de género."
                },
                {
                    "indicator_name": "Poblacion Vulnerable",
                    "response": "La texto no contiene información sobre los grupos en riesgo que se menciona en la noticia, por lo que no se puede proporcionar la información solicitada."
                },
                {
                    "indicator_name": "Tipo de Arma",
                    "response": "La noticia no especifica el tipo de arma que usó el hombre para asesinar a su compañera de vida, por lo que no se puede proporcionar la información sobre el tipo de arma."
                },
                {
                    "indicator_name": "Victimas",
                    "response": "La noticia no identifica a las víctimas, por lo que no se puede proporcionar la información de su identificación."
                },
                {
                    "indicator_name": "Agresor o Sospechoso",
                    "response": "El nombre del agresor en la noticia es **Jorge Castro Cañas**."
                }
            ],
            "priority": 3,
            "id": "https://diario.elmundo.sv/nacionales/un-hombre-en-san-miguel-asesina-a-su-companera-de-vida-y-luego-se-suicido"
        }
    },
    {
        "url": "https://diario.elmundo.sv/nacionales/suspenden-juicio-contra-acusado-del-feminicidio-de-fernanda-najera-por-segunda-vez",
        "date": "2024-05-05",
        "sheet_id": "https://diario.elmundo.sv/nacionales/suspenden-juicio-contra-acusado-del-feminicidio-de-fernanda-najera-por-segunda-vez",
        "source": "diario.elmundo.sv",
        "tag": "Feminicidio",
        "text": "\n        El Juzgado Especializado de Sentencia para una Vida Libre de Violencia y Discriminación para las Mujeres de San Salvador suspendió este lunes por segunda vez el juicio en contra de Michael Alejandro Castillo Murga, acusado del feminicidio agravado de Melvi Fernanda Nájera Quezada y el homicidio tentado de su hijo. \rSegún confirmaron fuentes ligadas al caso, la suspensión de la audiencia de vista pública fue porque la representación de la Fiscalía General de la República (FGR) solicitó la reprogramación. De momento se desconoce el motivo de la solicitud para reprogramar la diligencia. \rEsta es la segunda vez que se suspende e la diligencia, ya que el pasado 14 de febrero se aplazó, debido a la incomparecencia de la Fiscalía General de la República, ya que eran parte del escrutinio final de las elecciones presidenciales y de diputados 2024.\r¿Cómo ocurrió el feminicidio?\rSegún la acusación de la Fiscalía, Fernanda Nájera, de 23 años, fue encontrada muerta con múltiples lesiones ocasionadas con arma blanca, el 1 de febrero, en el kilómetro 99 de la carretera que de Ahuachapán conduce a Sonsonate, en la jurisdicción del cantón El Molino, del municipio de Concepción de Ataco. El hijo de la víctima, de un año y siete meses, fue encontrado el 4 de febrero en un cafetal en estado de abandono y deshidratado \rSegún el relato de la madre de Nájera, Michael Alejandro Castillo Murgas llegó a su casa el 31 de enero de 2019 a traer a su hija y a su nieto, supuestamente se dirigían a una diligencia para otorgarle su apellido al menor, sin embargo, nunca regresaron. \rMichael Alejandro Castillo Murgas es procesado en calidad de ausente. Sobre él pesa una orden de captura internacional.\n                \n\n\n\n",
        "title": "Suspenden juicio contra acusado del feminicidio de Fernanda Nájera, por segunda vez",
        "sheet": {
            "indicators": [
                {
                    "indicator_name": "Clasificacion",
                    "response": "La noticia describe un homicidio, pero no es la descripción del homicidio de la víctima. La noticia describe el feminicidio de una joven y el homicidio tentado de su hijo."
                },
                {
                    "indicator_name": "Titulo",
                    "response": "**Extraído el título de la noticia:**\n\nSuspenden juicio contra acusado del feminicidio de Fernanda Nájera, por segunda vez\n\nLa noticia se ajusta a la estructura de la pregunta, por lo que no se ha eliminado el texto original."
                },
                {
                    "indicator_name": "Resumen",
                    "response": "**Resumen:**\n\nLa noticia informa sobre la suspensión por segunda vez del juicio contra el acusado de feminicidio de Fernanda Nájera, Michael Alejandro Castillo Murga. La suspensión se produjo debido a la solicitud de reprogramación de la representación de la Fiscalía General de la República (FGR). No se sabe aún el motivo de la solicitud.\n\nLa víctima, Fernanda Nájera, de 23 años, fue encontrada muerta con múltiples lesiones ocasionadas con arma blanca, el 1 de febrero, en el kilómetro 99 de la carretera que de Ahuachapán conduce a Sonsonate. El hijo de la víctima, de un año y siete meses, fue encontrado en un cafetal en estado de abandono y deshidratado.\n\nEl acusado, Michael Alejandro Castillo Murgas, es procesado en calidad de ausente. Sobre él pesa una orden de captura internacional."
                },
                {
                    "indicator_name": "Ubicacion del Suceso",
                    "response": "La noticia ocurrió en el kilómetro 99 de la carretera que de Ahuachapán conduce a Sonsonate, en la jurisdicción del cantón El Molino, del municipio de Concepción de Ataco."
                },
                {
                    "indicator_name": "Fuentes",
                    "response": "**Cita de fuentes de información:**\n\nLa noticia no contiene ninguna cita de fuentes de información, por lo que no se puede determinar si la información es cierta o no."
                },
                {
                    "indicator_name": "Temas",
                    "response": "**Los temas principales tratados en la noticia:**\n\n* **Suspensión de juicio:** El juicio en contra de Michael Alejandro Castillo Murga por el feminicidio de Fernanda Nájera se suspendió por segunda vez.\n* **Causa de la suspensión:** La suspensión se dio debido a la solicitud de reprogramación de la representación de la Fiscalía General de la República (FGR).\n* **Descripción del feminicidio:** Nájera fue encontrada muerta con múltiples lesiones causadas con arma blanca.\n* **Proceso:** Castillo Murgas es procesado en calidad de ausente con una orden de captura internacional."
                },
                {
                    "indicator_name": "Hechos Violativos",
                    "response": "La noticia no contiene detalles sobre la violación a la ley, por lo que no se puede proporcionar la información solicitada."
                },
                {
                    "indicator_name": "Hipotesis de los Hechos",
                    "response": "**Teoría:**\n\nLa noticia reporta el suspensión del juicio contra el acusado de feminicidio de Fernanda Nájera por segunda vez. La causa de la suspensión no se conoce, pero se sabe que la Fiscalía General de la República (FGR) solicitó la reprogramación.\n\n**Suposición:**\n\nLa suspensión del juicio podría ser causada por una falta de preparación por parte de la FGR, ya que estaban implicadas en el escrutinio final de las elecciones presidenciales y de diputados 2024."
                },
                {
                    "indicator_name": "Poblacion Vulnerable",
                    "response": "La texto no contiene información sobre grupos en riesgo, por lo que no se puede proporcionar la información solicitado."
                },
                {
                    "indicator_name": "Tipo de Arma",
                    "response": "La texto no indica el tipo de arma utilizada en el feminicidio, por lo que no se puede proporcionar la información sobre el tipo de arma."
                },
                {
                    "indicator_name": "Victimas",
                    "response": "**Identifica a las víctimas:**\n\nLa noticia identifica a las víctimas como Melvi Fernanda Nájera Quezada, de 23 años, y su hijo, de un año y siete meses."
                },
                {
                    "indicator_name": "Agresor o Sospechoso",
                    "response": "El texto no menciona el nombre del agresor, por lo que no se puede proporcionar la información de su nombre."
                }
            ],
            "priority": 3,
            "id": "https://diario.elmundo.sv/nacionales/suspenden-juicio-contra-acusado-del-feminicidio-de-fernanda-najera-por-segunda-vez"
        }
    },
    {
        "url": "https://diario.elmundo.sv/nacionales/envian-a-la-carcel-a-cuatro-implicados-en-asesinato-de-lideresa-comunitaria-principal-acusado-sigue-profugo",
        "date": "2024-05-05",
        "sheet_id": "https://diario.elmundo.sv/nacionales/envian-a-la-carcel-a-cuatro-implicados-en-asesinato-de-lideresa-comunitaria-principal-acusado-sigue-profugo",
        "source": "diario.elmundo.sv",
        "tag": "Feminicidio",
        "text": "\n        El Juzgado de Paz de San Julián, en Sonsonate, decretó en audiencia inicial la detención provisional contra los implicados en el feminicidio agravado de la defensora de derechos humanos Rosa Elvira Flores Martínez, mientras el caso pasa a la etapa de instrucción. \rEn el caso es acusado Edwin Antonio Cáceres Ramírez (en calidad de ausente), la supuesta pareja de la defensora, contra quien el juzgado le giró orden de detención por estar prófugo de la justicia. \rLizeth del Carmen Hernández Coreto, Karla Esmeralda Siguach García, Daniel Adonay García Mauricio y Walter Daniel Melara seguirían en la cárcel por estar implicados en el hecho por el delito de encubrimiento. \r“En el proceso se determinó que Cáceres le quitó el teléfono celular a la víctima y lo entregó a una tercera persona (Walter Melara) para que se deshiciera de él y también le decomisó el dinero... Los demás imputados procedieron a movilizar a Cáceres hasta un punto ciego de la frontera para encubrirlo y que pudiera huir de la justicia salvadoreña”, indicó la Fiscalía General de la República.  \n\n\n\n\n\nRosa Elvira Flores integró el Movimiento Salvadoreño de Mujeres de Sonsonate.\n\n \rLa FGR explicó en su acusación que la víctima le informó el 19 de marzo a Edwin Cáceres que se dirigiría a Santa Isabel Ishuatán, hacia el centro de San Julián, a retirar una remesa de $2,500, que le había sido enviada por uno de los hijos de la víctima que vive en Estados Unidos. \rRosa Elvira Flores solicitó un taxi para trasladar unas cosas a su madre y, al salir, se reunió con Cáceres, quien procedió a cometer el feminicidio. \rLas investigaciones arrojan que la líder comunitaria del Movimiento Salvadoreño de Mujeres (MSM) desapareció el 19 de marzo y fue encontrada hasta el 27 de marzo en un cañal de San Julián. \r“Días después de que la familia interpusiera la denuncia de la desaparición, se encontraron restos óseos al interior de un cañal ubicado en San Julián, los cuales fueron sometidos a pruebas de ADN y ratificaron que pertenecían a la víctima, quien falleció de forma violenta con un golpe en el cráneo”, sostiene la Fiscalía. \rCuando se informó de hallazgo del cuerpo de la mujer, la Policía Nacional Civil (PNC) no incluyó el hecho a las estadísticas de homicidios porque dijo que era imposible determinar la causa de la muerte pero, el pasado jueves, la institución reconoció que fue homicidio e incluyó el hecho a las estadísticas diarias en fecha posterior. \rRosa Elvira tenía 47 años, era integrante del Movimiento Salvadoreño de Mujeres, que reúne diferentes organizaciones comunitarias que velan por los derechos de niñas, jóvenes y mujeres de Sonsonate.\n                \n\n\n\n",
        "title": "Envían a la cárcel a cuatro implicados en asesinato de lideresa comunitaria: principal acusado sigue prófugo",
        "sheet": {
            "indicators": [
                {
                    "indicator_name": "Clasificacion",
                    "response": "La noticia sí describe un homicidio, pero no es la descripción completa del mismo. La noticia describe el asesinato de la lideresa comunitaria Rosa Elvira Flores, pero no incluye la descripción del proceso de la autopsia o el modo en que se encontraron los restos óseos."
                },
                {
                    "indicator_name": "Titulo",
                    "response": "**Título:** Envían a la cárcel a cuatro implicados en asesinato de lideresa comunitaria: principal acusado sigue prófugo\n\nLa información extraída del título de la noticia es: **Envían a la cárcel a cuatro implicados en asesinato de lideresa comunitaria**."
                },
                {
                    "indicator_name": "Resumen",
                    "response": "**Resumen:**\n\nLa noticia informa sobre el asesinato de la líder comunitaria Rosa Elvira Flores, que integraba el Movimiento Salvadoreño de Mujeres de Sonsonate. El caso se encuentra en curso de investigación y se han realizado detenciones por el delito de encubrimiento.\n\nEn el caso, se acusó a Edwin Antonio Cáceres Ramírez de asesinato, mientras que Lizeth del Carmen Hernández Coreto, Karla Esmeralda Siguach García, Daniel Adonay García Mauricio y Walter Daniel Melara se encuentran en la cárcel por estar implicados en el encubrimiento. Las investigaciones revelaron que la víctima fue asesinada con un golpe en el cráneo y que su cuerpo fue encontrado en un cañal de San Julián.\n\nLa policía no incluyó el hecho en las estadísticas de homicidios al principio, pero posteriormente lo incluyó después de que se determinó que la muerte fue causada por homicidio."
                },
                {
                    "indicator_name": "Ubicacion del Suceso",
                    "response": "La noticia ocurrió en San Julián, Sonsonate, El Salvador. El crimen ocurrió en un cañal ubicado en San Julián."
                },
                {
                    "indicator_name": "Fuentes",
                    "response": "La información de la noticia no indica las fuentes de información, por lo que no se puede analizar la información de la misma para determinar si las fuentes de información son confiables."
                },
                {
                    "indicator_name": "Temas",
                    "response": "**Los temas principales tratados en la noticia:**\n\n* **Femicidio:** La noticia informa sobre el asesinato de la lideresa comunitaria Rosa Elvira Flores Martínez.\n* **Derechos humanos:** La noticia enfatiza la defensa de los derechos humanos y la eliminación de la discriminación.\n* **Movimientos comunitarios:** La noticia menciona el Movimiento Salvadoreño de Mujeres (MSM) y su defensa de los derechos de las mujeres.\n* **Investigación:** La noticia describe la investigación que condujo a la captura de los acusados.\n* **Legality:** La noticia destaca la necesidad de justicia y la inclusión de la víctima en las estadísticas de homicidio."
                },
                {
                    "indicator_name": "Hechos Violativos",
                    "response": "La noticia no contiene detalles específicos sobre la violación a la ley, por lo que no se puede proporcionar la información solicitada."
                },
                {
                    "indicator_name": "Hipotesis de los Hechos",
                    "response": "**Teoría:**\n\nLa noticia indica que el asesinato de la lideresa comunitaria Rosa Elvira Flores se produjo como consecuencia de un enfrentamiento entre ella y el principal acusado, Edwin Antonio Cáceres Ramírez. Flores, que era miembro del Movimiento Salvadoreño de Mujeres, fue encontrada muerta en un cañal de San Julián el 27 de marzo, después de que fuera desaparecida el 19 de marzo.\n\nLa teoría de la noticia es que Flores fue asesinada por causa de su defensa de los derechos humanos. El hecho de que el cuerpo de la víctima fuera encontrado en un cañal y que haya pruebas de que Cáceres le quitó el teléfono celular y el dinero de la víctima, apoyan esta teoría.\n\n**Suposición:**\n\nLa suposición de la noticia es que el asesinato de Rosa Elvira Flores fue motivado por su defensa de los derechos humanos."
                },
                {
                    "indicator_name": "Poblacion Vulnerable",
                    "response": "La noticia no indica grupos en riesgo, por lo que no se puede proporcionar la información solicitada."
                },
                {
                    "indicator_name": "Tipo de Arma",
                    "response": "La texto no menciona el tipo de arma que se utilizó en el asesinato de la lideresa comunitaria, por lo que no se puede determinar el tipo de arma utilizado en la noticia."
                },
                {
                    "indicator_name": "Victimas",
                    "response": "La noticia identifica a las víctimas como la defensora de derechos humanos Rosa Elvira Flores Martínez y el supuesto perpetrador Edwin Antonio Cáceres Ramírez."
                },
                {
                    "indicator_name": "Agresor o Sospechoso",
                    "response": "La información sobre el nombre del agresor en la noticia no se encuentra en el texto, por lo que no se pudo proporcionar la información requested."
                }
            ],
            "priority": 3,
            "id": "https://diario.elmundo.sv/nacionales/envian-a-la-carcel-a-cuatro-implicados-en-asesinato-de-lideresa-comunitaria-principal-acusado-sigue-profugo"
        }
    },
    {
        "url": "https://diario.elmundo.sv/nacionales/instalan-juicio-repetido-contra-condenado-por-feminicidio-agravado-de-edi-marcela",
        "date": "2024-05-05",
        "sheet_id": "https://diario.elmundo.sv/nacionales/instalan-juicio-repetido-contra-condenado-por-feminicidio-agravado-de-edi-marcela",
        "source": "diario.elmundo.sv",
        "tag": "Feminicidio",
        "text": "\n        El Juzgado Especializado de Sentencia para una Vida Libre de Violencia y Discriminación para las Mujeres, de San Salvador, instaló ayer por segunda vez un juicio en contra de Rodrigo Alfredo Pérez González, de 39 años, acusado del feminicidio agravado de su expareja Edi Marcela Pérez Girón, un hecho violento ocurrido en 2016. \rEl procesado fue condenado en 2021 a una pena de 35 años de cárcel, pero los defensores apelaron la decisión y la Sala de lo Penal de la Corte Suprema de Justicia anuló la sentencia y ordenó repetir el juicio. \rSegún la defensa, apelaron porque en el primer juicio no se valoró e incorporó una prueba. \rAyer, durante la primera jornada de audiencia se incorporaron los alegatos iniciales y se inició con la prueba testimonial de las partes. La audiencia entró en receso y continuará el próximo 26 de abril con la declaración de testigos.  \n\n\n\n\n\nEdi Marcela Pérez Girón fue víctima de feminicidio en 2016.\n\n \rA la expareja de la víctima, se le procesa por un hecho ocurrido el 19 de noviembre del 2016 ya que, según la relación de hechos de la Fiscalía, el sujeto llegó con su vehículo a la casa de la víctima para llevarla a un compromiso social, sin embargo, luego de llevársela la familia nunca supo nada de la joven. \rFue localizada fallecido a causa de “múltiples golpes” cerca de un basurero de la calle a Huizúcar. Las investigaciones revelan que la víctima fue asesinada en otro lugar y, ese mismo día, su cadáver fue lanzado a la orilla de la carretera. \rTras el asesinato de Edith Marcela, el principal sospechoso desapareció y no fue sino hasta el 21 de diciembre de 2019, tres años después del hecho, que fue capturado cuando ingresaba al país, procedente de Honduras, por la frontera terrestre de El Amatillo, en La Unión.\rBúsqueda de impunidad\rPrevio al inicio del juicio, organizaciones feministas se concentraron a las fuerzas del Centro Judicial “Isidro Menéndez” para denunciar la reapertura del caso, que consideran busca la impunidad al beneficiar al feminicida. \r“Llama la atención que en este contexto donde hay casos que no han tenido ninguna sentencia y que exista toda una narrativa del gobierno en negar los feminicidios y los homicidios, abran casos que ya tienen sentencia”, aseguró Keyla Cáceres, de la Colectiva Feminista. \rAseguraron que en el primer juicio se demostró con pruebas la culpabilidad del acusado y que como resultado se le impuso 35 años de cárcel. Exhortaron al sistema de justicia a mantener en firme la condena y no liberar al acusado.\n                \n\n\n\n",
        "title": "Instalan juicio repetido contra condenado por feminicidio agravado de Edi Marcela",
        "sheet": {
            "indicators": [
                {
                    "indicator_name": "Clasificacion",
                    "response": "La noticia describe un homicidio, pero no de forma explícita. La noticia habla sobre el asesinato de una mujer, pero no proporciona detalles sobre el modo en que ocurrió el asesinato o sobre el estado del cuerpo del víctima después de la muerte."
                },
                {
                    "indicator_name": "Titulo",
                    "response": "**Extraído el título de la noticia:**\n\n**Instalan juicio repetido contra condenado por feminicidio agravado de Edi Marcela**"
                },
                {
                    "indicator_name": "Resumen",
                    "response": "**Resumen:**\n\nLa noticia informa sobre el instalación de un juicio repetido contra un hombre acusado de feminicidio agravado de su expareja en San Salvador. El acusado, Rodrigo Alfredo Pérez González, fue condenado a 35 años de cárcel en 2021, pero la sentencia fue anulada por la Sala de lo Penal de la Corte Suprema de Justicia, por lo que se repitió el juicio. La defensa argumenta que no se valoró e incorporó una prueba en el primer juicio. El juicio se inició con la incorporación de los alegatos iniciales y la prueba testimonial de las partes.\n\n**Información:**\n\n* **Título:** Instalan juicio repetido contra condenado por feminicidio agravado de Edi Marcela\n* **Descripción:** El IUPAC de Sentencia para una Vida Libre de Violencia y Discriminación para las Mujeres instaló ayer por segunda vez un juicio en contra de Rodrigo Alfredo Pérez González.\n* **Causa:** El asesinato de Edi Marcela Pérez Girón en 2016.\n* **Impunidad:** Las organizaciones feministas se concentraron en el Centro Judicial “Isidro Menéndez” para denunciar la reapertura del caso."
                },
                {
                    "indicator_name": "Ubicacion del Suceso",
                    "response": "La noticia indica que el suceso ocurrió en un lugar no especificado en el texto, por lo que no se puede proporcionar la información de donde ocurrió el suceso."
                },
                {
                    "indicator_name": "Fuentes",
                    "response": "La información de la noticia no contiene citas de fuentes de información, por lo que no se puede proporcionar la solicitud de análisis."
                },
                {
                    "indicator_name": "Temas",
                    "response": "**Los temas principales tratados en la noticia:**\n\n* **Feminicidio:** La noticia describe el caso de feminicidio de Edi Marcela Pérez Girón y el juicio repetido contra el acusado.\n* **Impunidad:** La noticia destaca la reacción de las organizaciones feministas contra la reapertura del caso, que consideran que busca la impunidad.\n* **Justicia:** La noticia enfatiza la necesidad de mantener la condena del acusado y evitar la liberación.\n* **Derechos de las mujeres:** La noticia destaca la importancia de la justicia para las víctimas de feminicidio."
                },
                {
                    "indicator_name": "Hechos Violativos",
                    "response": "La noticia no contiene información sobre los detalles específicos de la violación a la ley, por lo que no se puede proporcionar la información solicitada."
                },
                {
                    "indicator_name": "Hipotesis de los Hechos",
                    "response": "**Teoría:**\n\nLa noticia describe el proceso judicial de un hombre acusado de feminicidio agravado de su expareja en El Salvador. La teoría de la noticia es que el juicio se repitió debido a la anulación de la sentencia original y que las organizaciones feministas están preocupadas por la posibilidad de impunidad.\n\n**Suposición:**\n\nLa noticia asume que el asesinato de la víctima fue relacionado con el feminicidio y que el acusado es culpable."
                },
                {
                    "indicator_name": "Poblacion Vulnerable",
                    "response": "La información sobre los grupos en riesgo que se encuentra en la noticia no se incluye en el texto, por lo que no se puede proporcionar la información solicitado."
                },
                {
                    "indicator_name": "Tipo de Arma",
                    "response": "La texto no indica el tipo de arma utilizada en el asesinato de Edi Marcela Pérez Girón, por lo que no se puede determinar si la información sobre el tipo de arma se incluye en la texto o no."
                },
                {
                    "indicator_name": "Victimas",
                    "response": "La noticia identifica a la víctima como **Edi Marcela Pérez Girón**. No se identifica la víctima del feminicidio ocurrido en el 2016."
                },
                {
                    "indicator_name": "Agresor o Sospechoso",
                    "response": "La información sobre el nombre del agresor en la noticia no se incluye en el texto, por lo que no se puede proporcionar la información solicitada."
                }
            ],
            "priority": 3,
            "id": "https://diario.elmundo.sv/nacionales/instalan-juicio-repetido-contra-condenado-por-feminicidio-agravado-de-edi-marcela"
        }
    },
    {
        "url": "https://diario.elmundo.sv/nacionales/al-menos-11-feminicidios-se-registran-en-el-salvador-entre-enero-y-marzo-segun-ong",
        "date": "2024-05-05",
        "sheet_id": "https://diario.elmundo.sv/nacionales/al-menos-11-feminicidios-se-registran-en-el-salvador-entre-enero-y-marzo-segun-ong",
        "source": "diario.elmundo.sv",
        "tag": "Feminicidio",
        "text": "\n        Al menos 11 casos de feminicidio se dieron en El Salvador entre enero y marzo de 2024, de acuerdo información proporcionada este martes a EFE por la Organización de Mujeres Salvadoreñas por la Paz (Ormusa) que alerta sobre \"una tendencia de desprotección\" a mujeres en el país centroamericano. \rEntre las muertes, indicó Silvia Juárez coordinadora de programas de la organización feminista Ormusa, está la de una defensora de derechos humanos en la localidad de Sonsonate (este), cuyos restos fueron encontrados siete días después de que se reportara su desaparición, según información de la prensa local. \rJuárez aseguró que \"la tendencia en el año sobre la desprotección e inseguridad de las mujeres se mantiene\" y alertó que \"esto pone en evidencia que la vida de las mujeres aún sigue en alta desprotección y que la tendencia, a pesar de la baja de homicidios, el número de muertes violentas de mujeres y de feminicidios sigue con un saldo en rojo\". \rActualmente, las instituciones estatales han puesto bajo secreto o niegan el acceso a datos de la violencia, incluida la información sobre feminicidios. \rRepresentantes de un consorcio feminista, integrado por cinco organizaciones no gubernamentales de mujeres y una asociación comunal, alertaron en marzo pasado sobre el aumento en El Salvador de los asesinatos de mujeres perpetradas por sus parejas y lamentaron \"el silencio\" de las autoridades ante esta situación. \rUnos 38 feminicidios y muertes violentas de mujeres se registraron en El Salvador entre enero y octubre de 2023, de acuerdo con datos del Observatorio de Violencia Contra la Mujer de Ormusa.\n\n\n\n\n",
        "title": "Al menos 11 feminicidios se registran en El Salvador entre enero y marzo, según ONG",
        "sheet": {
            "indicators": [
                {
                    "indicator_name": "Clasificacion",
                    "response": "No, la noticia no describe un homicidio. La noticia describe el problema de la violencia contra las mujeres en El Salvador, específicamente el delito de feminicidio."
                },
                {
                    "indicator_name": "Titulo",
                    "response": "**Extraído el título de la noticia:**\n\n**Al menos 11 feminicidios se registran en El Salvador entre enero y marzo, según ONG**"
                },
                {
                    "indicator_name": "Resumen",
                    "response": "**Resumen:**\n\nLa noticia informa sobre el aumento de los casos de feminicidio en El Salvador entre enero y marzo de 2024. Se indica que se registraron al menos 11 casos de feminicidio en el país, según la Organización de Mujeres Salvadoreñas por la Paz (Ormusa). La organización alerta sobre \"una tendencia de desprotección\" a mujeres en el país, destacando la muerte de una defensora de derechos humanos en la localidad de Sonsonate. El número de asesinatos de mujeres perpetradas por sus parejas y el número de feminicidios se ha elevado en El Salvador, y las instituciones estatales no han proporcionado información sobre la violencia, incluido la información sobre feminicidios."
                },
                {
                    "indicator_name": "Ubicacion del Suceso",
                    "response": "La información sobre el lugar donde ocurrió el suceso en la noticia es: Sonsonate (este), El Salvador."
                },
                {
                    "indicator_name": "Fuentes",
                    "response": "**Cita de las fuentes de información:**\n\n* EFE\n* Organización de Mujeres Salvadoreñas por la Paz (Ormusa)\n* Prensa local\n\n**No se utilizan otras fuentes de información.**"
                },
                {
                    "indicator_name": "Temas",
                    "response": "**Temas principales tratados en la noticia:**\n\n* **Femininidios en El Salvador:** La noticia informa sobre los casos de feminicidio en El Salvador entre enero y marzo de 2024.\n* **Desprotección de las mujeres:** La noticia enfatiza la falta de protección para las mujeres en El Salvador, destacando la tendencia de desprotección e inseguridad de las mujeres.\n* **Defensora de derechos humanos:** La noticia incluye la historia de una defensora de derechos humanos cuyo asesinato se incluye en los 11 casos.\n* **Falta de transparencia:** La noticia destaca la falta de transparencia de las instituciones estatales con respecto a la violencia contra las mujeres, incluido el acceso a datos sobre feminicidios.\n* **Lamentación por la falta de acción:** Los representantes de un consorcio feminista lamentaron la falta de acción de las autoridades en respuesta a la violencia contra las mujeres."
                },
                {
                    "indicator_name": "Hechos Violativos",
                    "response": "La texto no contiene detalles sobre la violación a la ley, por lo que no se puede analizar la información de la violación a la ley."
                },
                {
                    "indicator_name": "Hipotesis de los Hechos",
                    "response": "**Teoría:**\n\nLa noticia informa sobre un aumento de los casos de feminicidio en El Salvador entre enero y marzo de 2024. La organización de mujeres salvadoreñas por la paz (Ormusa) alerta sobre una tendencia de desprotección de las mujeres en el país, y enfatiza que la situación sigue siendo grave.\n\n**Suposición:**\n\nLa causa de la alta tasa de feminicidio en El Salvador es compleja y requiere una investigación exhaustiva. Sin embargo, la noticia sugiere que la falta de protección de las mujeres, la falta de transparencia y la falta de apoyo para las víctimas de violencia contra las mujeres podrían estar contribuyendo a la situación."
                },
                {
                    "indicator_name": "Poblacion Vulnerable",
                    "response": "La noticia no indica grupos en riesgo, por lo que no se puede proporcionar la información requested."
                },
                {
                    "indicator_name": "Tipo de Arma",
                    "response": "La texto no indica el tipo de arma utilizado en los asesinatos, por lo que no se puede proporcionar la información sobre el tipo de arma."
                },
                {
                    "indicator_name": "Victimas",
                    "response": "La noticia informa sobre el asesinato de al menos 11 mujeres en El Salvador entre enero y marzo de 2024. No se identifican las víctimas en la noticia, por lo que no se puede proporcionar la información de identificación de las víctimas."
                },
                {
                    "indicator_name": "Agresor o Sospechoso",
                    "response": "La información sobre el nombre del agresor no se encuentra en el texto, por lo que no se puede proporcionar la información de nombre del agresor."
                }
            ],
            "priority": 3,
            "id": "https://diario.elmundo.sv/nacionales/al-menos-11-feminicidios-se-registran-en-el-salvador-entre-enero-y-marzo-segun-ong"
        }
    },
    {
        "url": "https://diario.elmundo.sv/nacionales/suspenden-hasta-nuevo-aviso-juicio-por-feminicidio-de-yancy-urbina",
        "date": "2024-05-05",
        "sheet_id": "https://diario.elmundo.sv/nacionales/suspenden-hasta-nuevo-aviso-juicio-por-feminicidio-de-yancy-urbina",
        "source": "diario.elmundo.sv",
        "tag": "Feminicidio",
        "text": "\n        El Juzgado Especializado de Sentencia para una Vida Libre de Violencia y Discriminación de San Salvador suspendió hasta nuevo aviso el juicio contra Peter Wachowski, quien es enjuiciado del feminicidio de su exesposa, Yancy Urbina, la exdiputado del FMLN. \rSegún fuentes judiciales, el juicio entró en receso el pasado viernes 12 abril debido a que la jueza solicitó una prueba \"para mejor proveer\". \rEl juicio se reanudará una vez la prueba sea incorporada, y será hasta ese momento procesal que la jueza notificará a las partes la nueva fecha para reanudar el juicio. \rLa vista pública continuará con la presentación de los alegatos finales, donde la Fiscalía General de la República solicitará la sentencia condenatoria y la defensa solicitará sus argumentos para obtener la sentencia absolutoria. \rSon alrededor de 26 testigos tanto de cargo como de descargo los que han declarado durante la vista pública, entre ellos, peritos e investigadores. \rLa defensa sostiene que espera obtener una sentencia absolutoria, debido a que la Fiscalía no cuenta con los elementos de prueba para sostener la acusación contra Wachowski. \rLa exdiputada Yanci Urbina murió el pasado 29 de mayo del 2022, en su casa de habitación, en Antiguo Cuscatlán, departamento de La Libertad, aparentemente en un accidente, luego de una caída que posteriormente le habría provocado un paro cardíaco. \rLa Fiscalía sostiene que la muerte de la exdiputada se trató de un acto de violencia de género y no de un accidente por una caída. \rEn el transcurso del proceso, la Fiscalía ha manifestado que el cuerpo de Urbina tenía múltiples moretones, un golpe con objeto contundente y el tabique nasal quebrado. \rEl juicio inició el 3 de abril, inicialmente estaba programado para hacerse en dos días, pero debido a la cantidad de testigos se alargó.\n                \n\n\n\n",
        "title": "Suspenden hasta nuevo aviso juicio por feminicidio de Yancy Urbina",
        "sheet": {
            "indicators": [
                {
                    "indicator_name": "Clasificacion",
                    "response": "La noticia describe un homicidio, pero no es la muerte de la exdiputada Yancy Urbina. La noticia se centra en el juicio por feminicidio de la exdiputada Yancy Urbina, y no en su muerte."
                },
                {
                    "indicator_name": "Titulo",
                    "response": "**Título de la noticia:** Suspenden hasta nuevo aviso juicio por feminicidio de Yancy Urbina\n\n**Extraído:** El título de la noticia es \"Suspenden hasta nuevo aviso juicio por feminicidio de Yancy Urbina\"."
                },
                {
                    "indicator_name": "Resumen",
                    "response": "**Resumen:**\n\nLa noticia informa sobre el suspensión hasta nuevo aviso del juicio por feminicidio de Yancy Urbina, exdiputado del FMLN, contra su expareja, Peter Wachowski. El juicio se suspendió debido a la solicitud de una prueba por parte de la jueza. Una vez que la prueba sea incorporada, el juicio se reanudará y la jueza notificará a las partes de la nueva fecha. La defensa sostiene que espera obtener una sentencia absolutoria, debido a que la Fiscalía no cuenta con los elementos de prueba para sostener la acusación contra Wachowski."
                },
                {
                    "indicator_name": "Ubicacion del Suceso",
                    "response": "La información sobre el lugar donde ocurrió el suceso en la noticia es: Antiguo Cuscatlán, departamento de La Libertad."
                },
                {
                    "indicator_name": "Fuentes",
                    "response": "La información de la noticia no contiene fuentes de información, por lo que no se puede analizar la información de la misma para determinar su precisión."
                },
                {
                    "indicator_name": "Temas",
                    "response": "**Temas principales tratados en la noticia:**\n\n* **Juicio por feminicidio de Yancy Urbina:** El juicio contra el acusado de feminicidio, Peter Wachowski, se suspendió hasta nuevo aviso.\n* **Receso del juicio:** El juicio se suspendió debido a la solicitud de una prueba por parte de la jueza.\n* **Alegatos finales:** La vista pública continuación la presentación de los alegatos finales, donde la Fiscalía General y la defensa podrían solicitar sus sentencia.\n* **Defensa espera una sentencia absolutoria:** La defensa argumenta que no cuenta con los elementos de prueba para sostener la acusación.\n* **Causa de la muerte:** La Fiscalía sostiene que la muerte de la exdiputada se trata de un acto de violencia de género, no de un accidente."
                },
                {
                    "indicator_name": "Hechos Violativos",
                    "response": "La texto no contiene detalles sobre la violación a la ley, por lo que no se puede proporcionar la información requested."
                },
                {
                    "indicator_name": "Hipotesis de los Hechos",
                    "response": "**Teoría:**\n\nLa noticia indica que el juicio por feminicidio de Yancy Urbina se suspendió hasta nuevo aviso debido a una prueba que requiere ser incorporada. La defensa sostiene que espera obtener una sentencia absolutoria, debido a que la Fiscalía no cuenta con los elementos de prueba para sostener la acusación contra Wachowski.\n\n**Suposición:**\n\nEs probable que la prueba que requiere ser incorporada sea una prueba forense, como el análisis de las lesiones en el cuerpo de Urbina, para determinar si la muerte fue causada por violencia de género o por una caída."
                },
                {
                    "indicator_name": "Poblacion Vulnerable",
                    "response": "La texto no contiene información sobre grupos en riesgo, por lo que no se puede proporcionar la información requested."
                },
                {
                    "indicator_name": "Tipo de Arma",
                    "response": "La texto no menciona el tipo de arma que se utilizó en el feminicidio de Yancy Urbina, por lo que no se puede determinar si la información sobre el tipo de arma es completa o no."
                },
                {
                    "indicator_name": "Victimas",
                    "response": "La noticia describe el juicio por feminicidio de Yancy Urbina, exdiputado del FMLN, y no identifica a las víctimas. No se puede determinar si la noticia identifica a las víctimas o no."
                },
                {
                    "indicator_name": "Agresor o Sospechoso",
                    "response": "En la noticia, el nombre del agresor es **Peter Wachowski**."
                }
            ],
            "priority": 3,
            "id": "https://diario.elmundo.sv/nacionales/suspenden-hasta-nuevo-aviso-juicio-por-feminicidio-de-yancy-urbina"
        }
    },
    {
        "url": "https://diario.elmundo.sv/nacionales/programan-juicio-contra-acusado-del-feminicidio-de-fernanda-najera",
        "date": "2024-05-05",
        "sheet_id": "https://diario.elmundo.sv/nacionales/programan-juicio-contra-acusado-del-feminicidio-de-fernanda-najera",
        "source": "diario.elmundo.sv",
        "tag": "Feminicidio",
        "text": "\n        El Juzgado Especializado de Sentencia para una Vida Libre de Violencia y Discriminación para las Mujeres de San Salvador ha programado para el próximo 22 de abril el juicio en contra de Michael Alejandro Castillo Murga, acusado del feminicidio agravado de Melvi Fernanda Nájera Quezada y el homicidio tentado de su hijo. \rEn un principio el caso era conocido por un juzgado especializado de Santa Ana, sin embargo, por una resolución de una Cámara de lo Penal se trasladó el caso hacia San Salvador. \rEs la segunda programación del caso, ya que el pasado 14 de febrero se suspendió, debido a la incomparecencia de la Fiscalía General de la República, ya que eran parte del escrutinio final de las elecciones presidenciales y de diputados 2024. \rSegún la acusación de la Fiscalía, Fernanda Nájera de 23 años, fue encontrada muerta con múltiples lesiones ocasionadas con arma blanca, el 1 de febrero, en el kilómetro 99 de la carretera que de Ahuachapán conduce a Sonsonate, en la jurisdicción del cantón El Molino, del municipio de Concepción de Ataco. \rEl hijo de la víctima, de un año y siete meses, fue encontrado el 4 de febrero en un cafetal en estado de abandono y deshidratado. \rSegún el relato de la madre de Nájera, Michael Alejandro Castillo Murgas llegó a su casa el 31 de enero de 2019 a traer a su hija y a su nieto, supuestamente se dirigían a una diligencia para otorgarle su apellido al menor, sin embargo, nunca regresaron. \rLa Fiscalía General de la República acusó inicialmente a cinco personas por este caso, a Castillo Murgas por el delito de feminicidio agravado y homicidio tentado en perjuicio del hijo de la víctima. \rCastillo Murgas fue declarado rebelde y sobre él pesa una orden de captura internacional. El proceso lo enfrenta en calidad de reo ausente. Sobre el resto de procesados se desconoce en qué etapa avanzan el proceso penal.\n                \n\n\n\n",
        "title": "Programan juicio contra acusado del feminicidio de Fernanda Nájera",
        "sheet": {
            "indicators": [
                {
                    "indicator_name": "Clasificacion",
                    "response": "La noticia describe un homicidio, ya que incluye la muerte de una mujer por feminicidio y el hallazgo de su hijo en estado de abandono."
                },
                {
                    "indicator_name": "Titulo",
                    "response": "**Extraído el título de la noticia:**\n\nPrograman juicio contra acusado del feminicidio de Fernanda Nájera\n\n**Título:** Programan juicio contra acusado del feminicidio de Fernanda Nájera"
                },
                {
                    "indicator_name": "Resumen",
                    "response": "**Resumen:**\n\nLa noticia informa sobre el programacion del juicio contra el acusado de feminicidio de Fernanda Nájera, Michael Alejandro Castillo Murga. El juicio se programaará para el 22 de abril en San Salvador. El caso fue transfuerzado de Santa Ana a San Salvador por una resolución de una Cámara de lo Penal. La acusación de la Fiscalía indica que Nájera fue encontrada muerta con múltiples lesiones causadas con arma blanca. El hijo de la víctima fue encontrado en estado de abandono y deshidratado. Castillo Murgas ha sido declarado rebelde y sobre él pesa una orden de captura internacional."
                },
                {
                    "indicator_name": "Ubicacion del Suceso",
                    "response": "La noticia indica que el suceso ocurrió en el kilómetro 99 de la carretera que de Ahuachapán conduce a Sonsonate, en la jurisdicción del cantón El Molino, del municipio de Concepción de Ataco."
                },
                {
                    "indicator_name": "Fuentes",
                    "response": "La noticia no contiene ninguna fuente de información, por lo que no se puede proporcionar la cita de las fuentes de información."
                },
                {
                    "indicator_name": "Temas",
                    "response": "**Temas principales tratados en la noticia:**\n\n* **Juicio contra acusado de feminicidio:** La noticia informa sobre el juicio programado en contra de un acusado de feminicidio.\n* **Transferencia de caso:** El caso se trasladó de un juzgado especializado de Santa Ana a San Salvador por resolución de una Cámara de lo Penal.\n* **Suspendición del juicio:** El juicio se suspendió el pasado 14 de febrero debido a la incomparecencia de la Fiscalía General de la República.\n* **Acusación:** La Fiscalía General de la República acusó inicialmente a cinco personas por el caso, incluyendo al acusado de feminicidio.\n* **Declaración rebelde:** El acusado de feminicidio fue declarado rebelde y sobre él pesa una orden de captura internacional."
                },
                {
                    "indicator_name": "Hechos Violativos",
                    "response": "La noticia no contiene detalles sobre la violación a la ley, por lo que no se puede proporcionar la información requesteda."
                },
                {
                    "indicator_name": "Hipotesis de los Hechos",
                    "response": "**Teoría:**\n\nLa noticia informa sobre el programacion del juicio contra el acusado de feminicidio de Fernanda Nájera, Michael Alejandro Castillo Murga. La noticia sigue un orden lógico, presenta la información de manera concisa y clara, y incluye los detalles relevantes del caso.\n\n**Suposición:**\n\nLa noticia asume que el juicio se llevará a cabo en el fecha y lugar indicados, y que el proceso se desarrollará de acuerdo con la ley. No se hace ninguna suposición sobre la culpabilidad del acusado o el resultado del juicio."
                },
                {
                    "indicator_name": "Poblacion Vulnerable",
                    "response": "La texto no contiene información sobre grupos en riesgo, por lo que no se puede proporcionar la información requesteda."
                },
                {
                    "indicator_name": "Tipo de Arma",
                    "response": "La noticia no indica el tipo de arma utilizada en el feminicidio, por lo que no se puede proporcionar la información sobre el tipo de arma."
                },
                {
                    "indicator_name": "Victimas",
                    "response": "**Identifica a las víctimas en la noticia:**\n\nLa noticia identifica a las víctimas como Melvi Fernanda Nájera Quezada, de 23 años, y su hijo, de un año y siete meses."
                },
                {
                    "indicator_name": "Agresor o Sospechoso",
                    "response": "La información sobre el nombre del agresor en la noticia no se encuentra en el texto, por lo que no se puede proporcionar la información solicitada."
                }
            ],
            "priority": 3,
            "id": "https://diario.elmundo.sv/nacionales/programan-juicio-contra-acusado-del-feminicidio-de-fernanda-najera"
        }
    },
    {
        "url": "https://diario.elmundo.sv/nacionales/hombre-fue-asesinado-con-arma-blanca-en-san-miguel",
        "date": "2024-05-05",
        "sheet_id": "https://diario.elmundo.sv/nacionales/hombre-fue-asesinado-con-arma-blanca-en-san-miguel",
        "source": "diario.elmundo.sv",
        "tag": "Homicidio",
        "text": "\n        La Policía Nacional Civil (PNC) informó este viernes del homicidio de un hombre de 69 años de edad en El Tránsito en el departamento de San Miguel. Según la PNC, el hombre murió tras ser atacado con arma blanca. \r\"Nuestros agentes ya trabajan para resolver este caso\", dijo la PNC. \rEn los tres primeros días de mayo ya se reportan tres homicidios, dos ocurrieron el pasado 1 de mayo, uno en San Salvador luego de recibir una golpiza de un amigo con el que estaba ingiriendo bebidas alcohólicas y otro más en Ciudad Barrios, en San Miguel, de este último se desconocen los hechos.\n\n\n\n\n",
        "title": "Hombre fue asesinado con arma blanca en San Miguel",
        "sheet": None
    },
    {
        "url": "https://diarioelsalvador.com/barbero-enfrentara-audiencia-por-agredir-sexualmente-a-nina-en-mercado-sagrado-corazon/500259/",
        "date": "2024-05-06",
        "sheet_id": "https://diarioelsalvador.com/barbero-enfrentara-audiencia-por-agredir-sexualmente-a-nina-en-mercado-sagrado-corazon/500259/",
        "source": "diarioelsalvador.com",
        "tag": "Homicidio",
        "text": "El Juzgado Sexto de Paz de San Salvador, comenzará este lunes el proceso penal a Roberto Mauricio Villalta, de 42 años, por el delito de agresión sexual en menor e incapaz. El caso del imputado se conoció a través de redes sociales, en un video que fue divulgado se observa que se acerca a una niña para tocarla, pero la menor salió corriendo en un pasillo del Mercado Sagrado Corazón de San Salvador. La Policía Nacional Civil (PNC) informó de la captura el pasado 25 de abril, ese día la institución publicó que «además de los videos que se difundieron en redes sociales, hemos recabado otros vídeos de cámaras cercanas y múltiples testigos» Según el informe policial, «Villalta trabajaba como barbero y su modus operandi era pasar por el mercado observando a los niños y tratando de tocarlos cuando los padres se descuidaban». Tras ser arrestado y fichado, la PNC encontró en su base de datos que en el 2014, fue detenido por agredir sexualmente a otra niña, pero fue puesto en libertad por el sistema judicial de ese año. «Posteriormente fue detenido por agredir a una mujer, pero un juzgado determinó que sólo recibiera una orden de alejamiento, luego fue capturado porque incumplió esa orden de alejamiento», señala la Policía. Tiene antecedentes por los delitos de hurto, amenazas y extorsión, pero siempre fue exonerado por diversos juzgados. La Fiscalía General de la República ha solicitado que por este nuevo caso se le decrete detención provisional mientras el expediente avanza a la segunda fase.  ",
        "title": "Barbero enfrentará audiencia por agredir sexualmente a niña en mercado Sagrado Corazón",
        "sheet": None
    },
    {
        "url": "https://diarioelsalvador.com/pandillero-responsable-de-homicidio-fue-capturado-en-ahuachapan/500229/",
        "date": "2024-05-06",
        "sheet_id": "https://diarioelsalvador.com/pandillero-responsable-de-homicidio-fue-capturado-en-ahuachapan/500229/",
        "source": "diarioelsalvador.com",
        "tag": "Homicidio",
        "text": "La Policía Nacional Civil (PNC) confirmó el pasado domingo por la noche la captura de un sujeto perteneciente a grupos de pandillas y responsable de un homicidio. El detenido responde al nombre de Josué Vladimir Terán Canizalez, alias Black, perfilado como miembro activo de las estructuras terroristas de la pandilla Barrio 18. Capturamos a Josué Vladimir Terán Canizales, alias Black, terrorista del Barrio 18, quien es el responsable de asesinar a un hombre en el año 2021, en Atiquizaya, Ahuachapán.Este criminal será procesado por homicidio agravado y pasará varias décadas en la cárcel.… pic.twitter.com/lfkL2VVGj0 Según la institución policial, Terán Canizalez es el responsable de un homicidio cometido en el sector de Atiquizaya, en Ahuachapán, el pasado año 2021. La Policía detalló que Terán Canizalez será entregado a las autoridades correspondientes para ser procesado por el delito de homicidio agravado.",
        "title": "Pandillero responsable de homicidio fue capturado en Ahuachapán",
        "sheet": None
    },
    {
        "url": "https://diarioelsalvador.com/congresistas-democratas-piden-a-biden-revivir-titulo-42/500161/",
        "date": "2024-05-06",
        "sheet_id": "https://diarioelsalvador.com/congresistas-democratas-piden-a-biden-revivir-titulo-42/500161/",
        "source": "diarioelsalvador.com",
        "tag": "Homicidio",
        "text": "Cinco legisladores demócratas de la Cámara de Representantes de Estados Unidos solicitaron al presidente Joe Biden retomar la controversial política de expulsión a los migrantes: el Título 42, con la intención de contener la migración irregular en la frontera con México, en un año electoral en el que este tema se convierte en uno de los principales escenarios políticos. Los parlamentarios Marie Gluesenkamp Pérez, Jared Golden, Mary Peltola, Vicente González y Don Davis exigieron tomar medidas inmediatas sobre seguridad fronteriza. El Título 42 cumplirá un año de haber sido declarada nula en la frontera el 11 de mayo, después de que fue impulsada por el presidente Donald Trump en 2020 en el contexto de una emergencia de salud pública por la pandemia por la COVID-19 y extendida por la administración de Biden. La medida restringía el derecho de solicitar asilo en la frontera a los migrantes que intentaban ingresar a suelo estadounidense sin autorización y eran deportados inmediatamente, con el objetivo de desalentar los flujos masivos. «Nuestros intereses de seguridad nacional no se detienen en nuestras fronteras físicas. Por eso votamos a favor de enviar más armas a Ucrania para su lucha contra Rusia», indicó Pérez en un comunicado. «Más allá de defender a nuestros aliados, estamos totalmente de acuerdo con el Consejo Nacional de la Patrulla Fronteriza en que el Congreso y el presidente [Biden] deben actuar y poner orden en la frontera sur», exhortó. La congresista recordó que por eso también votó a favor por $19.6 mil millones en marzo para la Patrulla Fronteriza, «para que pudiera intensificar sus esfuerzos en asegurar la frontera». El monto representa $3.2 mil millones más que en el año fiscal 2023, compartió el periódico británico «Daily Mail». «Hacemos un llamado a los líderes tanto de la Cámara como del Senado para que aprueben legislación para devolver a la Patrulla Fronteriza la autoridad de expulsión que expiró el año pasado», insistió. Sin embargo, aunque el Título 42 es una referencia de bloqueo de la migración irregular para los políticos, un estudio del Instituto de Política Migratoria revela que no obtuvo el éxito que señalan y que incluso se puede describir como una disuasión fallida. El informe indica que durante su uso —de marzo de 2020 a mayo de 2023— aumentó el número de encuentros (detenciones y expulsiones) y los casos de migrantes que intentaban reingresar sin autorización, llegando a casi 3 millones de veces. Según el documento, los migrantes, al no enfrentar «consecuencias formales por su entrada irregular, como el procesamiento penal por entrada o reingreso ilegal», sino como única alternativa la expulsión exprés, siguieron intentando cruzar hasta lograrlo. El mismo caso ocurrió en el número de «fugas», un término utilizado por la Oficina de Aduanas y Protección Fronteriza (CBP, en inglés) de Estados Unidos para referirse a los migrantes que no fueron interceptados mientras cruzaban la frontera ilegalmente.",
        "title": "Congresistas demócratas piden a Biden revivir Título 42",
        "sheet": None
    },
    {
        "url": "https://diarioelsalvador.com/terremoto-de-magnitud-53-sacude-la-region-china-de-taiwan/500234/",
        "date": "2024-05-06",
        "sheet_id": "https://diarioelsalvador.com/terremoto-de-magnitud-53-sacude-la-region-china-de-taiwan/500234/",
        "source": "diarioelsalvador.com",
        "tag": "Homicidio",
        "text": "Un terremoto de magnitud 5,3 sacudió la zona marina del distrito de Hualien de la isla china de Taiwan a las 17:45 de hoy lunes (hora de Beijing), según el Centro de Redes Sismológicas de China (CENC, siglas en inglés). El epicentro fue monitoreado en 23,71 grados de latitud norte y 121,62 grados de longitud este. El sismo se registró a una profundidad de 20 kilómetros, de acuerdo con un informe publicado por el CENC. A las 17:52, un nuevo temblor, esta vez de magnitud 5,2, sacudió una zona adyacente, cuyo epicentro se localizó en 23,7 grados de latitud norte y 121,57 grados de longitud este. El segundo sismo se registró a una profundidad de 25 kilómetros.",
        "title": "Terremoto de magnitud 5,3 sacude la región china de Taiwan",
        "sheet": None
    },
    {
        "url": "https://diarioelsalvador.com/el-salvador-registra-un-segundo-dia-con-cero-homicidios-en-el-inicio-de-mayo-2024/500219/",
        "date": "2024-05-06",
        "sheet_id": "https://diarioelsalvador.com/el-salvador-registra-un-segundo-dia-con-cero-homicidios-en-el-inicio-de-mayo-2024/500219/",
        "source": "diarioelsalvador.com",
        "tag": "Homicidio",
        "text": "El Salvador sigue sumando días con cero homicidios en el presente año 2024, específicamente en el inicio del mes de mayo, según detallaron los registros de la Policía Nacional Civil (PNC) publicados en la madrugada de este lunes. Los datos oficiales de la corporación policial señalan que el domingo 5 de mayo finalizó con cero homicidios en el territorio salvadoreño, convirtiéndose en la segunda jornada con esta cifra de cinco que se han cumplido en el presente mes. Estos dos días contabilizados en los inicios de mayo 2024 se suman a las 19 jornadas con las que finalizó el pasado mes de abril y a las 21 que registró marzo de este año. Esto también se suma a los 48 días sin homicidios que sumaron los meses de enero y febrero. Finalizamos el domingo 05 de mayo, con 0 homicidios en el país. pic.twitter.com/2evVt6PJ8F Esto deja un total de 90 días con cero homicidios registrados en El Salvador en lo que va del presente año 2024, lo que mantiene la tendencia establecida en 2022 y 2023, cuando El Salvador comenzó a registrar un descenso histórico en la violencia homicida. Estos registros han sido posibles gracias a la implementación del Plan Control Territorial, estrategia que inició desde 2019, año que inició el período presidencial de Nayib Bukele en El Salvador y que ha permitido un combate frontal contra la criminalidad y las pandillas. De igual forma, el régimen de excepción, aprobado en marzo de 2022 y aún vigente en El Salvador, es otra de las estrategias que ha permitido la captura de más de 70,000 miembros y colaboradores de grupos de pandillas, generando una reducción del accionar de estos grupos terroristas en el país.",
        "title": "El Salvador registra un segundo día con cero homicidios en el inicio de mayo 2024",
        "sheet": None
    },
    {
        "url": "https://diarioelsalvador.com/batallas-contra-la-voluntad-soberana/500184/",
        "date": "2024-05-06",
        "sheet_id": "https://diarioelsalvador.com/batallas-contra-la-voluntad-soberana/500184/",
        "source": "diarioelsalvador.com",
        "tag": "Homicidio",
        "text": "Diversos sondeos sobre el régimen de excepción se han realizado desde que inició la medida ordenada por el presidente Nayib Bukele, como parte del Plan Control Territorial. Obviamente, no los hacen para mostrar al mundo el respaldo que la población le da porque ahora vive en paz, en tranquilidad, en verdadera seguridad.  No recuerdo mediciones hechas por las diferentes casas encuestadoras de cómo se sentía el salvadoreño trabajador, luchador, honrado y honesto sobre el clima de violencia, luto y dolor que generaban los grupos criminales. Hablo de dos décadas sangrientas que dejaron más de 110,000 salvadoreños asesinados. Por cierto, son más que los que dejó la guerra civil protagonizada por la derecha y la izquierda.  Tampoco recuerdo encuestas específicas de cómo evaluaban los planes de seguridad en los gobiernos de ARENA y el FMLN. Claro, no les interesaba hacerlas, pues formaban parte del sistema bipartito corrupto, amalgamado por el poder fáctico.  Hay dos verdades a dos años del régimen. Y para decirlo, tomaré como base el último sondeo de la institución académica férrea opositora del Gobierno del presidente Bukele: la primera es que 8.13 de cada 10 aprueban y respaldan la medida de seguridad. Suponiendo que no alteraron el porcentaje, es un número sin más que decir.  La segunda, a las ONG nacionales e internacionales, a sus medios de prensa aliados y políticos rastreros les revienta el total respaldo de salvadoreños honrados y honestos a la medida, al grado que no cesan sus batallas internacionales por derribar el régimen de excepción, por lograr que sus «angelitos» salgan de nuevo a las calles a continuar asesinando al pueblo, a asediar y violar a estudiantes, a extorsionar todo tipo de comercios.  Sus mismas familias, sus mismos hijos, padres, abuelos, todos, caminan con tranquilidad ahora en cualquier parte del territorio nacional, gracias al único plan de seguridad que ha dado resultados contundentes en el país.  Este bloque opositor vive especulando y mintiendo que los salvadoreños nos movemos con miedo al régimen, que tenemos nuestros derechos restringidos. Para las ONG y los plumíferos aliados, los miles de salvadoreños a quienes se les ha salvado la vida no valen nada. Solo les interesa el «bienestar» de los pandilleros asesinos. Ya ni los resultados de las elecciones, en las que la voluntad del soberano quedó nuevamente revelada, los mueve.  El pueblo sabe que esos organismos nacionales y extranjeros, y los plumíferos «incómodos», son pordioseros del financiamiento que reciben por mantener esas luchas, aunque vayan en contra de la vida de la gran mayoría de la gente honesta.  La insistencia de presentar ante organismos internacionales «informes» del régimen de excepción, con datos no oficiales, elaborados por las mismas ONG activistas, es de estudio.  Otra verdad hay en esto: sus batallas en contra del régimen simplemente son en favor de esos grupos criminales. ¿Por qué? Porque tienen la idea de que el regreso sangriento que ocasionan esos grupos permitirá la caída del mejor presidente que El Salvador ha tenido, y así regresar al sistema bipartito corrupto de ARENA y el FMLN, en el que se sentaban a la mesa a deleitarse con sus manjares.  ¿Qué es lo que no entienden de la voluntad del soberano, del pueblo?, ¿qué es lo que no entienden de los más de 2.7 millones de votos que recibió Nayib para ¡un segundo mandato!?  Una buena nueva hay para más de 6 millones de salvadoreños y, por supuesto, mala para los parásitos: el pueblo seguirá teniendo la oportunidad de decidir los grandes cambios en la nación. Otra gran tarea para ocupar la mente retrógrada de ONG, plumíferos, leguleyos «constitucionalistas», mercaderes de la fe y políticos rastreros.  No pueden ni podrán contra la voluntad del pueblo, el único soberano. ",
        "title": "Batallas contra la voluntad soberana",
        "sheet": None
    },
    {
        "url": "https://diarioelsalvador.com/realizan-patrullajes-preventivos-en-centros-de-tolerancia-y-bares-de-el-salvador/500224/",
        "date": "2024-05-06",
        "sheet_id": "https://diarioelsalvador.com/realizan-patrullajes-preventivos-en-centros-de-tolerancia-y-bares-de-el-salvador/500224/",
        "source": "diarioelsalvador.com",
        "tag": "Homicidio",
        "text": "Elementos de la Policía Nacional Civil (PNC) se desplegaron en diversos centros de tolerancia, discotecas y bares de distintas zonas de El Salvador para realizar operativos preventivos entre la noche del domingo y la madrugada de este lunes. Estos operativos buscan verificar que este tipo de establecimientos nocturnos no estén sirviendo como puntos de refugio para criminales o pandilleros, ni como centros de tráfico de ilícitos. Verificamos que en todos los centros de tolerancia del país, se cumpla la ley:▪️ Chalatenango▪️San Miguel▪️ Usulután▪️La UniónAdemás, nos aseguramos que ningún menor de edad sea expuesto a estos lugares.#PlanControlTerritorial pic.twitter.com/QuTloQ8ubh El despliegue incluyo bares y centros de tolerancia ubicados en los departamentos de Chalatenango, La Unión, Usulután y San Miguel, como parte de las medidas implementadas por las autoridades para combatir la criminalidad en el país. De igual forma, las autoridades policiales inspeccionan que no se cometan abusos contra menores de edad en estos lugares. El operativo se extendió por varias horas y abarcó diversos establecimientos de la ciudad capital. La institución policial mantiene este tipo de operativos constantemente como parte de las estrategias en el combate a la delincuencia, la criminalidad y las pandillas en todo el territorio salvadoreño.",
        "title": "Realizan patrullajes preventivos en centros de tolerancia y bares de El Salvador",
        "sheet": None
    },
    {
        "url": "https://diarioelsalvador.com/guatemala-ha-capturado-41-pandilleros-que-huyeron-del-regimen-de-excepcion-en-este-ano/500264/",
        "date": "2024-05-06",
        "sheet_id": "https://diarioelsalvador.com/guatemala-ha-capturado-41-pandilleros-que-huyeron-del-regimen-de-excepcion-en-este-ano/500264/",
        "source": "diarioelsalvador.com",
        "tag": "Homicidio",
        "text": "Entre el 1 de enero y 5 de mayo de 2024, la Policía Nacional Civil (PNC) de Guatemala, ha capturado a 41 pandilleros salvadoreños que huyeron del régimen de excepción implementado por el Gobierno. Según el informe oficial, de todos los detenidos 14 están guardando prisión en el sistema penitenciario de ese país por diversos delitos de crimen organizado. Otros 27 de los terroristas arrestados fueron entregados a las autoridades de El Salvador ya que en ese país no habían cometido delito, pero como parte de la colaboración entre las Policías de ambas naciones, los trasladaron a las cuatro fronteras terrestres para garantizar que no regresaran y que se les siga el respectivo proceso en los tribunales por el delito de agrupaciones ilícitas. Los mareros que han quedado en prisión en Guatemala, incurrieron en casos de extorsión, robo y homicidio, delitos por los cuales les están siguiendo un expediente penal. La última captura reportada por la PNC de Guatemala fue el pasado domingo, cuando en la Zona 1 de Jutiapa, investigadores de la División Nacional contra el Desarrollo Criminal de las Pandillas (Dipanda) capturaron a Eduardo Edenilson Hernández Hernández, alias, «El Triby» de la Mara Salvatrucha. «Este individuo se encontraba en territorio guatemalteco tras escapar de la guerra contra pandillas. Por encontrarse de manera irregular en Guatemala e incumplir con los protocolos migratorios, fue remitido al Instituto Guatemalteco de Migración IGM de la frontera San Cristóbal, Atescatempa, Jutiapa y entregado a las autoridades de El Salvador», publicó la PNC del vecino país. En El Salvador, Hernández, ya fue entregado a la Policía y será remitido a la Fiscalía General de la República para que un tribunal contra el crimen organizado le inicie un proceso por el delito de agrupaciones ilícitas. Este ilícito es aplicado a los imputados que forman parte de una pandilla, grupos considerados como organizaciones terroristas según una resolución de la Sala de lo Constitucional de la Corte Suprema de Justicia. En lo que va del año, 41 pandilleros salvadoreños han sido localizados en Guatemala, de los que 14 guardan prisión en nuestro país y 27 han sido entregados a las autoridades de @PNCSV.¡No hay mañana!#LaSeguridadEsHoy pic.twitter.com/jyU40R7lEr",
        "title": "Guatemala ha capturado 41 pandilleros que huyeron del régimen de excepción en este año",
        "sheet": None
    },
    {
        "url": "https://diarioelsalvador.com/criminalidad-en-ecuador-crece-de-forma-alarmante-dice-jefa-de-unodc/500412/",
        "date": "2024-05-06",
        "sheet_id": "https://diarioelsalvador.com/criminalidad-en-ecuador-crece-de-forma-alarmante-dice-jefa-de-unodc/500412/",
        "source": "diarioelsalvador.com",
        "tag": "Homicidio",
        "text": "La directora ejecutiva de la agencia de las Naciones Unidas contra la Droga y el Delito (UNODC), Ghada Waly, afirmó este lunes que la amenaza del crimen organizado ha aumentado «de forma brusca y alarmante» en Ecuador, donde la oficina estableció una nueva sucursal. «En los últimos meses, la amenaza que representan las bandas y los grupos criminales en Ecuador se ha intensificado de forma brusca y alarmante, socavando la paz y la prosperidad», dijo Waly en una conferencia de prensa en Quito este lunes, cuando se inauguró la nueva sede.  La expansión del tráfico de droga, especialmente de cocaína, «ha desencadenado la competencia criminal (…) desatando la violencia en las calles y cárceles de Ecuador», añadió.  De acuerdo con la UNODC, al menos el 80% de los homicidios en Ecuador se atribuyen al crimen organizado. La tasa de homicidios trepó en 2023 al récord de 43 por cada 100.000 habitantes, mientras que en 2018 era de 6, según cifras oficiales.  En ese contexto, la agencia estableció una oficina en Quito con miras a «intensificar el apoyo» en la lucha contra el narcotráfico en el país, donde el año pasado se decomisaron cerca de 220 toneladas de droga. Ubicado entre Colombia y Perú -los mayores productores mundiales de cocaína- Ecuador dejó hace años de ser una isla de paz y se convirtió en un centro logístico para el envío de droga, principalmente cocaína, hacia Europa y Estados Unidos. La canciller ecuatoriana, Gabriela Sommerfeld, expresó que el plan de compromisos con la UNODC tiene seis ejes que incluyen la lucha contra la corrupción en los puertos, el combate al lavado de activos, el refuerzo de la seguridad marítima y fluvial y la cooperación internacional. «La UNODC ha sido un actor clave para el Ecuador con la que podemos contar para recuperar la paz», dijo Sommerfeld.",
        "title": "Criminalidad en Ecuador crece de forma «alarmante», dice jefa de UNODC",
        "sheet": None
    },
    {
        "url": "https://www.diariocolatino.com/ulloa-reconoce-regimen-excepcion-detenciones-ilegales/",
        "date": "2024-05-06",
        "sheet_id": "https://www.diariocolatino.com/ulloa-reconoce-regimen-excepcion-detenciones-ilegales/",
        "source": "diariocolatino.com",
        "tag": "Homicidio",
        "text": "\n\nCompartir\n\n Facebook\n Twitter\n Google +\n\n\n\n\n\nArtículos relacionados\n\n\n\n\n\n \n\n\nApoyan demanda de libertad de hijo de líder indígena\n4 mayo, 2024\n\n\n\n\n \n\n\nEl Salvador cerca de 20 jornadas sin homicidios en abril\n28 abril, 2024\n\n\n\n\n \n\n\nFESPAD pide a Centros Penales cumpla orden de libertad de Levi Morales \n27 abril, 2024\n\n\n\n\nSamuel Amaya\n@SamuelAmaya98\nEl vicepresidente electo de la República, Félix Ulloa, reconoció en una entrevista televisa que durante el estado de excepción se han cometido detenciones ilegales contra miles de salvadoreños que nada tienen que ver con pandillas.\nEn el espacio “Las Cosas Como Son”, el vicepresidente electo sostuvo que “nosotros lo hemos reconocido, ha habido capturas ilegales, más de 7 mil personas han salido libres, más de 7 mil que han comprobado que no tienen vinculación con las pandillas o que estuvieron en el lugar y hora equivocada cuando los capturaron, (pero) han salido en libertad”, comentó Ulloa.\nEsto surgió luego que Ulloa fue cuestionado del porqué hay organizaciones defensoras de derechos humanos que critican la medida. El funcionario afirmó que los defensores de DDHH tienen antecedentes de pertenecer a partidos políticos, “estás hablando de voceros de un partido que no tiene el liderazgo político para salir por sí mismo, entonces, utiliza a estas oenegés para criticar al Gobierno, porque el partido como tal, no tiene autoridad moral ni respaldo político para criticar, entonces, usa a instituciones para hacerlo”.\nUlloa atacó a CRISTOSAL, al plantear que Ruth López, Zaira Navas y David Morales pertenecían al partido político Frente Farabundo Martí para la Liberación Nacional (FMLN). Sobre las detenciones arbitrarias, el entrevistador no quiso profundizar en los cuestionamientos.\nEl régimen de excepción inició el 27 de marzo de 2022 luego de un repunte en los homicidios que dejó como saldo a más de 80 salvadoreños muertos.\n\nRelacionado\n\n",
        "title": "Ulloa reconoce que en régimen de excepción han cometido detenciones ilegales",
        "sheet": None
    },
    {
        "url": "https://www.diariocolatino.com/por-sus-frutos-los-conocereis-2/",
        "date": "2024-05-06",
        "sheet_id": "https://www.diariocolatino.com/por-sus-frutos-los-conocereis-2/",
        "source": "diariocolatino.com",
        "tag": "Homicidio",
        "text": "\n\nCompartir\n\n Facebook\n Twitter\n Google +\n\n\n\n\n\nArtículos relacionados\n\n\n\n\n\n \n\n\nDesafíos para la izquierda salvadoreña\n1 mayo, 2024\n\n\n\n\n \n\n\nInstalan en El Salvador nueva Asamblea Legislativa\n1 mayo, 2024\n\n\n\n\n \n\n\nLa última jugada política de Bukele y su bancada Cyan\n30 abril, 2024\n\n\n\n\nPor Colectivo Tetzáhuitl* \n \nA un Presidente se le debe juzgar por sus acciones y no por ofrecimientos o declaraciones demagógicas… \n“En aquel tiempo, dijo Jesús a sus discípulos: Cuidado con los profetas falsos; se acercan con piel de oveja, pero por dentro son lobos rapaces. Por sus frutos los conoceréis…” (Mateo 7, 15-20)\nFrutos, obras, acciones, da igual.\nLo importante es que a un político, a un dirigente de partido, a un funcionario público y sobre todo a un Presidente de la República se le debe juzgar no por lo que declara sino por lo que hace, no por lo que promete y dice que va a hacer ya en el cargo, sino por lo que realmente hace o está dispuesto a hacer.\nA un funcionario se le evalúa además por lo que no hace a pesar de que lo ofreció y podría haberlo hecho.\nEn tal sentido, a Bukele, su gobierno, Nuevas Ideas y el bloque de derecha que representan hay que juzgarlos por lo que hicieron hasta ahora una vez asumieron el control de la Presidencia y no tanto por lo que prometieron en campaña en el 2019.\nBukele se vendió como un candidato de izquierda, identificado con los intereses populares y esencialmente anti oligárquico.\nCon ese espíritu inició su carrera política de la mano de José Luis Merino, ex dirigente del FMLN, allá por el año 2012 como alcalde de Nuevo Cuscatlán.\nEnarbolando la bandera de la anti política y la anti corrupción, Bukele comenzó a criticar a los gobiernos del FMLN y a tomar distancia de la dirigencia del partido hasta conquistar el voto de la izquierda y ganar las elecciones presidenciales del 2019 bajo la bandera de un partido de derecha, paradójicamente acusado de corrupción y de ser un partido tradicional.\nYa en el control del cargo presidencial, Bukele comenzó a hacer todo lo contrario de lo que había ofrecido y que prometió que iba a hacer.\nOfreció combatir la corrupción tanto en el gobierno como la promovida por los grupos empresariales.\nEn sus primeros cuatro años en la Presidencia no hizo absolutamente nada al respecto.\nPor el contrario, restringió drásticamente el acceso a la información de naturaleza pública y ordenó el cierre de todos los expedientes abiertos por el ex Fiscal General Raúl Melara en contra de su gobierno.\nEs decir, no solo bloqueó las investigaciones penales en contra de sus funcionarios más cercanos, sino que consintió y hasta ocultó las habituales prácticas corruptas de sus\nfuncionarios que habían sido detectadas por la Comisión Investigadora de la OEA (CICIES), la que acabó disolviendo.\nEntre estos expedientes se encontraba una voluminosa investigación denominada “Catedral”, centrada en tres emblemáticos casos: Las negociaciones con las Pandillas, la corrupción en la entrega de alimentos durante la pandemia del COVID y la creación de una organización criminal creada para saquear fondos públicos y que era manejada desde Casa Presidencial por la Jefa de Gabinete, Carolina Recinos de Bernal, los hermanos de Bukele, el Secretario de Comercio de CAPRES y tío de Nayib y el Presidente de Nuevas Ideas, Xavier Zablah.\nLa investigación fue literalmente cerrada y los fiscales que habían participado en ella fueron perseguidos y amenazados hasta exiliarse.\nHace un año, con ocasión de su cuarto aniversario, Bukele anunció en la Asamblea Legislativa una “Guerra contra las Pandillas” y puso de ejemplo el inicio de un proceso penal contra el ex Presidente Alfredo Cristiani, acusado de haber malversado fondos públicos cuando fue Presidente entre 1989 y 1994.\nEn esa ocasión, reunió en Casa Presidencial a todo su gabinete y les dijo a los funcionarios que asistieron que no pasaría a la historia como un Presidente que había robado y que además no deseaba que se le recordara como un Presidente, tal como ocurrió con Napoleón Duarte, que aunque no había robado sí estuvo en cambio rodeado de funcionarios ladrones y corruptos.\nSus palabras fueron interpretadas como una amenaza directa a sus funcionarios de que no vacilaría en meterlos presos si llegaban a manejar indebidamente fondos públicos.\nHace unos días, la Fiscalía dio a conocer la captura del Comisionado Presidencial para Proyectos Estratégicos, Christian Flores, acusado del delito de Cohecho o soborno.\nSegún las investigaciones del Ministerio Público, Christian Flores cobraba comisiones en dinero por el otorgamiento de algunos proyectos municipales y nacionales bajo su responsabilidad.\nEl caso ha sido exhibido como una muestra más de esta “cruzada nacional” en contra de la corrupción.\nLos mismo hizo meses atrás cuando ordenó la captura del entonces Presidente de BANDESAL, Juan Pablo Durán, por los delitos de Actos Arbitrarios y Cohecho Impropio en perjuicio de la administración pública.\nPese a algunas detenciones, entre ellas las de un Diputado se Nuevas Ideas, acusado de falsedad ideológica y material, Bukele continúa sin explicar por qué la Fiscalía no procesa a los funcionarios cercanos de su gobierno sobre los cuales se tienen suficientes pruebas de que han cometido actos de corrupción que han afectado las finanzas públicas.\nAlgunos de ellos hasta aparecen en el listado de corruptos del Departamento de Estado y del Departamento del Tesoro de EEUU.\nTampoco ha explicado por qué le ordenó al Fiscal Rodolfo Delgado que cerrara los expedientes de investigación penal que había abierto el ex Fiscal Raúl Melara y que contenían abundante evidencia en contra de los funcionarios investigados.\nMientras no explique esas decisiones controversiales, Bukele podría pasar a la historia como un Presidente que si bien no robó, afirmación que solo él y su gobierno sostienen en público, sí en cambio protegió a funcionarios corruptos de su gobierno y los encubrió e impidió que fueran investigados y enjuiciados.\nDeterioro de la economía y de las condiciones de vida de la población… \nLo mismo podría decirse de las promesas económicas y sociales hechas en el 2019.\nBukele ofreció una reforma tributaria progresiva en la que deberían pagar más impuestos aquellos contribuyentes que ganan más ingresos.\nSin embargo, después de cinco años en la Presidencia y con el control absoluto de las decisiones legislativas, el país sigue teniendo una política tributaria regresiva que hace caer el peso de la fiscalidad en los pobres y en la clase media.\nTampoco acabó con los privilegios económicos de los grupos empresariales oligárquicos, como dijo que lo haría.\nPor el contrario, fortaleció su presencia en la economía nacional y aumentó la concentración de la riqueza en pocas manos.\nPara el 2023, el 10% más rico del país concentraba el 60% de la riqueza nacional.\nMientras que el 50% de las familias de menores ingresos apenas tenían acceso a menos del 5% del PIB.\nComo hemos señalado en otras ocasiones, 160 millonarios del país acaparan casi el 90% de la renta nacional y un solo grupo empresarial, el grupo Kriete, dedicado a la aviación comercial entre otros negocios, tiene un patrimonio de más de 7 mil millones dólares, es decir, cerca del 20% del PIB.\nBajo el gobierno de Bukele los ricos son más ricos y los pobres más pobres.\nLejos de disminuir la pobreza de ingresos, tal como prometió, esta pobreza aumentó en un 5%, volviendo a los niveles de finales del gobierno de Saca.\nEn cinco años pasaron a formar parte de los cinturones de pobreza 255 mil salvadoreños más de los que había en el 2019.\nEn la administración Bukele el poder adquisitivo de los salvadoreños se ha reducido y sus condiciones de vida se han deteriorado.\nY en esto no solo han tenido que ver los problemas económicos y sociales que generó la pandemia del COVID o las crisis económicas internacionales.\nEn cinco años Bukele no ha sido capaz de diseñar un programa de reactivación económica del país, basado en una mayor atracción de inversión extranjera directa (IED) y de inversión privada nacional.\nLa inversión pública ha caído en todos estos años y el programa de inversiones contemplado en el Presupuesto Público apenas se ha concretado en un 60%.\nLas finanzas del gobierno se han deteriorado y la deuda pública se ha disparado a más de 30 mil millones de dólares, es decir, un poco más del 90% del PIB.\nEl gasto social también se ha contraído.\nDe hecho fueron suprimidos una docena de programas sociales que venían de los gobiernos del FMLN y otra docena más han sido desfinanciados.\nEn campaña, Bukele dijo que aumentaría el gasto social, sobre todo en Salud y Educación.\nPrometió a los estudiantes de la UES que aumentaría el Presupuesto de la Universidad hasta convertirlo en uno de los más altos de la región.\nNo solo no lo aumentó sino que en estos momentos tiene una deuda de más de 70 millones de dólares con el Alma Mater, lo que le está provocando serios problemas financieros a la institución.\nTampoco construyó las sedes regionales universitarias que ofreció y no marchó con los estudiantes como dijo que lo haría para exigir un aumento presupuestario a la Asamblea.\nYa en la Presidencia desfinanció programas estratégicos de alto impacto social como Ciudad Mujer, la Pensión Básica para Adultos Mayores, la entrega de paquetes agrícolas y la entrega de los paquetes escolares, el vaso de leche y la alimentación escolar, entre otros.\nEn cinco años de gobierno de Bukele cayeron la mayoría de los indicadores sociales que habían mejorado en los diez años de gobiernos del FMLN.\nEntronización de la Dictadura… \nA nivel político en estos cinco años el país ha retrocedido en términos de convivencia democrática.\nEl Estado de Derecho y el orden constitucional han sido vulnerados en varias ocasiones.\nEl país se ha convertido en una autocracia donde una sola persona concentra la casi totalidad del poder político para beneficio del clan gobernante.\nBukele ofreció más democracia, respeto a las Leyes y a la Constitución y una nueva forma de hacer política que le diferenciaría de los anteriores gobiernos.\nPero desde que asumió el cargo de Presidente se ha dedicado a desmontar la democracia en el país y a perseguir a la oposición.\nEl Estado se ha convertido en violador de los Derechos Humanos. Muchos inocentes han muerto bajo el control de elementos de la policía o del ejército, otros guardan prisión injustamente sin que existan pruebas contundentes en contra de ellos.\nEl país lleva ya más de dos años sometido a un injustificable régimen de excepción que vulnera derechos fundamentales, como el de defensa y la presunción de inocencia.\nLa Asamblea Legislativa en manos de Nuevas Ideas acaba de reformar un artículo de la Constitución (art. 248) que contiene una cláusula pétrea que, tal como su nombre lo indica, no puede ser objeto de reforma a menos que sea derogado por una Asamblea Constituyente.\nDe todo lo prometido lo único que se ha cumplido es la reducción de los niveles de delincuencia que el país enfrenta desde hace varias décadas.\nSin embargo, esta sensible disminución de los homicidios a manos de la pandillas no se debe a la aplicación de un efectivo plan de seguridad publica sino a una negociación con sus principales cabecillas, en la que se ha pactado un acuerdo de reducción de la violencia a cambio de beneficios procesales y económicos para los pandilleros.\nEn resumidas cuentas, a Bukele y su gobierno habrá que juzgarlos por sus acciones y decisiones y no tanto por sus promesas y anuncios demagógicos.\nComo dice la Biblia citando expresiones de Jesús a sus discípulos: “Por sus frutos los conoceréis”\n*El Colectivo Tetzáhuitl está integrado por un grupo de periodistas y analistas de la realidad nacional que se dedican a reflexionar sobre la situación política y económica del país. \nSus puntos de vista no están atados a ninguna ideología y mucho menos a intereses partidarios. \n \n\nRelacionado\n\n",
        "title": "Por sus frutos los conoceréis…",
        "sheet": None
    },
    {
        "url": "https://www.diariocolatino.com/category/nacionales/page/6283/",
        "date": "2024-05-06",
        "sheet_id": "https://www.diariocolatino.com/category/nacionales/page/6283/",
        "source": "diariocolatino.com",
        "tag": "Homicidio",
        "text": "\n@AlmaCoLatino El titular del Ministerio de Obras Públicas (MOP), rx Gerson Martínez, illness y representantes de la Agencia de Cooperación Internacional del Japón (JICA), dieron a conocer los avances del Proyecto GENSAI, que viene a fortalecer las capacidades para la mitigación de riesgos en el país. Martínez explicó que el programa GENSAI surgió en enero de 2012 ante la vulnerabilidad …\nLeer artículo completo \n",
        "title": "No se encontró el título",
        "sheet": None
    },
    {
        "url": "https://diario.elmundo.sv/nacionales/instalan-juicio-mujer-acusada-de-matar-a-su-hija-de-nueve-anos-en-apopa",
        "date": "2024-05-06",
        "sheet_id": "https://diario.elmundo.sv/nacionales/instalan-juicio-mujer-acusada-de-matar-a-su-hija-de-nueve-anos-en-apopa",
        "source": "diario.elmundo.sv",
        "tag": "Homicidio",
        "text": "\n        El Tribunal Segundo de Sentencia de San Salvador instaló este lunes el juicio en contra de Ester Leonor Pineda de Orellana por el delito de homicidio agravado en perjuicio de su hija, una niña de 9 años, un hecho ocurrido el 10 de enero del 2023. \rEster Leonor Pineda de Orellana, de 30 años, es procesada por el delito de homicidio agravado y por el delito de violación en menor e incapaz agravada, en su modalidad de omisión. \rPineda Orellana fue capturada el pasado 11 de enero señalada como la responsable de asesinar a su hija, de nueve años. \rEl hecho ocurrió el 10 de enero, según la información policial, en la colonia Popotlán I de Apopa, al norte de San Salvador . La Fiscalía aseguró que la niña presentaba múltiples lesiones con arma blanca, las cuales fueron propinadas por su madre. Incluso, el fiscal general, Rodolfo Delgado, aseguró que había indicios de maltrato infantil.\n                \n\n\n\n",
        "title": "Instalan juicio mujer acusada de matar a su hija de nueve años en Apopa",
        "sheet": None
    },
    {
        "url": "https://diario.elmundo.sv/opinion/regimen-de-excepcion-para-el-transporte-vehicular",
        "date": "2024-05-06",
        "sheet_id": "https://diario.elmundo.sv/opinion/regimen-de-excepcion-para-el-transporte-vehicular",
        "source": "diario.elmundo.sv",
        "tag": "Homicidio",
        "text": "\n        Nuestro país, El Salvador, presenta una de las tasas de mortalidad por homicidio más bajas del continente americano. El gobierno actual reporta mas de 600 días con cero homicidios. Un logro espectacular y que asombra a muchos países del mundo. Sin embargo, aunque las muertes por homicidio han disminuido, las muertes por accidentes de tráfico no. A diferencia de las muertes por homicidio, en lo que va del año, solamente durante tres días no se han reportado muertos por accidentes de tráfico, el resto de los días han ocurrido por lo menos tres muertes por día. El Salvador, después de Guatemala presenta la tasa de fatalidad por accidente de tráfico más alta de Centroamérica. \rUn accidente de tráfico se define como el fallo del sistema del conductor del vehículo de carretera para realizar una o más actividades necesarias para que el viaje se complete sin daños ni pérdidas. Los principales factores que contribuyen a los accidentes de tráfico son el mal estado de las carreteras, los adelantamientos imprudentes, la conducción somnolienta, el sonambulismo, la embriaguez, la enfermedad, el uso del teléfono móvil, comer y beber en el coche, la falta de atención en caso de accidente en la calle y la incapacidad de los demás conductores para reaccionar con suficiente rapidez ante la situación. \rSegún el Observatorio Nacional de Seguridad Vial de nuestro país -al cual aprovecho para felicitar por su magnífica página en línea, y por mantener su acceso al pueblo- las tres principales causas de siniestros viales en nuestro país son la distracción del conductor (35%), velocidad excesiva (28%), e invasión de carril (10%). La principal causa de accidente de tráfico y subsecuente mortalidad es estar ocupado mientras se conduce, lo que puede causar graves daños. \rEl manejo del móvil es una cuestión crucial para la seguridad de la conducción que requiere intervención. Por ejemplo, cuando las personas están ocupadas con sus teléfonos móviles mientras conducen, el riesgo de accidentes de tráfico aumenta unas cuatro veces más que el de quienes no utilizan sus teléfonos móviles mientras conducen. La razón es que el uso del móvil mientras se conduce perturba la reacción de la persona ante los frenos y las señales de tráfico y la incapacita para mantenerse en la línea y seguir la distancia adecuada. Lo que se prevé que aumente día a día es el riesgo de colisión con el uso del teléfono móvil. \rPor el otro lado, existe una relación directa entre las velocidades y la posibilidad de que se produzca un accidente, así como la gravedad de los sucesos; con un aumento del 1% de las velocidades medias aumenta la probabilidad de que se produzca un accidente mortal en un 4% y aumenta el riesgo de lesiones graves en un 3%. Además, el diseño de las carreteras tiene un impacto significativo en la seguridad vial. Esto abarca la seguridad de todos los usuarios de la carretera, por ejemplo, peatones, ciclistas y motociclistas. La gran mayoría de muertes por accidentes de tráfico en nuestro país se dan en peatones (42%) y en motociclistas (37%). O sea, de cada 10 personas que fallecen en un accidente de tráfico, ocho de ellas o iban caminando o montados en una moto. \rEs muy importante tener en cuenta la seguridad de todos los usuarios a la hora de diseñar las carreteras. Para reducir el riesgo de accidentes de los usuarios, son muy importantes las calles, los carriles bici, los cruces seguros y otras medidas de pacificación del tráfico. Otro factor de tomar en cuenta en nuestra seguridad vial es la edad del conductor. En los accidentes de tráfico por colisión y choque, el 77% y el 68%, respectivamente, la edad del conductor se encuentra entre los 19 y 40 años. Adicionalmente, el 85% de los muertos por atropello tienen más de 60 años. Geográficamente, 6 de cada 10 muertes por accidente de trafico ocurren en San Salvador (21%), La Libertad (16%), Sonsonate (12%), y Santa Ana (10%). \rLa Asamblea Legislativa aprobó en enero de 2023 una ley que aumenta significativamente las multas por infracciones de tráfico, incluyendo el uso de multas por tecnología como las cámaras de semáforos. Estas medidas de política publica al parecer carecen de un impacto significativo. ¿A lo mejor, un régimen de excepción?  • El Dr. Alfonso Rosales es médico epidemiólogo\n\n\n\n\n",
        "title": "¿Régimen de excepción para el transporte vehicular?",
        "sheet": None
    },
    {
        "url": "https://diario.elmundo.sv/nacionales/juicio-por-feminicidio-de-yancy-urbina-entra-en-receso-hasta-el-12-de-abril",
        "date": "2024-05-06",
        "sheet_id": "https://diario.elmundo.sv/nacionales/juicio-por-feminicidio-de-yancy-urbina-entra-en-receso-hasta-el-12-de-abril",
        "source": "diario.elmundo.sv",
        "tag": "Feminicidio",
        "text": "\n        El Juzgado Especializado de Sentencia para una Vida Libre de Violencia y Discriminación, de San Salvador recesó este jueves el juicio en contra Peter Wachowski, acusado del feminicidio de su exesposa, Yanci Urbina, la exdiputada del FMLN. \rLa vista pública fue instalada el pasado miércoles 3 de abril en una de las salas del Centro Judicial \"Isidro Menéndez\", sin embargo, la jornada de este jueves se desarrolló en las salas de audiencia del edificio del Centro Integrado de Segunda Instancia de San Salvador, donde el acceso a la prensa es limitado, y será reanudado el próximo 12 de abril. \rDurante el juicio se espera recibir la declaración de 26 testigos tanto de cargo como de descargo, hasta este jueves habían pasado 11 testigos, entre ellos, peritos, investigadores. \rEs de mencionar que la audiencia estaba programada para un día, pero debido a la declaración de testigos se alargó. \rLa defensa sostiene que espera obtener una sentencia absolutoria, debido a que la Fiscalía no cuenta con los elementos de prueba para sostener la acusación contra Wachowski. \rLa exdiputada Yanci Urbina murió el pasado 29 de mayo del 2022, en su casa de habitación, en Antiguo Cuscatlán, departamento de La Libertad, aparentemente en un accidente, luego de una caída que posteriormente le habría provocado un paro cardíaco. \rDe igual forma, sostiene que la muerte de la exdiputada se trató de un acto de violencia de género y no de un accidente por una caída. \rEn el transcurso del proceso, la Fiscalía ha manifestado que el cuerpo de Urbina tenía múltiples moretones, un golpe con objeto contundente y el tabique nasal quebrado.\n                \n\n\n\n",
        "title": "Juicio por feminicidio de Yancy Urbina entra en receso hasta el 12 de abril",
        "sheet": None
    },
    {
        "url": "https://diario.elmundo.sv/nacionales/al-menos-26-testigos-declaran-en-el-juicio-por-caso-del-feminicidio-de-yanci-urbina",
        "date": "2024-05-06",
        "sheet_id": "https://diario.elmundo.sv/nacionales/al-menos-26-testigos-declaran-en-el-juicio-por-caso-del-feminicidio-de-yanci-urbina",
        "source": "diario.elmundo.sv",
        "tag": "Feminicidio",
        "text": "\n        Unos 26 testigos de cargo y descargo declararán en el juicio en contra del ciudadano de origen alemán, Peter Wachowski, quien es acusado del feminicidio de su exesposa, Yanci Urbina, la exdiputada del FMLN. \rEl abogado defensor, Óscar Argueta, confirmó a Diario El Mundo que serán 26 testigos, entre ellos, peritos, investigadores, que declararán sobre los hechos del 29 de mayo del 2022. \rLa vista pública estaba programada para desarrollarse un día, sin embargo, por el número de testigos el defensor aseguró que se podría extender. Hasta la tarde de este miércoles, el juicio seguía. \rSobre quiénes son los testigos, el defensor no entró en detalles, debido a la reserva total del caso. \r\"Obviamente la defensa, salir adelante con un fallo absolutorio...animado ahorita (Peter Wachowski)\", aseguró el abogado defensor en referencia a su cliente. \rEl principal acusado, el exesposo de la víctima, este se mantiene en detención desde el 14 de junio del 2022.\r¿Cuando murió la exdiputada?\rLa exdiputada Yanci Urbina murió el pasado 29 de mayo del 2022, en su casa de habitación, en Antiguo Cuscatlán, departamento de La Libertad, aparentemente en un accidente, luego de una caída que posteriormente le habría provocado un paro cardíaco. \rSegún la investigación de la Fiscalía, existe evidencia que el entonces esposo de la exdiputada, Yanci Urbina, la habría golpeado y esto la llevó a un paro cardíaco, que le causó la muerte. \rDe igual forma, sostiene que la muerte de la exdiputada se trató de un acto de violencia de género y no de un accidente por una caída. \rEn el transcurso del proceso, la Fiscalía ha manifestado que el cuerpo de Urbina tenía múltiples moretones, un golpe con objeto contundente y el tabique nasal quebrado.\n                \n\n\n\n",
        "title": "Al menos 26 testigos declaran en el juicio por caso del feminicidio de Yanci Urbina",
        "sheet": None
    },
    {
        "url": "https://diario.elmundo.sv/el-mundo/presos-sin-sentencia-votan-por-primera-vez-para-presidente-en-mexico",
        "date": "2024-05-06",
        "sheet_id": "https://diario.elmundo.sv/el-mundo/presos-sin-sentencia-votan-por-primera-vez-para-presidente-en-mexico",
        "source": "diario.elmundo.sv",
        "tag": "Homicidio",
        "text": "\n        \"Que cumplan lo que nos prometen, ¿no?\", pidió este lunes a los candidatos un joven tras votar por primera vez para elegir presidente en una prisión de México. El joven es uno de los más de 30.000 presos sin sentencia que, por primera vez, pueden votar en el país. \rEl proceso entre aquellos que cumplen prisión preventiva, que arrancó este lunes y se cerrará el 20 de mayo, marca un hito en esta campaña ya de por sí histórica, ya que los sondeos indican que por primera vez una mujer ganará las presidenciales, que se celebran el 2 de junio. \rEl recluso, de 24 años y cuya identidad no puede ser revelada debido a su situación legal, no solo votó para presidente. También lo hizo para alcalde de Ciudad de México, diputados federales y locales, y hasta para la alcaldía del distrito donde se ubica la cárcel. \r\"Nos trajeron las pláticas, vimos los debates y con eso nos pudimos apoyar para poder votar\", relató a la prensa el interno, cuya principal demanda a los aspirantes presidenciales es \"un poco más de consideración\" para los privados de libertad. \rEn el Reclusorio Varonil Norte, donde está detenido, 354 de los 1.862 internos están llamados a las urnas después de que el Tribunal Electoral del Poder Judicial de la Federación determinara en febrero de 2019 que los presos sin sentencia tienen derecho a votar. \r\"Son personas que se encuentran en prisión preventiva, es decir, no tienen una sentencia y por tanto tienen los derechos político-electorales vigentes\", explicó a periodistas María Luisa Flores, presidenta del Consejo Local del Instituto Nacional Electoral (INE) de Ciudad de México. \r\"Es una mañana histórica realmente (...) para todo el país\", añadió la funcionaria sobre las jornadas de votación, programadas en 282 cárceles de México.  \n\n\n\n\n\nLa población carcelaria del centro de detención de Puente Grande, Jalisco, hace fila para emitir el sufragio. / AFP\n\n Entusiasmo \rDe una población de 232,684 internos, 31.121 -el 13,3%- cumplieron con los requisitos que estableció el INE para participar de la votación, según el gobierno. \rEn el Reclusorio Norte, el sufragio arrancó a las nueve de la mañana en un ambiente de entusiasmo. \rEl auditorio de la cárcel, cuyo techo estaba adornado por una enorme y multicolor escarapela de papel seda, recibió a los 171 primeros votantes que ingresaron y se sentaron ordenadamente a esperar su turno. \rSobre el escenario, una docena de funcionarios electorales instalaron siete cabinas de votación colocadas simétricamente y a distancia prudente para que nadie pueda husmear y violar el secreto del voto. \r\"Estamos reconociendo el derecho que tienen ustedes de poder elegir\", dijo Flores, palabras respondidas por los internos con aplausos.  \n\n\n\n\n\nAFP\n\n ¿Excarcelación masiva? \rLos primeros siete votantes subieron al escenario y ocuparon las cabinas en las que se leía: \"El voto es libre y secreto\". \rPasaron unos cinco minutos antes de que el primero terminara de votar y bajara del escenario al espacio habilitado para depositar su boleta en el ánfora y recibir la marca de tinta indeleble en el dedo, que certifica su participación. Luego, la votación se hizo más ágil. \rLos votos de los reclusos se mantendrán cerrados hasta el final de la votación del 2 de junio, cuando se sumarán al resto de las boletas para realizar el computo general, informó Flores. \rEl voto de los presos se da después de que en abril pasado el gobierno del presidente Andrés Manuel López Obrador alertara que la Suprema Corte se propone eliminar la figura de la prisión preventiva oficiosa. \rEsa medida, advierte el gobierno, dejaría libres a unos 68.000 presuntos delincuentes acusados de delitos como homicidio, secuestro, violación y narcotráfico.\n                \n\n\n\n",
        "title": "Presos sin sentencia votan por primera vez para presidente en México",
        "sheet": None
    },
    {
        "url": "https://diarioelsalvador.com/desde-este-jueves-se-pueden-comprar-los-boletos-para-el-encuentro-de-leyendas/501724/",
        "date": "2024-05-09",
        "sheet_id": "https://diarioelsalvador.com/desde-este-jueves-se-pueden-comprar-los-boletos-para-el-encuentro-de-leyendas/501724/",
        "source": "diarioelsalvador.com",
        "tag": "Homicidio",
        "text": "El Banco Cuscatlán, patrocinador del juego solidario denominado «A la cancha por una sonrisa», anunció este miércoles que desde este jueves estarán disponibles en Fun Capital los boletos para el partido benéfico que reunirá, en el estadio Mágico González el 18 de junio a las 7:00 p. m., a exestrellas de talla mundial como Javier Zanetti, David Trezeguet, Carlos Valderrama, Cafú y a leyendas salvadoreñas como Jorge González. La institución financiera informó que los exfutbolistas Manuel Salazar, Ramiro Carballo, Memo Rivera, Cárcamo Batres, Papo Castro Borja, entre otros, serán los rivales de esa constelación que es liderada por Zanetti, promotor de la Fundación PUPI. «Estoy feliz, sobre todo, porque El Salvador nos abre las puertas para hacer el partido A la cancha por una sonrisa de mi fundación a la que muchos jugadores dijeron presente, así que será una gran fiesta», dijo el Pupi Zanetti en una videollamada realizada durante la conferencia organizada por el Banco Cuscatlán. Sin revelar el precio de los boletos de ese partido, Isabel Giamattei, gerente de mercadeo y estrategia del banco, dijo que es un honor hacer posible este tipo de eventos, al tiempo que se informó que desde hoy y durante los próximos cinco días, habrá una venta exclusiva para clientes del Cuscatlán que paguen con su tarjeta de crédito o débito, además de contar con la facilidad de pagar hasta en 12 cuotas.",
        "title": "Desde este jueves se pueden comprar los boletos para el «Encuentro de leyendas»",
        "sheet": None
    },
    {
        "url": "https://diarioelsalvador.com/nayib-bukele-afirma-que-faes-lograra-su-victoria-mas-grande/501945/",
        "date": "2024-05-09",
        "sheet_id": "https://diarioelsalvador.com/nayib-bukele-afirma-que-faes-lograra-su-victoria-mas-grande/501945/",
        "source": "diarioelsalvador.com",
        "tag": "Homicidio",
        "text": "El presidente de la república, Nayib Bukele, compartió un video en el que se destacan los 200 años de vida y la labor que desarrolla la Fuerza Armada de El Salvador (FAES) por resguardar la paz, la soberanía nacional y el bienestar que ahora tienen los salvadoreños, con sus acciones enmarcadas dentro del Plan Control Territorial (PCT) y apoyo al régimen de excepción. «Nuestra Fuerza Armada cumple 200 años y está a punto de lograr su victoria más grande», escribió el mandatario en X, con el video que hace un repaso a los dos siglos de vida de la institución castrense. En el audiovisual, que tiene una duración de un minuto con 31 segundos, se define a la Fuerza Armada como una institución «gloriosa, moderna y profesional» como producto de los cambios que ha tenido en su gestión. «Hoy el mundo es testigo del servicio que estos hombres y mujeres valientes han brindado», se indica en el video, que muestra a los militares en distintas tareas realizadas en beneficio de la población. «Después de enfrentar y vencer a miles de terroristas, El Salvador se ha transformado en el país más seguro del hemisferio occidental», se destaca. La Fuerza Armada es la institución del Estado que recibe la más alta nota por parte de los salvadoreños a dos años de vigencia del régimen de excepción, según la más reciente encuesta del Instituto Universitario de Opinión Pública (Iudop), de la Universidad Centroamericana José Simeón Cañas (UCA). Los salvadoreños dan en la encuesta —realizada en marzo pasado a escala nacional— una nota de 8.1 al trabajo de la FAES en el marco del estado de excepción, que ha permitido una reducción drástica de homicidios, la captura de más de 80,000 pandilleros y la recuperación de territorios en poder de las pandillas. Durante la administración del presidente Bukele se ha dignificado al personal militar dotándolo de moderno equipo para combatir el crimen, con instalaciones dignas, atención sanitaria moderna, salario justo y la entrega de un bono por su trabajo.",
        "title": "Nayib Bukele afirma que FAES logrará su victoria más grande",
        "sheet": None
    },
    {
        "url": "https://diarioelsalvador.com/miss-teen-y-miss-usa-renuncian-a-su-titulo-para-cuidar-de-su-salud-mental/501730/",
        "date": "2024-05-09",
        "sheet_id": "https://diarioelsalvador.com/miss-teen-y-miss-usa-renuncian-a-su-titulo-para-cuidar-de-su-salud-mental/501730/",
        "source": "diarioelsalvador.com",
        "tag": "Homicidio",
        "text": "Usuarios en redes sociales reaccionaron ante la decisión de UmaSofia Srivastava, Miss Teen USA, luego renunciar a su título, al igual que lo hizo la modelo Noelia Voigt, dimitir a su corona como Miss USA.«Valores personales ya no se alinean completamente con la dirección de la organización», expresó UmaSofia Srivastava, quien añadió:«Después de meses de aferrarme a esta decisión, tomé la decisión de renunciar al título de Miss Teen USA. Estoy agradecida por todos los que me animaron desde que gané mi título estatal. Siempre recordaré con cariño mi época como Miss NJ Teen USA, y la experiencia de representar a mi estado como mexicano-indio americano de primera generación a nivel nacional fue gratificante en sí misma». La joven de Nueva Jersey también reiteró lo importante de «priorizar su salud» y confesó que «después de una cuidadosa consideración, decidí renunciar porque descubrí que mis valores personales ya no se alinean completamente con la dirección de la organización. Sin embargo, continuaré mi incansable defensa de la educación y la aceptación con mi libro infantil multilingüe The White Jaguar y con las organizaciones con las que he tenido el privilegio de trabajar». Cabe mencionar que la renuncia de UmaSofia Srivastava, ha sido oficial casi dos días después de que la modelo Noelia Voigt dejará su título como Miss USA, quien también explicó que la decisión tiene como objetivo priorizar su salud mental. A post shared by Noelia Voigt (@noeliavoigt) «En el fondo sé que este es solo el comienzo de un nuevo capítulo para mí, y mi esperanza es seguir inspirando a otros a permanecer firmes, priorizar su salud mental, defenderse a sí mismos y a los demás usando su voz, y nunca tener miedo de lo que depara el futuro, incluso si se siente incierto», publicó en sus redes sociales.",
        "title": "Miss Teen y Miss USA renuncian a su título para cuidar de su «salud mental»",
        "sheet": None
    },
    {
        "url": "https://diarioelsalvador.com/condenan-a-hombres-que-mataron-a-pedradas-a-victima-en-san-salvador/501844/",
        "date": "2024-05-09",
        "sheet_id": "https://diarioelsalvador.com/condenan-a-hombres-que-mataron-a-pedradas-a-victima-en-san-salvador/501844/",
        "source": "diarioelsalvador.com",
        "tag": "Homicidio",
        "text": "El Tribunal Sexto de Sentencia de San Salvador condenó a 30 años de prisión a Víctor Manuel Medrano y a William Ernesto Matute Pérez, por el delito de homicidio agravado en perjuicio de Adonay Enrique Carrillo Vásquez. Un testigo protegido, que presenció el hecho, declaró que, el 18 de julio de 2021 a las 9:40 de la mañana,Víctor fue quien sujetó de los brazos a la víctima por detrás, mientras que William le causaba una serie de lesiones con arma blanca, se consigna en el reporte oficial de la Fiscalía. Luego vio que la víctima cayó al suelo y los sujetos lo golpearon en la cabeza, cada uno, con una piedra. La víctima quedó tendida sobre el adoquinado de la calle San Juan, entre 26 y 28 Avenida Norte de San Salvador, y los sujetos se marcharon del lugar como si nada hubieran hecho.",
        "title": "Condenan a hombres que mataron a pedradas a víctima en San Salvador",
        "sheet": None
    },
    {
        "url": "https://diarioelsalvador.com/hospital-de-sonsonate-desarrolla-jornada-de-cirugias-pediatricas/501836/",
        "date": "2024-05-09",
        "sheet_id": "https://diarioelsalvador.com/hospital-de-sonsonate-desarrolla-jornada-de-cirugias-pediatricas/501836/",
        "source": "diarioelsalvador.com",
        "tag": "Homicidio",
        "text": "Niños entre los cuatros meses y 11 años fueron beneficiados con una jornada de cirugías en el Hospital Nacional de Sonsonate, así lo detalló el ministro de Salud, Francisco Alabi, quien destacó la articulación del trabajo del personal médico. «Todo el equipo interdisciplinario que está participando tiene como objetivo garantizar el bienestar de los hijos de los salvadoreños», indicó el titular del Ministerio de Salud. Entre los padecimientos abordados con las cirugías están: hernia inguinal bilateral, colelitiasis, varicoceles, entre otros, los cuales fueron resueltos con las cirugías. Alabi señaló que a la jornada se sumó el personal de diferentes hospitales para beneficiar a los niños que se sometieron a las cirugías. Agradeció la disposición para contribuir a la mejorar la calidad de vida de los pacientes. «Agradezco a todo el personal de los hospitales de San Bartolo, Cojutepeque y Bloom por sumarse a esta jornada y hacer posible el éxito en cada intervención», subrayó Alabi. A través de estas jornadas, el Minsal continúa reduciendo la mora quirúrgica heredada de décadas en el sistema de salud. El equipamiento de los hospitales nacionales permite desarrollar procedimientos de mínima invasión que benefician a las personas, quienes se recuperan en menor tiempo. La semana pasada, el ministro Alabi también informó sobre otra jornada de cirugías que se ejecutó en el Hospital Nacional Rosales; mediante estas intervenciones, se benefició a 20 pacientes. «Un total de 20 pacientes fueron intervenidos exitosamente por un equipo multidisciplinario y comprometido con la población. ¡Continuaremos realizando más jornadas en todos los hospitales públicos del país!», dijo Alabi. ",
        "title": "Hospital de Sonsonate desarrolla jornada de cirugías pediátricas",
        "sheet": None
    },
    {
        "url": "https://diarioelsalvador.com/encuentran-nueve-cadaveres-en-region-mexicana-azotada-por-escalada-de-violencia/501705/",
        "date": "2024-05-09",
        "sheet_id": "https://diarioelsalvador.com/encuentran-nueve-cadaveres-en-region-mexicana-azotada-por-escalada-de-violencia/501705/",
        "source": "diarioelsalvador.com",
        "tag": "Homicidio",
        "text": "Nueve cadáveres fueron encontrados este miércoles en la mexicana ciudad de Morelos, del estado norteño de Zacatecas, un día después de que otros nueve cuerpos fueran hallados sobre una avenida de Fresnillo, de la misma demarcación, informaron autoridades. Zacatecas enfrenta un aumento de hechos violentos tras la reciente captura de criminales, de acuerdo con autoridades. «Se atendió el reporte del hallazgo de nueve cuerpos sin vida, mismos que corresponden a personas del sexo masculino», informó la fiscalía de Zacatecas en un breve comunicado sin dar más detalles. Y «en relación a los eventos registrados el día 7 de mayo, en el municipio de Fresnillo (…) se informa que han sido identificados 5 víctimas, mismas que ya fueron entregados a sus familiares», concluyó el comunicado. Junto a estos últimos cuerpos se encontraron «mensajes dirigidos a un grupo antagónico», dijo por su parte el secretario de gobierno del estado de Zacatecas, Rodrigo Reyes.  Fueron arrojados cerca de un mercado dos días después de que grupos criminales bloquearan carreteras y quemaran vehículos de carga en respuesta a la captura de 13 presuntos delincuentes en Fresnillo. El país acumula unos 450.000 homicidios y más de 100.000 desaparecidos desde que en 2006 el Estado lanzó una ofensiva antidrogas con participación militar. La inseguridad es uno de los ejes de la campaña para las elecciones presidenciales del próximo 2 de junio, cuya intención de voto lidera cómodamente la oficialista de izquierda Claudia Sheinbaum, por encima de la opositora de centroderecha Xóchitl Gálvez y de Jorge Álvarez Máynez (centroizquierda), según encuestas. Sheinbaum ofrece dar continuidad al enfoque del mandatario Andrés Manuel López Obrador, que según él privilegia atender las causas de la violencia, como la pobreza y la exclusión, antes que la guerra frontal contra los cárteles. Por el contrario, Gálvez promete capturar a los grandes capos y de este modo poner fin a la estrategia de «abrazos, no balazos», como López Obrador bautizó su política de seguridad.",
        "title": "Encuentran nueve cadáveres en región mexicana azotada por escalada de violencia",
        "sheet": None
    },
    {
        "url": "https://diarioelsalvador.com/arrestan-a-hombre-que-intento-asesinar-a-machetazos-a-su-pareja/501977/",
        "date": "2024-05-10",
        "sheet_id": "https://diarioelsalvador.com/arrestan-a-hombre-que-intento-asesinar-a-machetazos-a-su-pareja/501977/",
        "source": "diarioelsalvador.com",
        "tag": "Feminicidio",
        "text": "Este jueves, las autoridades reportaron la captura de Pio Antonio González, de 67 años de edad, quien según explicaron, trató de quitarle la vida a su pareja utilizando un corvo. La Policía Nacional Civil (PNC) detalló que la mujer, quien no fue identificada, sufrió lesiones y fue trasladada hasta el Hospital Regional San Juan de Dios, en San Miguel. «La víctima fue trasladada al Hospital Regional San Juan de Dios, con heridas graves en la cabeza, mandíbula y brazos», escribió la PNC en su cuenta de X. #DePaís La @PNCSV capturó a Pio Antonio González, de 67 años, por intento de feminicidio, en el caserío El Rebalse, de San Miguel. Según informó la Policía, este sujeto intentó asesinar a machetazos a su compañera de vida. La víctima fue trasladada al Hospital Regional San Juan… pic.twitter.com/yyjBbnYArU En hombre fue ubicado y capturado por agentes policiales en el caserío El Rebalse, de San Miguel, tras cometer las agresiones contra su compañera de vida.   Las autoridades indicaron que Gonzáles será procesado por intento de feminicidio.",
        "title": "Arrestan a hombre que intentó asesinar a machetazos a su pareja",
        "sheet": {
            "indicators": [
                {
                    "indicator_name": "Clasificacion",
                    "response": "No, la noticia no describe un homicidio. La noticia describe un intento de feminicidio, no un homicidio."
                },
                {
                    "indicator_name": "Titulo",
                    "response": "*Título:* Arrestan a hombre que intento asesinar a machetazos a su pareja\n\nLa información extraída es correcta."
                },
                {
                    "indicator_name": "Resumen",
                    "response": "*Resumen:*\n\nLa noticia informa sobre el arresto de Pio Antonio González, de 67 años, por intento de feminicidio en San Miguel. La víctima, aún no identificada, sufriuó lesiones graves en la cabeza, la mandíbula y los brazos. La policía capturó a González en el caserío El Rebalse. Las autoridades indicaron que Gonzáles será procesado por intento de feminicidio."
                },
                {
                    "indicator_name": "Ubicacion del Suceso",
                    "response": "*Dónde ocurrió el suceso:*\n\nLa noticia indica que el suceso ocurrió en el caserío El Rebalse, de San Miguel."
                },
                {
                    "indicator_name": "Fuentes",
                    "response": "*Cita de fuentes de información:*\n\nLa noticia no indica fuentes de información, por lo que no se puede proporcionar la cita de fuentes de información."
                },
                {
                    "indicator_name": "Temas",
                    "response": "*Los temas principales tratados en la noticia:\n\n *Intento de feminicidio:* La noticia describe un intento de feminicidio ocurrido en San Miguel, en el que un hombre de 67 años llamado Pio Antonio González intentó quitarle la vida a su pareja con un corvo.\n* *Seguridad de las mujeres:* La noticia enfatiza la importancia de la protección de las mujeres y su seguridad, y cómo este caso ilustra la necesidad de tomar medidas para prevenir la violencia contra las mujeres.\n* *Legality:* La noticia menciona el procesamiento de González por intento de feminicidio, enfatizando la necesidad de garantizar la justicia y la protección de las víctimas de violencia."
                },
                {
                    "indicator_name": "Hechos Violativos",
                    "response": "La noticia no contiene información sobre la violación a la ley, por lo que no se puede proporcionar la información solicitada."
                },
                {
                    "indicator_name": "Hipotesis de los Hechos",
                    "response": "*Teoría:\n\nLa noticia reporta el asesinato de una mujer por parte de su pareja, utilizando un corvo como arma. La teoría de la situación es que el hombre, de 67 años, probablemente experimentó un problema de salud mental y en un estado emocional impulsivo, ejecutó el crimen.\n\nSuposición:*\n\nLa suposición de la noticia es que el hombre, de 67 años, es responsable de las lesiones sufrididas por su pareja. Es probable que el hombre haya actuado impulsivamente debido a una condición mental o una reacción violenta a una situación percibida."
                },
                {
                    "indicator_name": "Poblacion Vulnerable",
                    "response": "La noticia no contiene información sobre los grupos en riesgo, por lo que no se puede proporcionar la información solicitado."
                },
                {
                    "indicator_name": "Tipo de Arma",
                    "response": "La noticia indica que la arma utilizada en el intento de feminicidio fue una macheta."
                },
                {
                    "indicator_name": "Victimas",
                    "response": "La noticia no identifica a la víctima, por lo que no se puede proporcionar la información de su identificación."
                },
                {
                    "indicator_name": "Agresor o Sospechoso",
                    "response": "El texto indica que el nombre del agresor es Pio Antonio González, pero no se menciona el nombre de la víctima.\n\nPor lo tanto, la información que se puede proporcionar es:\n\n*Nombre del agresor:* Pio Antonio González\n\n*No se indica el nombre de la víctima.*"
                }
            ],
            "priority": 3,
            "id": "https://diarioelsalvador.com/arrestan-a-hombre-que-intento-asesinar-a-machetazos-a-su-pareja/501977/"
        }
    },
    {
        "url": "https://diarioelsalvador.com/enjuiciaran-a-hombre-por-trasladar-cadaver-de-joven-asesinada-en-ciudad-delgado/501519/",
        "date": "2024-05-10",
        "sheet_id": "https://diarioelsalvador.com/enjuiciaran-a-hombre-por-trasladar-cadaver-de-joven-asesinada-en-ciudad-delgado/501519/",
        "source": "diarioelsalvador.com",
        "tag": "Feminicidio",
        "text": "En noviembre de 2017, una joven de 20 años con tres meses de embarazado fue asesinada en Ciudad Delgado, los responsables del crimen no fueron identificados, solo Antonio Galdámez, de 60 años de edad, quien supuestamente ayudó a trasladar el cadáver para luego lanzarlo en una calle. Por ese hecho, el Juzgado Especializado Primero de Instrucción para una Vida Libre de Violencia y Discriminación para las Mujeres, de San Salvador, lo envió a juicio por complicidad en el delito de feminicidio agravado. El caso comenzó a ser investigado por la Fiscalía General de la República tras el hallazgo del cuerpo de la joven el 5 de noviembre de 2017, en la calle principal de la colonia Guadalcanal, en el municipio de Ciudad Delgado. En la audiencia preliminar el ministerio público presentó el dictamen de la autopsia que efectuó el Instituto de Medicina Legal en el cual se establece que la causa de la muerte fue por múltiples lesiones con arma blanca y golpes en el cuerpo. A los responsables del crimen no los han identificado hasta la fecha, la Fiscalía solo logró obtener información de que Galdámez llegó a una vivienda donde lo esperaban dos sujetos, luego salieron del inmueble con un bulto y lo subieron a la cama de un pick-up de su propiedad el cual ocupaba para transportar sillas y mesas que alquilaba. Según el informe fiscal, Galdámez, condujo el automotor hasta la calle principal de la colonia Guadalcanal, donde lanzó el cadáver.",
        "title": "Enjuiciarán a hombre por trasladar cadáver de joven asesinada en Ciudad Delgado",
        "sheet": None
    },
    {
        "url": "https://diario.elmundo.sv/nacionales/suspenden-audiencia-por-resistencia-contra-presunto-asesino-de-nina-en-la-campanera",
        "date": "2024-05-08",
        "sheet_id": "https://diario.elmundo.sv/nacionales/suspenden-audiencia-por-resistencia-contra-presunto-asesino-de-nina-en-la-campanera",
        "source": "diario.elmundo.sv",
        "tag": "Feminicidio",
        "text": "\n        El Juzgado Segundo de Instrucción de San Salvador suspendió este miércoles la audiencia preliminar por el delito de resistencia en contra de Edwin Mauricio Alvarado Lazo, capturado en octubre del 2023 como el presunto responsable del homicidio de una niña de siete años en La Campanera, en Soyapango. \rLa audiencia por el delito de resistencia estaba programada para las 11:00 de la mañana, sin embargo, se suspendió porque el equipo tecnológico de la Corte Suprema de Justicia no logró establecer conexión virtual con el centro penal donde está detenido el imputado supuestamente porque el penal tenía programada la audiencia para otro día. El juzgado programó la audiencia para el próximo 22 de julio, a las 9:30 de la mañana. \rEs de mencionar, que Mauricio Alvarado Lazo fue acusado por la Fiscalía General de la República inicialmente por resistencia el 24 de octubre, por hechos sucedidos el pasado 11 de octubre, a las 3:00 de la tarde sobre el bulevar Tutunichapa, entre la Avenida España y Avenida Avenida Monseñor Óscar Arnulfo Romero, en San Salvador. \rLa detención habría derivado cuando los agentes de la Policía Nacional Civil se percataron del nerviosismo del imputado, fue cuando le realizaron los altos, pero este habría hecho caso omiso al llamado, y al realizar la detención este se habría opuesto ultrajando y diciéndoles palabras soeces.\r Feminicidio, violación y privación de libertad\rEl 27 de octubre la Fiscalía presentó formalmente la acusación contra Edwin Mauricio Alvarado Lazo por los delitos de feminicidio agravado, violación y privación de libertad, como el único responsable del asesinato de Diana Melissa C.H, de siete años, en el reparto La Campanera, en Soyapango. \rLa acusación, supuestamente esta sustentado con la confesión del sujeto sobre el asesinato de la menor, así mismo, de inspecciones en diferentes lugares donde la menor habría pasado las últimas horas de su vida, donde encontraron cuerdas, y los mismo tipos de nudos que el acusado usaba en su vivienda. \rLa Fiscalía también ha sostenido qué hay evidencia científica para sustentar las acusaciones, como una pericia o examen médico de Medicina Legal, sobre indicios de abuso sexual. \r\"Él de ser un vecino del lugar y ser un posible testigo de los hechos, se convierte en nuestro principal sospechoso y posteriormente, en presencia de un defensor, la presencia de los fiscales, de los investigadores, el sujeto se quiebra y decide confesar los hechos, la persona confesó que fue él el causante de la muerte de Melissa”, confirmó el fiscal general, Rodolfo Delgado, el pasado miércoles 25 de octubre.  Diana Melissa.C.H., quien fue asesinada en el reparto La Campanera, en el municipio de Soyapango, cuyo cuerpo fue encontrado el pasado martes 10 de octubre en un saco, en una zona verde de la misma colonia. El presunto responsable vivía a unos 90 metros de distancia de la casa donde vivía la menor. \rEl director de la Policía Nacional Civil, Mauricio Arriaza, aseguró, cuando lo presentaron públicamente, que Alvarado privó de libertad a la víctima, entre las 5:30 de la tarde y las 7:00 de la noche, la condujo a su vivienda, la número 34, donde habría cometido el hecho. Arriaza aseguró que cuando la madre de la menor avisó de la desaparición, los vecinos se organizaron para la búsqueda, y que cuando se le pidió ayuda al capturado “él estaba en toalla”.\n\n\n\n\n",
        "title": "Suspenden audiencia por resistencia contra presunto asesino de niña en La Campanera",
        "sheet": None
    },
    {
        "url": "https://diario.elmundo.sv/author/2445/iliana-cornejo-con-reportes-de-juan-carlos-vsquez",
        "date": "No se pudo encontrar una fecha válida en el formato proporcionado.",
        "sheet_id": "https://diario.elmundo.sv/author/2445/iliana-cornejo-con-reportes-de-juan-carlos-vsquez",
        "source": "diario.elmundo.sv",
        "tag": "Feminicidio",
        "text": "No se encontró el texto del articulo",
        "title": "No se encontró el título",
        "sheet": None
    }
]
@router.get("/news-sheet-filter/")
def read_all_saved(search_word: str = None, filters_sheet: SheetEntry = None, date_start: str = None,
                   date_end: str = None):
    if filters_sheet is not None:
        filters_sheet = filters_sheet.dict()
    date_regex = r"^.{4}-.{2}-.{2}$"
    #list_saved_news = get_news_sheets()
    list_saved_news = mocked_sheet
    if search_word is not None:
        list_saved_news = [news for news in list_saved_news if search_word in news["text"]]
    if filters_sheet is not None:
        filtered_news = []
        for new in list_saved_news:
            if new["sheet"] is not None:
                for index, indicator in enumerate(new["sheet"]["indicators"]):
                    search = filters_sheet["indicators"][index]["response"]
                    if search != "" and search in indicator["response"]:
                        filtered_news.append(new)
        list_saved_news = filtered_news
    date_start_obj = datetime.strptime(date_start, '%Y-%m-%d').date() if date_start else None
    date_end_obj = datetime.strptime(date_end, '%Y-%m-%d').date() if date_end else None
    if date_start is not None and date_end is None:
        list_saved_news = [news for news in list_saved_news if
                           re.match(date_regex, news["date"]) and datetime.strptime(news["date"], '%Y-%m-%d').date() >= date_start_obj]
    if date_end is not None and date_start is None:
        list_saved_news = [news for news in list_saved_news if
                           re.match(date_regex, news["date"]) and datetime.strptime(news["date"], '%Y-%m-%d').date() <= date_end_obj]
    if date_end is not None and date_start is not None:
        list_saved_news = [news for news in list_saved_news if
                           re.match(date_regex, news["date"]) and
                           datetime.strptime(news["date"], '%Y-%m-%d').date() >= date_start_obj and datetime.strptime(
                               news["date"], '%Y-%m-%d').date() <= date_end_obj]

    return list_saved_news


@router.get("/news/{new_id}")
def read(new_id: str):
    new = get_new_by_id(new_id)
    if new is not None:
        return new
    raise HTTPException(status_code=404, detail="new not found")


@router.put("/news/{new_id}")
def update(new_id: str, new: New):
    update_new(new_id, new)
    return {"message": "new updated successfully."}


@router.delete("/news/{new_id}")
def delete(new_id: str):
    delete_new(new_id)
    return {"message": "new deleted successfully."}

import random

#Elige una tematica dada una lista de diccionarios
def elegir_tematica(lista:list):
    try:
        nombre_tematica = []
        
        for item in lista:
            nombre_tematica.append(item["tematica"])

        #Se podria haber usado un map y un lambda
        nombre_tematica = list(set(nombre_tematica))
        largo_lista = len(nombre_tematica) -1
        tematica = nombre_tematica[random.randint(0,largo_lista)]
        return tematica
    except IndexError as e:
        print(f"La lista esta vacia: {e}")

#Elige una pregunta dada una tematica, usa una lista de diccionarios
def elegir_pregunta(lista: list, tematica: str):
    try:
        lista_preguntas = []
        for item in lista:
            if item["tematica"] == tematica:
                lista_preguntas.append(item) # Agrega diccionarios
        
        largo_lista = len(lista_preguntas) -1
        pregunta = lista_preguntas[random.randint(0,largo_lista)]

        return pregunta
    except IndexError as e:
        print(f"La lista esta vacia: {e}")

#Dada una respuesta, busca en que index del diccionario se encuentra
def encontrarRespuesta(pregunta:dict, respuesta:str):
    try:
        for key, value in pregunta.items():
            if value == respuesta:
                #Devuelve el nombre del index
                return str(key)
    except IndexError as e:
        print(f"La lista esta vacia: {e}")

#Dada una respuesta, compara con todas las respuestas para saber si fue correcta.
#Si lo fue, retorna los puntos.
def comparar_respuesta(pregunta:dict, respuesta:str, respuestasRepetidas:list):
    puntos = 0
    for item in respuestasRepetidas:
        if respuesta == item:
            return puntos
    for i in range (1, len(pregunta)-1):
        if pregunta[f"Respuesta_{i}"] == respuesta:
            puntos = pregunta[f"Cantidad_R{i}"]
            return puntos
    
    return puntos

#Se busca la respuesta con menos puntos que no haya sido mostrada
def elegir_minimo(pregunta:dict, respuestasRepetidas:list):
    respuestasTotales = []
    puntosTotales = []

    #Toman todas las respuestas
    for i in range (5):
        respuestasTotales.append(pregunta["Respuesta_" + str(i + 1)])
    
    #Quitan las repetidas
    for respuesta in respuestasRepetidas:
        respuestasTotales.remove(respuesta)

    #Obtienen todos los puntos correspondientes a cada respuesta
    for respuesta in respuestasTotales:
        puntosTotales.append(comparar_respuesta(pregunta, respuesta, []))
    
    #Obtiene el minimo
    min = 100
    for i in range(len(puntosTotales)):
        if puntosTotales[i] < min:
            min = puntosTotales[i]
    
    #Retorna aquel que corresponda con el minimo.
    #Esta parte contempla que haya repetidos, toma el primero
    for i in range (5):
        if pregunta["Cantidad_R" + str(i + 1)] == min:
            for respuesta in respuestasTotales:
                if pregunta["Respuesta_" + str(i + 1)] == respuesta:
                    return pregunta["Respuesta_" + str(i + 1)]

import re

#Busca normalizar las respuestas de una pregunta
def normalizar(preguntaNormalizada:dict):
    for i in range(1, 6):
        preguntaNormalizada[f'Respuesta_{i}'] = normalizar_acentos(preguntaNormalizada[f'Respuesta_{i}'])
        preguntaNormalizada[f'Respuesta_{i}'] = normalizar_mayusculas(preguntaNormalizada[f'Respuesta_{i}'])
    return preguntaNormalizada

#Reemplaza las mayusculas por minusculas
def normalizar_mayusculas(palabra:str):
    palabra = re.sub(r'[A-Z]', lambda x: x.group(0).lower(), palabra)
    return palabra

#Reemplaza las vocales con tilde por sin tilde
def normalizar_acentos(palabra:str):
    palabra = re.sub(r'[áéíóúÁÉÍÓÚ]',\
            lambda x: {'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u',\
                        'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U'}\
                        .get(x.group(0), ''), palabra)
    return palabra

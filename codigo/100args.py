import random
import json
import pygame
from normalizar import *
from preguntasRespuestas import *

pygame.init()
#Ventana
ANCHO = 800
ALTO = 800
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("100 Argentinos dicen")

#Imagenes
pygame.display.set_icon(pygame.image.load("imgs/100argsdicen_logo.jpg"))
fondo = pygame.image.load("imgs/fondo_100_args.jpg")
fondoVacio = pygame.image.load("imgs/fondo_vacio.jpg")

#Tiempo
clock = pygame.time.Clock()

#Fuentes
font_input = pygame.font.Font(None, 32)
font = pygame.font.SysFont("Arial", 36)
font_timer = pygame.font.SysFont("Arial", 20)
font_titulo = pygame.font.SysFont("Arial", 60)

#Colores para el boton y el input
boton = pygame.Rect((ANCHO // 2) - 150, ALTO // 2, 300, 50)
input_box = pygame.Rect(200, 740, 400, 32)
color_inactivo = pygame.Color(255, 255, 255, 255)
color_activo = pygame.Color(0, 0, 0, 0)
color = color_inactivo
color_hover = pygame.Color(0, 0, 0, 0)
color_not_hover = pygame.Color(98, 0, 115, 255)
color_boton = color_not_hover
active = False
respuestaUsuario = ''

#Mysc para el juego
intentos = 3
txt_intentos = font_input.render(f"Intentos: {intentos}", True, (255, 255, 255)) #Blanco
nueva_ronda = True
puntos_usuario = 0
puntos_aumentos = 0
rondasRestantes = 5
tiempoRonda = 60

#Valores comodin
tiempoExtra = 0
multiplicador = False
comodin = True

#Lista de preguntas
listTematicas = []
try:
    with open('data/data.json', 'r', encoding='utf-8') as file:
        listTematicas = json.load(file)
except FileNotFoundError as e:
    print(f"Archivo no encontrado: {e}")
except json.JSONDecodeError as e:
    print(f"Formato no valido: {e}")
except UnicodeEncodeError as e:
    print(f"Palabras no contempladas en unicode: {e}")

#Menus
premio = 0
menu = 0

flag_Run = True
while flag_Run:

    timerReal = pygame.time.get_ticks() // 1000
    
    timer = tiempoRonda - (timerReal - tiempoExtra) # Comienza desde 60 y va disminuyendo
    txt_timer = font_timer.render(f"Tiempo: {timer} segundos", True, (0, 0, 0)) #El tiempo cambia cada tick

    ##Logica
    #Nueva ronda
    if nueva_ronda:
        tematica = elegir_tematica(listTematicas)
        pregunta = elegir_pregunta(listTematicas, tematica)
        listTematicas.remove(pregunta)

        txt_pregunta = font_input.render(f"{pregunta['Pregunta']}", True, (255, 255, 255)) #Blanco
        txt_tematica = font.render(f"Tematica: {pregunta['tematica']}", True, (255, 255, 255)) #Blanco

        txt_respuestas = [] #Se vacian las listas por cada ronda nueva
        respuestasRepetidas = []
        mostrarRespuestas = []
        
        #Machete
        for i in range(1,6):
            print(f"{pregunta[f'Respuesta_{i}']} + {pregunta[f'Cantidad_R{i}']}")
        nueva_ronda = False
    
    #Cambio de ronda
    if menu == 1 and (len(respuestasRepetidas) == 5 or timer < 0 or intentos < 1):
        nueva_ronda = True
        rondasRestantes -= 1
        intentos = 3
        txt_intentos = font_input.render(f"Intentos: {intentos}", True, (255, 255, 255))
        
        #Agrega los 60 de la ronda, ademas de agregar o sacar lo que el tiempo ya avanzó
        tiempoRonda = tiempoRonda - timer + 60 
        if rondasRestantes == 0:
            if puntos_usuario >= 500:
                premio = 1000000
            else:
                premio = 500 * puntos_usuario
            menu = 2

    #Ganaste un intento
    if puntos_aumentos > 50:
        puntos_aumentos -= 50
        intentos += 1
        txt_intentos = font_input.render(f"Intentos: {intentos}", True, (255, 255, 255))
    
    #Eventos de teclado
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            flag_Run = False
        if evento.type == pygame.MOUSEBUTTONDOWN:
            # Al hacer click en el input
            if input_box.collidepoint(evento.pos):
                active = not active
            else:
                active = False
            # Al hacer click en el boton de comenzar
            if boton.collidepoint(evento.pos):
                menu = 1
                #Agrega los 60 de la ronda, ademas de agregar o sacar lo que el tiempo ya avanzó
                tiempoRonda = tiempoRonda - timer + 60
            
            color = color_activo if active else color_inactivo #Color del input

        color_boton = color_hover if menu == 0 and boton.collidepoint(pygame.mouse.get_pos()) else color_not_hover #Color del boton
        
        if evento.type == pygame.KEYDOWN:
            #Acciona segun el input
            if active:
                if evento.key == pygame.K_RETURN: #Si apreto enter
                    respuestaUsuario = normalizar_acentos(respuestaUsuario)
                    respuestaUsuario = normalizar_mayusculas(respuestaUsuario)
                    preguntaNormalizada = pregunta.copy()
                    preguntaNormalizada = normalizar(preguntaNormalizada)

                    puntos = comparar_respuesta(preguntaNormalizada, respuestaUsuario, respuestasRepetidas)
                    
                    if respuestaUsuario == "comodin" and comodin: #De haber comodin y no se uso antes
                        tiempoExtra = 10 #Retrasa el tiempo 10 segundos
                        
                        #Se agrega la pregunta menos votada
                        respuestaComodin = elegir_minimo(pregunta, respuestasRepetidas)
                        rta = encontrarRespuesta(pregunta, respuestaComodin)
                        respuestasRepetidas.append(respuestaComodin)
                        renderText = font.render(f'{pregunta[rta]}: {pregunta["Cantidad_R"+ rta[-1]]} argentinos', True, (255, 255, 255))
                        tamanoText = renderText.get_size()
                        
                        #Centrar texto
                        x = (ventana.get_width() - tamanoText[0]) // 2
                        mostrarRespuestas.append([renderText, (x, 25 + 100 * int(rta[-1]))])
                        multiplicador = True #Multiplica x 2 la siguiente respuesta
                        comodin = False
                    else:
                        if puntos == 0:
                            intentos -= 1
                            txt_intentos = font_input.render(f"Intentos: {intentos}", True, (255, 255, 255))
                        else:
                            respuestasRepetidas.append(respuestaUsuario)
                            if multiplicador:
                                puntos_usuario += puntos * 2
                                puntos_aumentos += puntos * 2
                                multiplicador = False
                            else:
                                puntos_usuario += puntos
                                puntos_aumentos += puntos

                            print(puntos_usuario)
                            #Mostrar la respuesta adivinada
                            rta = encontrarRespuesta(preguntaNormalizada, respuestaUsuario)
                            renderText = font.render(f'{pregunta[rta]}: {pregunta["Cantidad_R"+ rta[-1]]} argentinos', True, (255, 255, 255))
                            tamanoText = renderText.get_size()
                            x = (ventana.get_width() - tamanoText[0]) // 2
                            mostrarRespuestas.append([renderText, (x, 135 + 83 * int(rta[-1]))])

                    respuestaUsuario = ''
                elif evento.key == pygame.K_BACKSPACE: #Si apreto para borrar
                    respuestaUsuario = respuestaUsuario[:-1]
                else: #Si apreto cualquier otro caracter
                    try:
                        respuestaUsuario += evento.unicode
                    except UnicodeEncodeError as e:
                        print(f"Palabras no contempladas en unicode: {e}")

    #Dibujar
    ventana.fill((150, 150, 150)) #Gris

    #Segun en que etapa del juego se carga un menu u otro
    if menu == 0:
        ventana.blit(fondoVacio, (0,0))

        txt_titulo = font_titulo.render("Empezar el juego", True, (255, 255, 255)) #Blanco
        rect = pygame.Rect(((ventana.get_width() - txt_titulo.get_size()[0]) // 2) - 5, 300,\
                            txt_titulo.get_width() + 10, txt_titulo.get_height() + 10)
        pygame.draw.rect(ventana, pygame.Color(98, 0, 115, 255), rect, 0)
        ventana.blit(txt_titulo, ((ventana.get_width() - txt_titulo.get_size()[0]) // 2, 300)) #Titulo
        
        txt_empezar = font.render("EMPECEMOS", True, (255, 255, 255)) #Blanco
        pygame.draw.rect(ventana, color_not_hover, boton, 0)
        pygame.draw.rect(ventana, color_boton, boton, 4)
        ventana.blit(txt_empezar, ((ventana.get_width() - txt_empezar.get_size()[0]) // 2, 405)) #Boton con empezar

    elif menu == 1:
        ventana.blit(fondo, (0,0))
        
        ventana.blit(txt_tematica, ((ventana.get_width() - txt_tematica.get_size()[0]) // 2, 70)) #Tematica
        ventana.blit(txt_timer, ((ventana.get_width() - txt_timer.get_size()[0]) // 2, 110)) #Tiempo

        for item in mostrarRespuestas: #Respuestas adivinadas
            ventana.blit(item[0], item[1])
        
        ventana.blit(txt_pregunta, (15, 690)) #Pregunta
        ventana.blit(txt_intentos, (650, 690)) #Intentos

        txt_input = font_input.render(respuestaUsuario, True, color)
        ventana.blit(txt_input, (input_box.x+5, input_box.y+5)) #Input   
        
        pygame.draw.rect(ventana, color, input_box, 2)
    elif menu == 2:
        ventana.blit(fondoVacio, (0,0))

        txt_titulo = font_titulo.render(f"HAS GANADO: ${premio}", True, (255, 255, 255)) #Blanco
        rect = pygame.Rect(((ventana.get_width() - txt_titulo.get_size()[0]) // 2) - 5, 300,\
                            txt_titulo.get_width() + 10, txt_titulo.get_height() + 10)
        pygame.draw.rect(ventana, pygame.Color(98, 0, 115, 255), rect, 0)
        ventana.blit(txt_titulo, ((ventana.get_width() - txt_titulo.get_size()[0]) // 2, 300)) #Monto final

    pygame.display.update()
    clock.tick(30)

pygame.quit()
from pygame import Color
from engine.IO import Teclas
from engine.misc import Resources as r, Config as C

class Constants:
    
    CUADRO = 32
    ANCHO = C.dato('resolucion/ANCHO')
    ALTO = C.dato('resolucion/ALTO')
    TECLAS = Teclas(C.dato('teclas'))
    
    GRUPO_ITEMS = 0
    GRUPO_SALIDAS = 1
    GRUPO_MOBS = 2
    CAPA_CIELO = 3

    CAPA_OVERLAYS_DIALOGOS = 1 # ocupan un framento de la pantalla
    CAPA_OVERLAYS_MENUS = 2 # ocupan toda o gran parte de la pantalla

    COLOR_COLISION = Color(255,0,255) #Fuchsia #FF00FF
    COLOR_IGNORADO = Color(1,1,1)
    
    #constantes de eventos de teclado
    HOLD = 24
    TAP = 25
    RELEASE = 26
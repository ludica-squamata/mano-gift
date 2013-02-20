#global information
from pygame import Color

class Constants(object):
    CUADRO = 32
    ALTO = 480
    ANCHO = 480

    CAPA_BACKGROUND = 0
    CAPA_GROUND_ITEMS = 1
    CAPA_GROUND_MOBS = 2
    CAPA_HERO = 3
    CAPA_TOP_ITEMS = 4
    CAPA_TOP_MOBS = 5

    COLOR_COLISION = Color(255,0,255) #Fuchsia #FF00FF
    
class Globales:
    MAPA_ACTUAL = ''
    

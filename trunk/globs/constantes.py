from pygame import Color
from .teclas import Teclas

class Constants:
    CUADRO = 32
    ANCHO = 480 #estas medidas podriamos ponerlas en config 
    ALTO = 480
    
    CAPA_BACKGROUND = 0
    CAPA_GROUND_ITEMS = 1
    CAPA_GROUND_SALIDAS = 2
    CAPA_GROUND_MOBS = 3
    CAPA_HERO = 4
    CAPA_TOP_ITEMS = 5
    CAPA_TOP_MOBS = 6
    CAPA_TOP_CIELO = 7

    CAPA_OVERLAYS_DIALOGOS = 1 # ocupan un framento de la pantalla
    CAPA_OVERLAYS_MENUS = 2 # ocupan toda o gran parte de la pantalla

    COLOR_COLISION = Color(255,0,255) #Fuchsia #FF00FF

    TECLAS = Teclas()
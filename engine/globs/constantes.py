from pygame import Color
from engine.IO import Teclas
from engine.misc import Config


class Constants:
    CUADRO = 32
    ANCHO = 640
    ALTO = 480
    TECLAS = Teclas(Config.dato('teclas'))
    
    CAPA_BACKGROUND = 0
    CAPA_GROUND_ITEMS = 1
    CAPA_GROUND_SALIDAS = 2
    CAPA_GROUND_MOBS = 3
    CAPA_HERO = 4
    CAPA_TOP_ITEMS = 5
    CAPA_TOP_MOBS = 6
    CAPA_TOP_CIELO = 7

    CAPA_OVERLAYS_INVENTARIO = 0
    CAPA_OVERLAYS_HUD = 1
    CAPA_OVERLAYS_DIALOGOS = 2  # ocupan un framento de la pantalla
    CAPA_OVERLAYS_MENUS = 3  # ocupan toda o gran parte de la pantalla

    COLOR_COLISION = Color(255, 0, 255)  # Fuchsia #FF00FF
    COLOR_IGNORADO = Color(1, 1, 1)

    # constantes de eventos de teclado
    HOLD = 24
    TAP = 25
    RELEASE = 26

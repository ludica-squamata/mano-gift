from pygame import Color
from engine.IO import Teclas
from engine.misc import Config

CUADRO = 32
ANCHO = 640
ALTO = 480
TECLAS = Teclas(Config.dato('teclas'))
SAVEFD = Config.savedir

GRUPO_ITEMS = 0
GRUPO_SALIDAS = 1
GRUPO_MOBS = 2
CAPA_CIELO = 3
CUADRANTE_NO = 4
CUADRANTE_NE = 5
CUADRANTE_SO = 6
CUADRANTE_SE = 7

CAPA_OVERLAYS_INVENTARIO = 0
CAPA_OVERLAYS_HUD = 1
CAPA_OVERLAYS_DIALOGOS = 2  # ocupan un framento de la pantalla
CAPA_OVERLAYS_MENUS = 3  # ocupan toda o gran parte de la pantalla
CAPA_OVERLAYS_CIRCULAR = 4

# noinspection PyArgumentList
COLOR_COLISION = Color(255, 0, 255)  # Fuchsia #FF00FF
# noinspection PyArgumentList
COLOR_IGNORADO = Color(1, 1, 1)

# constantes de eventos de teclado
HOLD = 24
TAP = 25
RELEASE = 26

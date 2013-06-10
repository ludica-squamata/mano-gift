#global information
import pygame
from misc import Resources as r

class Teclas:
    ARRIBA = pygame.K_UP
    ABAJO = pygame.K_DOWN
    IZQUIERDA= pygame.K_LEFT
    DERECHA = pygame.K_RIGHT

    ACCION = pygame.K_x
    HABLAR = pygame.K_s
    CANCELAR_DIALOGO = pygame.K_a
    INVENTARIO = pygame.K_z
    MENU = pygame.K_RETURN
    SALIR = pygame.K_ESCAPE


    def asignar (self,data):
        Teclas.ARRIBA = data['arriba']
        Teclas.ABAJO = data['abajo']
        Teclas.IZQUIERDA = data['izquierda']
        Teclas.DERECHA = data['derecha']

        Teclas.ACCION = data['accion']
        Teclas.INVENTARIO = data['inventario']
        Teclas.MENU = data['menu']
        Teclas.SALIR = data['salir']

class Constants:
    CUADRO = 32
    ALTO = 480
    ANCHO = 480

    CAPA_BACKGROUND = 0
    CAPA_GROUND_ITEMS = 1
    CAPA_GROUND_SALIDAS = 2
    CAPA_GROUND_MOBS = 3
    CAPA_HERO = 4
    CAPA_TOP_ITEMS = 5
    CAPA_TOP_MOBS = 6

    CAPA_OVERLAYS_DIALOGO = 1
    CAPA_OVERLAYS_INVENTARIO = 2

    COLOR_COLISION = pygame.Color(255,0,255) #Fuchsia #FF00FF

    TECLAS = Teclas()

class World:
    mapas = {}
    MAPA_ACTUAL =''
    HERO =''
    onDialog = False
    onSelect = False
    
    def cargar_hero():
        from mobs import PC
        World.HERO = PC('heroe','mobs/heroe_color12.png',World.MAPA_ACTUAL)

    def setear_mapa(mapa, entrada):
        from mapa import Stage
        if mapa not in World.mapas:
            World.mapas[mapa] = Stage(r.abrir_json('maps/'+mapa+'.json'))
        World.MAPA_ACTUAL = World.mapas[mapa]
        World.MAPA_ACTUAL.cargar_hero(World.HERO, entrada)
        World.MAPA_ACTUAL.mapa.dirty=1

FPS = pygame.time.Clock()

i = 10
while i > 0:
    FPS.tick(60)
    i-=1
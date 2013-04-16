#global information
import pygame
from misc import Resources as r

class Teclas:
    ARRIBA = pygame.K_UP
    ABAJO = pygame.K_DOWN
    IZQUIERDA= pygame.K_LEFT
    DERECHA = pygame.K_RIGHT

    ACCION = pygame.K_x
    MENU = pygame.K_RETURN
    SALIR = pygame.K_ESCAPE
    
    def asignar (self,data):
        Teclas.ARRIBA = data['arriba']
        Teclas.ABAJO = data['abajo']
        Teclas.IZQUIERDA = data['izquierda']
        Teclas.DERECHA = data['derecha']
        
        Teclas.ACCION = data['accion']
        Teclas.MENU = data['menu']
        Teclas.SALIR = data['salir']

class Constants:
    CUADRO = 32
    ALTO = 480
    ANCHO = 480

    CAPA_BACKGROUND = 0
    CAPA_GROUND_ITEMS = 1
    CAPA_GROUND_MOBS = 2
    CAPA_HERO = 3
    CAPA_TOP_ITEMS = 4
    CAPA_TOP_MOBS = 5

    COLOR_COLISION = pygame.Color(255,0,255) #Fuchsia #FF00FF
    
    TECLAS = Teclas()

class World:
    mapas = {}
    MAPA_ACTUAL =''
    HERO =''
    def cargar_hero():
        from mobs import PC
        World.HERO = PC('mobs/heroe_color4.png',World.MAPA_ACTUAL)

    def setear_mapa(mapa, entrada):
        from mapa import Stage
        if mapa not in World.mapas:
            World.mapas[mapa] = Stage(r.abrir_json('maps/'+mapa+'.json'))
        World.MAPA_ACTUAL = World.mapas[mapa]
        World.MAPA_ACTUAL.cargar_hero(World.HERO, entrada)
        World.MAPA_ACTUAL.mapa.dirty=1
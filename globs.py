#global information
from pygame import Color
from mobs import PC
from misc import Resources as r

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

    COLOR_COLISION = Color(255,0,255) #Fuchsia #FF00FF

class World:
    mapas = {}
    MAPA_ACTUAL =''
    HERO =''
    def cargar_hero():
        World.HERO = PC('grafs/heroe_color.png')

    def setear_mapa(mapa, entrada):
        from mapa import Stage
        if mapa not in World.mapas:
            World.mapas[mapa] = Stage(r.abrir_json('maps/'+mapa+'.json'))
        World.MAPA_ACTUAL = World.mapas[mapa]
        World.MAPA_ACTUAL.cargar_hero(World.HERO, entrada)
        World.MAPA_ACTUAL.mapa.dirty=1
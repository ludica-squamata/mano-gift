from misc import Resources as r
from .tiempo import Tiempo as T
from .constantes import Constants as C

class World:
    mapas = {}
    MAPA_ACTUAL = ''
    HERO = ''
    menu_actual = ''
    menu_previo = ''
    MENUS = {}
    DIALOG = None
    MODO = 'Aventura'
    onPause = False
    QUESTS = []
    
    def cargar_hero():
        from mobs import PC
        if World.HERO == '':
            World.HERO = PC('heroe',r.abrir_json('data/mobs/hero.mob'),World.MAPA_ACTUAL)

    def setear_mapa(mapa, entrada):
        from mapa import Stage
        if mapa not in World.mapas:
            World.mapas[mapa] = Stage(r.abrir_json('data/maps/'+mapa+'.json'))
        World.MAPA_ACTUAL = World.mapas[mapa]
        World.MAPA_ACTUAL.cargar_hero(World.HERO, entrada)
        World.MAPA_ACTUAL.mapa.dirty=1
        World.MAPA_ACTUAL.contents.add(T.noche)
        World.MAPA_ACTUAL.properties.add(T.noche,layer=C.CAPA_TOP_CIELO)
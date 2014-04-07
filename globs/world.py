from misc import Resources as r
from .tiempo import Tiempo as T
from .constantes import Constants as C
from .renderer import Renderer

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
    RENDERER = Renderer()
    
    def setear_mapa(mapa, entrada):
        from mapa import Stage
        if mapa not in World.mapas:
            World.mapas[mapa] = Stage(r.abrir_json('data/maps/'+mapa+'.json'),entrada)
        World.MAPA_ACTUAL = World.mapas[mapa]
        World.RENDERER.clear()
        World.RENDERER.setBackground(World.MAPA_ACTUAL.mapa)
        for obj in World.MAPA_ACTUAL.properties:
            World.RENDERER.addObj(obj,obj.rect.bottom)
        World.RENDERER.camara.centrar()
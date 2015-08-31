from engine.misc import Resources as r
from .mod_data import ModData as MD
from .giftgroups import MobGroup
from .renderer import Renderer
from .tiempo import Tiempo
from .eventDispatcher import EventDispatcher

class EngineData:
    mapas = {}
    MAPA_ACTUAL = None
    HERO = None
    DIALOG = None
    HUD = None
    menu_actual = ''
    menu_previo = ''
    MENUS = {}
    MODO = ''
    onPause = False
    RENDERER = Renderer()
    EVENTS = EventDispatcher()
    
    scene_data = None
    
    @classmethod
    def setear_escena(cls,nombre):
        cls.MODO = 'Aventura'
        scene_data = r.abrir_json(MD.scenes+nombre+'.scene')
        cls.scene_data = scene_data
        stage,entrada = scene_data['stage']
        cls.setear_mapa(stage,entrada)
        Tiempo.setear_momento(scene_data['dia'],*scene_data['hora'])
        if scene_data['focus'] != '':
            cls.RENDERER.camara.set_focus(MobGroup[scene_data['focus']])
            cls.RENDERER.use_focus = True
        else:
            cls.RENDERER.use_focus = False
    
    @classmethod
    def setear_mapa(cls,nombre,entrada):
        cls.RENDERER.clear()
        from engine.UI.hud import HUD
        from engine.mapa import Stage
        from engine.mapa.loader import _loader
        if nombre not in cls.mapas:
            cls.mapas[nombre] = Stage(nombre,cls.scene_data['mobs'],entrada)
        else:
            _loader.setStage(cls.mapas[nombre])
            _loader.cargar_hero(entrada)
        cls.MAPA_ACTUAL = cls.mapas[nombre]
        cls.MAPA_ACTUAL.register_at_renderer(entrada)
        cls.HUD = HUD()

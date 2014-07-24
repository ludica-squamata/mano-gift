from engine.misc import Resources as r
from .mod_data import ModData as MD
from .giftgroups import MobGroup
from .renderer import Renderer
from .tiempo import Tiempo

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
    
    scene_data = None
    
    @staticmethod
    def setear_escena(nombre):
        ED = EngineData
        ED.MODO = 'Aventura'
        scene_data = r.abrir_json(MD.scenes+nombre+'.scene')
        ED.scene_data = scene_data
        stage,entrada = scene_data['stage']
        ED.setear_mapa(stage,entrada)
        Tiempo.setear_momento(scene_data['dia'],scene_data['hora'])
        ED.RENDERER.camara.setFocus(MobGroup[scene_data['focus']])
    
    @staticmethod
    def setear_mapa(nombre,entrada):
        ED = EngineData
        ED.RENDERER.clear()
        from engine.UI.hud import HUD
        from engine.mapa import Stage
        if nombre not in ED.mapas:
            ED.mapas[nombre] = Stage(nombre,ED.scene_data['mobs'],entrada)
        ED.MAPA_ACTUAL = ED.mapas[nombre]
        ED.MAPA_ACTUAL.register_at_renderer(entrada)
        ED.HUD = HUD()
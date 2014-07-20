from engine.misc import Resources as r
from .mod_data import ModData as MD
from .giftgroups import MobGroup
from .renderer import Renderer
from .tiempo import Tiempo

class EngineData:
    MAPA_ACTUAL = None
    HERO = ''
    menu_actual = ''
    menu_previo = ''
    MENUS = {}
    DIALOG = None
    MODO = ''
    onPause = False
    RENDERER = Renderer()
    HUD = None
    
    @staticmethod
    def setear_escena(nombre):
        from engine.mapa import Stage
        EngineData.MODO = 'Aventura'
        scene_data = r.abrir_json(MD.scenes+nombre+'.scene')
        
        EngineData.MAPA_ACTUAL = Stage(scene_data['mobs'],*scene_data['stage'])
        Tiempo.setear_momento(scene_data['dia'],scene_data['hora'])
        EngineData.RENDERER.camara.setFocus(MobGroup.get(scene_data['focus']))
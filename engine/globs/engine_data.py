from .eventDispatcher import EventDispatcher
from engine.misc import Resources
from .mod_data import ModData
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
    scene_data = None

    @classmethod
    def setear_escena(cls, nombre):
        cls.MODO = 'Aventura'
        scene_data = Resources.abrir_json(ModData.scenes + nombre + '.scene')
        cls.scene_data = scene_data
        stage, entrada = scene_data['stage']
        cls.setear_mapa(stage, entrada)
        Tiempo.setear_momento(scene_data['dia'], *scene_data['hora'])
        focus = scene_data.get('focus', False)
        if focus:
            if focus in MobGroup:
                focus = MobGroup[scene_data['focus']]
            else:
                for prop in cls.MAPA_ACTUAL.properties:
                    if focus == prop.nombre:
                        focus = prop

            Renderer.camara.set_focus(focus)
            Renderer.use_focus = True
        else:
            Renderer.use_focus = False

    @classmethod
    def setear_mapa(cls, nombre, entrada):
        Renderer.clear()
        from engine.UI.hud import HUD
        from engine.mapa import Stage
        from engine.mapa.loader import Loader
        if nombre not in cls.mapas:
            cls.mapas[nombre] = Stage(nombre, cls.scene_data['mobs'], entrada)
        else:
            Loader.set_stage(cls.mapas[nombre])
            Loader.cargar_hero(entrada)
        cls.MAPA_ACTUAL = cls.mapas[nombre]
        cls.MAPA_ACTUAL.register_at_renderer()
        cls.HUD = HUD()

    @classmethod
    def on_cambiarmapa(cls, evento):
        if evento.data['mob'] is cls.HERO:
            cls.setear_mapa(evento.data['dest'], evento.data['link'])

EventDispatcher.register(EngineData.on_cambiarmapa, "CambiarMapa")

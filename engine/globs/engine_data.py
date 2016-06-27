from .eventDispatcher import EventDispatcher
from engine.misc import Resources
from .mod_data import ModData
from .giftgroups import MobGroup
from .renderer import Renderer
from .tiempo import Tiempo
from .constantes import SAVEFD


class EngineData:
    mapas = {}
    MAPA_ACTUAL = None
    """:type : engine.mapa.Stage.Stage"""
    HERO = None
    DIALOG = None
    HUD = None
    current_qcm_idx = 0
    menu_actual = ''
    acceso_menues = []
    MENUS = {}
    MODO = ''
    onPause = False
    scene_data = None
    setKey = False
    char_name = ''

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

    @classmethod
    def on_setkey(cls, event):
        """
        :param event:
        :type event: AzoeEvent
        :return:
        """
        value = event.data['value']

        if event.data['mode'] == 'SetKey':
            cls.setKey = value
    
    @classmethod
    def end_dialog(cls, layer):
        Renderer.clear_overlays_from_layer(layer)
        cls.DIALOG = None
        cls.MODO = 'Aventura'
        cls.onPause = False

    @classmethod
    def salvar(cls, event):
        data = {
            'name': cls.char_name,
            'mapa': cls.MAPA_ACTUAL.nombre
        }
        data.update(event.data)

        Resources.guardar_json(SAVEFD+'/save.json', data)


EventDispatcher.register(EngineData.on_cambiarmapa, "CambiarMapa")
EventDispatcher.register(EngineData.on_setkey, "SetMode")
EventDispatcher.register(EngineData.salvar, "Save")

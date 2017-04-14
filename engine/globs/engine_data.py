from .eventDispatcher import EventDispatcher
from engine.misc import Resources
from .giftgroups import Mob_Group
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
    save_data = {'NPC': {}}
    current_view = 'north'

    @classmethod
    def setear_mapa(cls, nombre, entrada):
        Renderer.clear()
        from engine.UI.hud import HUD
        from engine.mapa import Stage
        from engine.mapa.loader import Loader
        if nombre not in cls.mapas:
            cls.mapas[nombre] = Stage(nombre, entrada)
        else:
            Loader.load_hero(entrada)
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
        cls.setKey = event.data['value']

    @classmethod
    def end_dialog(cls, layer):
        Renderer.clear_overlays_from_layer(layer)
        cls.DIALOG = None
        # cls.menu_actual.deregister()  # no estoy seguro de que se pueda usar todas las veces.
        EventDispatcher.trigger('TogglePause', 'EngineData', {'value': False})
        if cls.HUD is not None:
            cls.MODO = 'Aventura'
            cls.HERO.register()
            cls.HUD.show()

    @classmethod
    def salvar(cls, event):
        data = Resources.abrir_json(SAVEFD + '/' + cls.char_name + '.json')
        data.update(event.data)
        Resources.guardar_json(SAVEFD + '/' + cls.char_name + '.json', data)

    @classmethod
    def new_game(cls, char_name):
        cls.char_name = char_name
        Resources.guardar_json(SAVEFD + '/' + char_name + '.json', {"name": char_name})
        EventDispatcher.trigger('NewGame', 'engine', {})

    @classmethod
    def load_savefile(cls, filename):
        data = Resources.abrir_json(SAVEFD + '/' + filename)
        cls.save_data.update(data)
        cls.char_name = data['name']
        EventDispatcher.trigger('NewGame', 'engine', {'savegame': data})

    @classmethod
    def cargar_juego(cls, mapa, entrada, dia, hora, minutos, focus):
        cls.acceso_menues.clear()
        cls.setear_mapa(mapa, entrada)
        if not Tiempo.clock.is_real():
            Tiempo.set_time(dia, hora, minutos)
        Renderer.set_focus(Mob_Group[focus])
        cls.MODO = 'Aventura'
        cls.HUD.show()

    @classmethod
    def compound_save_data(cls, event):
        if event.origin in cls.save_data:
            cls.save_data[event.origin][event.data['nombre']] = {}
        else:
            cls.save_data.update(event.data)

        if not EventDispatcher.is_quequed('SaveDataFile'):
            EventDispatcher.trigger('SaveDataFile', 'EngineData', cls.save_data)

    @classmethod
    def rotarte_view(cls, event):
        cls.current_view = event.data['new_view']

    @classmethod
    def toggle_pause(cls, event):
        cls.onPause = event.data['value']


EventDispatcher.register(EngineData.on_cambiarmapa, "SetMap")
EventDispatcher.register(EngineData.on_setkey, "ToggleSetKey")
EventDispatcher.register(EngineData.salvar, "SaveDataFile")
EventDispatcher.register(EngineData.compound_save_data, "SaveData")
EventDispatcher.register(EngineData.rotarte_view, 'RotateEverything')
EventDispatcher.register(EngineData.toggle_pause, 'TogglePause')

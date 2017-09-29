from .eventDispatcher import EventDispatcher
from engine.misc import abrir_json, guardar_json
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
    save_data = {}
    current_view = 'north'

    @classmethod
    def setear_mapa(cls, stage, entrada, mob=None, is_new_game=False):
        from engine.mapa import Stage
        x, y = 0, 0
        Renderer.clear()
        if stage not in cls.mapas or is_new_game:
            cls.mapas[stage] = Stage(stage, entrada)
        else:
            x, y = cls.mapas[stage].data['entradas'][entrada]['pos']
            cls.HERO.ubicar_en_entrada(x, y)

        cls.MAPA_ACTUAL = cls.mapas[stage]
        cls.MAPA_ACTUAL.register_at_renderer(mob)

        if x or y:
            cls.MAPA_ACTUAL.mapa.rect.topleft = 320 - x, 240 - y
            Renderer.camara.panear()

    @classmethod
    def on_cambiarmapa(cls, evento):
        if Renderer.camara.is_focus(evento.data['mob']):
            cls.setear_mapa(evento.data['target_stage'],
                            evento.data['target_entrada'],
                            mob=evento.data['mob'])

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
        EventDispatcher.trigger('TogglePause', 'EngineData', {'value': False})
        if cls.HUD is not None:
            cls.MODO = 'Aventura'
            cls.HERO.AI.register()
            cls.HUD.show()

    @classmethod
    def salvar(cls, event):
        data = abrir_json(SAVEFD + '/' + cls.char_name + '.json')
        data.update(event.data)
        guardar_json(SAVEFD + '/' + cls.char_name + '.json', data)

    @classmethod
    def new_game(cls, char_name):
        cls.char_name = char_name
        guardar_json(SAVEFD + '/' + char_name + '.json', {"name": char_name})
        EventDispatcher.trigger('NewGame', 'engine', {})

    @classmethod
    def load_savefile(cls, filename):
        data = abrir_json(SAVEFD + '/' + filename)
        cls.save_data.update(data)
        cls.char_name = data['name']
        EventDispatcher.trigger('NewGame', 'engine', {'savegame': data})

    @classmethod
    def cargar_juego(cls, data):
        from engine.UI.hud import HUD
        cls.acceso_menues.clear()
        
        cls.setear_mapa(data['mapa'], data['entrada'], is_new_game=True)
        if not Tiempo.clock.is_real():
            Tiempo.set_time(*data['tiempo'])
        focus = data['focus']
        Renderer.set_focus(Mob_Group[focus])
        cls.HERO = Mob_Group[focus]
        cls.MODO = 'Aventura'
        cls.HUD = HUD(Mob_Group[focus])
        cls.HUD.show()

    @classmethod
    def compound_save_data(cls, event):
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

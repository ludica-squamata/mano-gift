from .eventDispatcher import EventDispatcher
from engine.misc import abrir_json, guardar_json, salir_handler, salir
from .giftgroups import Mob_Group
from .renderer import Renderer
from .tiempo import Tiempo
from .constantes import SAVEFD


class EngineData:
    mapas = {}
    HERO = None
    HUD = None
    current_qcm_idx = 0
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
        Renderer.clear()
        if stage not in cls.mapas or is_new_game:
            cls.mapas[stage] = Stage(stage, entrada)
        else:
            cls.mapas[stage].ubicar_en_entrada(entrada)

        cls.mapas[stage].register_at_renderer(mob)

        return cls.mapas[stage]

    @classmethod
    def on_cambiarmapa(cls, evento):
        if Renderer.camara.is_focus(evento.data['mob']):
            cls.setear_mapa(evento.data['target_stage'],
                            evento.data['target_entrada'],
                            mob=evento.data['mob'])
            stage = evento.data['target_stage']
            x, y = cls.mapas[stage].posicion_entrada(evento.data['target_entrada'])
            cls.HERO.ubicar_en_entrada(x, y)

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
        Mob_Group.clear()
        EventDispatcher.trigger('NewGame', 'engine', {'savegame': data})

    @classmethod
    def cargar_juego(cls, data):
        from engine.UI.hud import HUD
        cls.acceso_menues.clear()

        mapa = cls.setear_mapa(data['mapa'], data['entrada'], is_new_game=True)
        if not Tiempo.clock.is_real():
            Tiempo.set_time(*data['tiempo'])

        focus = Mob_Group[data['focus']]
        Renderer.set_focus(focus)

        cls.check_focus_position(focus, mapa, data['entrada'])

        cls.HERO = focus
        cls.MODO = 'Aventura'
        cls.HUD = HUD(focus)
        cls.HUD.show()

    @classmethod
    def check_focus_position(cls, focus, mapa, entrada):
        fx, fy = focus.mapRect.center
        ex, ey = mapa.data['entradas'][entrada]['pos']
        if fx != ex or fy != ey:
            texto = 'Error\nEl foco de la cámara no está en el centro. Verificar que la posición inicial\ndel foco ' \
                    'en el chunk ({},{}) sea la  misma que la posición de la entrada \n({},{}).'.format(fx, fy, ex, ey)
            salir(texto)

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
EventDispatcher.register(salir_handler, 'QUIT')

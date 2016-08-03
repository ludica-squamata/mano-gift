from .eventDispatcher import EventDispatcher
from engine.misc import Resources
from .mod_data import ModData
from .giftgroups import MobGroup, ItemGroup
from .renderer import Renderer
from .tiempo import Tiempo
from .constantes import SAVEFD
import os.path


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
    def load_savefile(cls, filename):
        data = Resources.abrir_json(SAVEFD + '/' + filename)
        cls.char_name = data['name']
        if 'scene' in data:
            cls.setear_escena(data['scene'], savedata=data)

    @classmethod
    def setear_escena(cls, idx, savedata=None):
        cls.MODO = 'Aventura'
        cls.onPause = False
        cls.acceso_menues.clear()
        if savedata is None:
            savedata = {}

        ruta = ModData.scenes + str(idx) + '.json'
        if os.path.isfile(ruta):
            cls.scene_data = Resources.abrir_json(ruta)
            cls.scene_data.update({'ID': idx})
            mapa, entrada = None, None  # para corregir una advertencia de PyCharm
            if 'mapa' in savedata:
                mapa = savedata['mapa']
                entrada = savedata['link']
            elif 'stage' in cls.scene_data:
                mapa = cls.scene_data['stage']['mapa']
                entrada = cls.scene_data['stage']['entrada']
            cls.setear_mapa(mapa, entrada)

            if 'mobs' in cls.scene_data:
                # este es un hook para modificar la IA de los mobs
                # si así la escena lo demandara.
                pass

            if 'tiempo' in cls.scene_data:
                dia = cls.scene_data['tiempo']['dia']
                hora = cls.scene_data['tiempo']['hora']
                Tiempo.setear_momento(dia, *hora)

            if 'focus' in cls.scene_data:
                # la escena puede no especificar un foco
                # lo que implica que el foco no cambia,
                # no que se vuelva None necesariamente.
                focus = cls.scene_data.get('focus', False)
                if focus:
                    if focus in MobGroup:
                        focus = MobGroup[focus]

                    elif focus in ItemGroup:
                        focus = ItemGroup[focus]

                    Renderer.set_focus(focus)
                else:
                    Renderer.set_focus()

        else:
            raise OSError('la Escena no existe')

    @classmethod
    def setear_mapa(cls, nombre, entrada):
        Renderer.clear()
        from engine.UI.hud import HUD
        from engine.mapa import Stage
        from engine.mapa.loader import Loader
        if nombre not in cls.mapas:
            cls.mapas[nombre] = Stage(nombre, cls.scene_data.get('mobs', {}), entrada)
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
        data = Resources.abrir_json(SAVEFD + '/' + cls.char_name + '.json')
        data.update({
            'mapa': cls.MAPA_ACTUAL.nombre,
            'link': cls.MAPA_ACTUAL.entrada,
            'scene': cls.scene_data['ID']
        }
        )

        data.update(event.data)

        Resources.guardar_json(SAVEFD + '/' + cls.char_name + '.json', data)

    @classmethod
    def new_game(cls, char_name):
        cls.char_name = char_name
        data = {
            "name": char_name,
            "scene": 0
        }
        Resources.guardar_json(SAVEFD + '/' + char_name + '.json', data)
        cls.setear_escena(data['scene'])


EventDispatcher.register(EngineData.on_cambiarmapa, "CambiarMapa")
EventDispatcher.register(EngineData.on_setkey, "SetMode")
EventDispatcher.register(EngineData.salvar, "Save")

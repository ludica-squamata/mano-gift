from engine.misc import abrir_json, guardar_json, salir_handler, salir, Config
from .constantes import CAPA_OVERLAYS_MENUS
from .event_dispatcher import EventDispatcher, AzoeEvent
from .game_groups import Mob_Group
from .renderer import Renderer
from .tiempo import Tiempo
from .mod_data import ModData


class EngineData:
    mapas = {}
    acceso_menues = []
    MENUS = {}
    setKey = False
    save_data = {}
    character = {}

    @classmethod
    def setear_mapa(cls, stage, entrada, mob=None, is_new_game=False):
        from engine.mapa import Stage
        if stage not in cls.mapas or is_new_game:
            cls.mapas[stage] = Stage(stage, entrada)
        else:
            cls.mapas[stage].ubicar_en_entrada(entrada)

        if mob is not None:
            cls.mapas[stage].mapa.add_property(mob, 2)
            mob.set_parent_map(cls.mapas[stage].mapa)

        return cls.mapas[stage]

    @classmethod
    def on_cambiarmapa(cls, evento):
        mapa_actual = Renderer.camara.focus.stage
        mob = evento.data['mob']
        mapa_actual.del_property(mob)
        if Renderer.camara.is_focus(evento.data['mob']):
            cls.setear_mapa(evento.data['target_stage'],
                            evento.data['target_entrada'],
                            mob=evento.data['mob'])
            stage = evento.data['target_stage']
            x, y = cls.mapas[stage].posicion_entrada(evento.data['target_entrada'])
            Renderer.camara.focus.ubicar_en_entrada(x, y)
        else:
            mob.set_parent_map(None)

    @classmethod
    def on_setkey(cls, event):
        """
        :param event:
        :type event: AzoeEvent
        :return:
        """
        cls.setKey = event.data['value']

    @classmethod
    def end_dialog(cls):
        EventDispatcher.trigger('TogglePause', 'EngineData', {'value': False})

    @classmethod
    def salvar(cls, event):
        name = event.data['name']
        data = abrir_json(Config.savedir + '/' + name + '.json')
        data.update(event.data)
        guardar_json(Config.savedir + '/' + name + '.json', data)

    @classmethod
    def new_game(cls, char_name):
        guardar_json(Config.savedir + '/' + char_name + '.json', {"name": char_name})
        EventDispatcher.trigger('NewGame', 'engine', {'savegame': {"name": char_name}})

    @classmethod
    def load_savefile(cls, filename):
        data = abrir_json(Config.savedir + '/' + filename)
        cls.save_data.update(data)
        Mob_Group.clear()
        EventDispatcher.trigger('NewGame', 'engine', {'savegame': data})

    @classmethod
    def cargar_juego(cls, event):
        data = event.data
        cls.acceso_menues.clear()

        mapa = cls.setear_mapa(data['mapa'], data['entrada'], is_new_game=True)
        if not Tiempo.clock.is_real():
            Tiempo.set_time(*data['tiempo'])

        focus = Mob_Group[data['focus']]
        Renderer.set_focus(focus)

        cls.check_focus_position(focus, mapa, data['entrada'])
        focus.character_name = data['name']

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
    def pop_menu(cls, event=None):
        from engine.UI.menues import default_menus

        if event is None and not len(cls.acceso_menues):
            titulo = 'Pausa'
        elif event is not None:
            titulo = event.data['value']
        else:
            # esto evita que se abra el menú Pausa desde Menú Cargar (lo que provoca un crash).
            # es necesario porque Modos ya no existe, y sería la única otra forma
            # de evitar que pop_menu() respodiese al tap de la tecla Menu.
            return

        if titulo == 'Previous':
            del cls.acceso_menues[-1]
            titulo = cls.acceso_menues[-1]
        else:
            cls.acceso_menues.append(titulo)

        if titulo not in EngineData.MENUS:
            name = 'Menu' + titulo
            if name in ModData.custommenus:
                menu = ModData.custommenus[name]()
            elif name in default_menus:
                menu = default_menus[name]()
            else:
                raise NotImplementedError('El menu "{}" no existe'.format(titulo))
        else:
            menu = cls.MENUS[titulo]
            menu.reset()

        menu.register()
        EventDispatcher.trigger('TogglePause', 'Modos', {'value': True})
        Renderer.add_overlay(menu, CAPA_OVERLAYS_MENUS)
        Renderer.overlays.move_to_front(menu)

    @classmethod
    def create_character(cls, event):
        final = event.data.pop('final')
        cls.character.update(event.data)
        if final:
            cls.character.update({'AI': 'controllable'})
            cls.new_game(cls.character['nombre'])


EventDispatcher.register(EngineData.on_cambiarmapa, "SetMap")
EventDispatcher.register(EngineData.on_setkey, "ToggleSetKey")
EventDispatcher.register(EngineData.salvar, "SaveDataFile")
EventDispatcher.register(EngineData.compound_save_data, "SaveData")
EventDispatcher.register(EngineData.pop_menu, AzoeEvent('Key', 'Input', {'nom': 'menu', 'type': 'tap'}))
EventDispatcher.register(EngineData.pop_menu, 'OpenMenu')
EventDispatcher.register(lambda e: EngineData.end_dialog(), 'EndDialog')
EventDispatcher.register(salir_handler, 'QUIT')
EventDispatcher.register(EngineData.cargar_juego, 'LoadGame')
EventDispatcher.register(EngineData.create_character, 'CharacterCreation')

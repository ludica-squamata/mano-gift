from engine.misc import abrir_json, guardar_json, salir_handler, salir, Config
from .constantes import CAPA_OVERLAYS_MENUS
from .event_dispatcher import EventDispatcher, AzoeEvent
from .game_groups import Mob_Group
from .renderer import Renderer
from .tiempo import Tiempo, SeasonalYear
from .mod_data import ModData
from os import path, mkdir, getcwd
from .sun import Sun


class EngineData:
    mapas = {}
    acceso_menues = []
    MENUS = {}
    setKey = False
    save_data = {}
    character = {
        'AI': 'controllable'
    }
    transient_mobs = {}

    @classmethod
    def init(cls):
        EventDispatcher.register_many(
            (cls.on_cambiarmapa, "SetMap"),
            (cls.on_setkey, "ToggleSetKey"),
            (cls.save_transient_npcs, 'Save'),
            (cls.salvar, "SaveDataFile"),
            (cls.compound_save_data, "SaveData"),
            (cls.pop_menu, AzoeEvent('Key', 'Input', {'nom': 'menu', 'type': 'tap'})),
            (cls.pop_menu, 'OpenMenu'),
            (lambda e: cls.end_dialog(), 'EndDialog'),
            (salir_handler, 'QUIT'),
            (cls.cargar_juego, 'LoadGame'),
            (cls.create_character, 'CharacterCreation')
        )

    @classmethod
    def setear_mapa(cls, stage, entrada, mob=None, is_new_game=False):
        from engine.mapa import Stage
        if stage not in cls.mapas or is_new_game:
            cls.mapas[stage] = Stage(stage, mob, entrada)
        else:
            cls.mapas[stage].ubicar_en_entrada(entrada)

        if mob is not None:
            cls.mapas[stage].mapa.add_property(mob, 2)
            mob.set_parent_map(cls.mapas[stage].mapa)

        if stage in cls.transient_mobs:
            for item in cls.transient_mobs[stage]:
                mob = item['mob']
                x, y = cls.mapas[stage].posicion_entrada(item['pos'])
                dx, dy = mob.direcciones[mob.direccion]
                dx *= 32
                dy *= 32
                mob.ubicar_en_mapa(x + dx, y + dy)
                if type(mob) is not str:
                    cls.mapas[stage].mapa.add_property(mob, 2)
                    mob.set_parent_map(cls.mapas[stage].mapa)

        return cls.mapas[stage]

    @classmethod
    def on_cambiarmapa(cls, evento):
        mapa_actual = Renderer.camara.focus.stage
        mob = evento.data['mob']
        mapa_actual.del_property(mob)
        stage = evento.data['target_stage']
        entrada = evento.data['target_entrada']
        if Renderer.camara.is_focus(mob):
            EventDispatcher.trigger('EndDialog', cls, {})
            mapa = cls.setear_mapa(stage, entrada, mob=mob)
            SeasonalYear.propagate()
            x, y = mapa.posicion_entrada(entrada)
            Renderer.camara.focus.ubicar_en_entrada(x, y)
        else:
            pos = entrada if stage not in cls.mapas else cls.mapas[stage].posicion_entrada(entrada)
            if stage not in cls.transient_mobs:
                cls.transient_mobs[stage] = []
            cls.transient_mobs[stage].append({'mob': mob, 'pos': pos})
            Renderer.camara.remove_obj(mob.sombra)
            mob.AI.reset()

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
        name = event.data['focus']
        data = abrir_json(Config.savedir + '/' + name + '.json')
        data.update(event.data)
        guardar_json(Config.savedir + '/' + name + '.json', data)

    @classmethod
    def new_game(cls, char_name):
        guardar_json(Config.savedir + '/' + char_name + '.json', {"focus": char_name})
        EventDispatcher.trigger('NewGame', 'engine', {'savegame': {"focus": char_name}})

    @classmethod
    def load_savefile(cls, filename):
        data = abrir_json(Config.savedir + '/' + filename)
        cls.save_data.update(data)
        cls.transient_mobs = data.get('transient', {})
        Mob_Group.clear()
        EventDispatcher.trigger('NewGame', 'engine', {'savegame': data})

    @classmethod
    def cargar_juego(cls, event):
        from engine.mapa.loader import load_mobs
        data = event.data
        cls.acceso_menues.clear()

        map_data = abrir_json(ModData.mapas + data['mapa'] + '.stage.json')
        Sun.init(map_data['latitude'])
        if not Tiempo.clock.is_real():
            Tiempo.set_time(*data['tiempo'])
        Sun.set_mod(*SeasonalYear.cargar_timestamps())
        stage = cls.setear_mapa(data['mapa'], data['entrada'], is_new_game=True)

        focus = Mob_Group[data['focus']]
        if type(focus) is str:
            if focus not in stage.mapa.datos['mobs']:
                datos = {'mobs': {focus: [data['entrada']]}}
                datos.update({'entradas': stage.data['entradas']})
                datos.update({'refs': {focus: ModData.fd_player + focus + '.json'}})
                focus, grupo = load_mobs(datos)[0]

                obj = stage.mapa.add_property(focus, grupo)
                obj.set_parent_map(stage.mapa)
            else:
                focus = stage.mapa.get_property(focus)

        for item in cls.transient_mobs.get(stage.nombre, []):
            mob_name = item['mob']
            x, y = cls.mapas[stage].posicion_entrada(item['pos'])
            datos = {'mobs': {mob_name: [[x, y]]}}
            datos.update({'entradas': stage.data['entradas']})
            item, grupo = load_mobs(datos)[0]

            obj = stage.mapa.add_property(item, grupo)
            obj.set_parent_map(stage.mapa)

        Renderer.set_focus(focus)
        cls.check_focus_position(focus, stage, data['entrada'])
        focus.character_name = data['focus']

    @classmethod
    def save_transient_npcs(cls, event):
        # transient NPCS porque el focus pasa por otro lado.
        transient = {}
        for stage in cls.transient_mobs:
            transient[stage] = [i['mob'].nombre for i in cls.transient_mobs[stage]]
        EventDispatcher.trigger(event.tipo + 'Data', 'Engine', {'transient': transient})

    @classmethod
    def check_focus_position(cls, focus, mapa, entrada):
        fx, fy = focus.mapRect.center
        ex, ey = mapa.data['entradas'][entrada]['pos']
        if fx != ex or fy != ey:
            texto = 'Error\nEl foco de la cámara no está en el centro. Verificar que la posición inicial\ndel foco '
            texto += f'en el chunk ({fx},{fy}) sea la  misma que la posición de la entrada \n({ex},{ey}).'
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

        if titulo not in cls.MENUS:
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
        ruta = path.join(getcwd(), ModData.fd_player)
        if final:
            name = cls.character['nombre']
            if not path.exists(ruta):
                mkdir(ruta)
            guardar_json(path.join(ruta, name + '.json'), cls.character)
            cls.new_game(name)


EngineData.init()

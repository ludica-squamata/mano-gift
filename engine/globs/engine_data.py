from engine.misc import abrir_json, guardar_json, salir_handler, Config
from .constantes import CAPA_OVERLAYS_MENUS
from .event_dispatcher import EventDispatcher, AzoeEvent
from .game_groups import Mob_Group, Prop_Group
from .renderer import Renderer
from .tiempo import Tiempo, SeasonalYear
from .mod_data import ModData
from os import path, mkdir, getcwd
from .sun import Sun
from csv import DictWriter


class EngineData:
    mapas = {}
    acceso_menues = []
    MENUS = {}
    setKey = False
    save_data = {}
    character = {
        'AI': 'controllable'
    }
    transient_mobs = []
    _concreted_trades = []

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
            (cls.create_character, 'CharacterCreation'),
            (cls.remove_from_transient, 'MobDeath')
        )

    @classmethod
    def setear_mapa(cls, stage, entrada, named_npcs=None, mob=None, is_new_game=False, use_csv=False):
        from engine.mapa import Stage, loader
        if stage not in cls.mapas or is_new_game:
            cls.mapas[stage] = Stage(cls, stage, mob, entrada, named_npcs, use_csv=use_csv)
        else:
            cls.mapas[stage].ubicar_en_entrada(mob, entrada)

        chunk = None
        if mob is not None:
            adress = cls.mapas[stage].entradas[entrada]
            chunk = cls.mapas[stage].get_chunk_by_adress(adress)
            chunk.add_property(mob, 2)
            mob.set_parent_map(chunk)

        for entry in cls.transient_mobs:
            tr_mob = Mob_Group[entry['id']]
            if tr_mob is None and entry['to'] == stage:
                pos = cls.mapas[stage].entradas[entry['pos']]
                all_data = {'mobs': {entry['mob']: [entry['pos']]},
                            'entradas': {entry['pos']: {'pos': pos}}, 'refs': {}}
                tr_mob = loader.load_mobs(chunk, all_data)[0][0]

            if entry['from'] in cls.mapas:
                cls.mapas[entry['from']].search_and_delete(tr_mob)
                entry['flagged'] = True

            if entry['to'] == stage:
                type_entrada = type(entry['pos'])  # shortcut
                x, y = cls.mapas[stage].posicion_entrada(entry['pos']) if type_entrada is str else entry['pos']
                dx, dy = tr_mob.direcciones[tr_mob.direccion]
                dx *= 32
                dy *= 32
                tr_mob.ubicar_en_mapa(x + dx, y + dy)
                if type(tr_mob) is not str:
                    adress = cls.mapas[stage].entradas[entry['pos']]
                    chunk = cls.mapas[stage].get_chunk_by_adress(adress)
                    chunk.add_property(tr_mob, 2)
                    tr_mob.set_parent_map(chunk)
                    tr_mob.id = entry['id']

        return cls.mapas[stage]

    @classmethod
    def delete_flagged_entries(cls):
        flagged = [i for i in cls.transient_mobs if i['flagged']]
        for each in flagged:
            cls.transient_mobs.remove(each)

    @classmethod
    def on_cambiarmapa(cls, evento):
        mapa_actual = Renderer.camara.focus.parent
        mob = evento.data['mob']
        mapa_actual.del_property(mob)
        stage = evento.data['target_stage']
        entrada = evento.data['target_entrada']

        if Renderer.camara.is_focus(mob):
            Renderer.camara.clear()
            mapa = cls.setear_mapa(stage, entrada, mob=mob)
            SeasonalYear.propagate()
            x, y = mapa.posicion_entrada(entrada)
            adress = mapa.entradas[entrada]
            Renderer.camara.set_background(mapa.chunks[adress])
            Renderer.set_focus(mob)
            Renderer.camara.focus.ubicar_en_mapa(x, y)
        else:
            item = {'name': mob.nombre, 'id': mob.id, 'pos': entrada, 'from': mapa_actual.parent.nombre, "to": stage}
            cls.transient_mobs.append(item)
            Renderer.camara.remove_obj(mob.sombra)
            mob['AI'].reset()

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
        cls.record_transactions()

    @classmethod
    def new_game(cls, char_name):
        guardar_json(Config.savedir + '/' + char_name + '.json', {"focus": char_name})
        EventDispatcher.trigger('NewGame', 'engine', {'savegame': {"focus": char_name}})

    @classmethod
    def load_savefile(cls, file):
        if type(file) is str:
            data = abrir_json(Config.savedir + '/' + file)
        elif type(file) is dict:
            data = file
        else:
            raise TypeError(f'"file" must be str or dict, not {type(file)}')

        cls.save_data.update(data)
        cls.transient_mobs = data.get('transient', [])
        Mob_Group.clear()
        Prop_Group.clear()
        EventDispatcher.trigger('NewGame', 'engine', {'savegame': data})

    @classmethod
    def cargar_juego(cls, event):
        from engine.mapa.loader import load_mobs
        data = event.data
        use_csv = data.get('use_csv', False)
        cls.acceso_menues.clear()

        map_data = abrir_json(ModData.mapas + data['mapa'] + '.stage.json')
        # Sun.init(map_data['latitude'])
        if not Tiempo.clock.is_real():
            Tiempo.set_time(*data['tiempo'])
        # Sun.set_mod(*SeasonalYear.cargar_timestamps())

        ids = [e['id'] for e in cls.transient_mobs]
        names = [e['name'] for e in cls.transient_mobs]
        named_npcs = [ids, names]

        if data['mapa'] in cls.mapas:
            cls.mapas[data['mapa']].delete_everything()
            cls.mapas.clear()
        stage = cls.setear_mapa(data['mapa'], data['entrada'], named_npcs, is_new_game=True, use_csv=use_csv)
        SeasonalYear.propagate()

        focus = stage.get_entitiy_from_my_chunks(data['focus'])
        exists = stage.exists_within_my_chunks(data['focus'], 'mobs')
        if focus is None or not exists:
            adress = map_data['entradas'][data['entrada']]['adress']
            mapa = stage.get_chunk_by_adress(adress)
            datos = {'mobs': {data['focus']: [data['entrada']]}, 'focus': True}
            datos.update({'entradas': stage.data['entradas']})
            datos.update({'refs': {data['focus']: ModData.fd_player + data['focus'] + '.json'}})
            focus, grupo = load_mobs(mapa, datos)[0]

            mapa.add_property(focus, grupo)

        Renderer.set_focus(focus)
        Sun.update()

    @classmethod
    def save_transient_npcs(cls, event):
        # transient NPCS porque el focus pasa por otro lado.
        transient = []
        for entry in cls.transient_mobs:
            entry.update({'mob': str(entry['name'])})
            transient.append(entry)

        EventDispatcher.trigger(event.tipo + 'Data', 'Engine', {'transient': transient})

    @classmethod
    def extend_trades(cls, new):
        cls._concreted_trades.extend(new)

    @classmethod
    def record_transactions(cls):
        ruta = path.join(Config.savedir, 'trading_list.csv')
        with open(ruta, 'at', encoding='utf-8', newline='') as csv_file:
            field_names = ['trader', 'item', 'cant', 'desde']
            writer = DictWriter(csv_file, fieldnames=field_names, delimiter=';', lineterminator='\r\n')
            for transaction in cls._concreted_trades:
                row = {
                    'trader': transaction['trader'], 'item': transaction['item'],
                    'cant': transaction['delta'], 'desde': transaction['tiempo']
                }
                writer.writerow(row)

    @classmethod
    def compound_save_data(cls, event):
        cls.save_data.update(event.data)
        if not EventDispatcher.is_quequed('SaveDataFile'):
            EventDispatcher.trigger('SaveDataFile', 'EngineData', cls.save_data)

    @classmethod
    def pop_menu(cls, event=None):
        from engine.UI.menues import default_menus

        kwargs = {}
        if event is None and not len(cls.acceso_menues):
            titulo = 'Pausa'
        elif event is not None:
            titulo = event.data.pop('value')
            kwargs = event.data
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
                menu = ModData.custommenus[name](cls, **kwargs)
            elif name in default_menus:
                menu = default_menus[name](cls, **kwargs)
            else:
                raise NotImplementedError('El menu "{}" no existe'.format(titulo))
        else:
            menu = cls.MENUS[titulo]
            menu.reset(*kwargs)

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

    @classmethod
    def remove_from_transient(cls, event):
        mob = event.data['obj']
        for entry in cls.transient_mobs:
            if entry['id'] == mob.id:
                entry['flagged'] = True


EngineData.init()

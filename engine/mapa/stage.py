from .loader import load_something, cargar_salidas, NamedNPCs, load_chunks_csv, load_props_csv
from engine.globs.azoe_group import AzoeGroup, AzoeBaseSprite, ChunkGroup
from engine.globs import ModData, COLOR_COLISION, Noche, ANCHO, ALTO
from engine.globs.event_dispatcher import EventDispatcher
from engine.misc import abrir_json, cargar_imagen, Config
from engine.globs.renderer import Renderer
from engine.globs import Mob_Group, MobCSV
from pygame import mask
from os import path
import csv


class Stage:
    properties = None
    chunks = None
    data = None
    offset_x = ANCHO // 2  # camara.rect.centerx
    offset_y = ALTO // 2  # camara.rect.centery

    zoom_level = ''  # Afecta el paso del tiempo. Los valores pueden ser "world", "interior" y "local" (default).

    def __init__(self, parent, nombre, mob, info, npcs_with_id=None, use_csv=False):
        NamedNPCs.npcs_with_ids = npcs_with_id
        self.id = ModData.generate_id()
        self.parent = parent  # a Stage's parent is always EngineData
        self.chunks = ChunkGroup()
        self.interactives = []
        self.properties = AzoeGroup('Stage ' + nombre + ' Properties', self.id)
        self.nombre = nombre
        self.data = abrir_json(ModData.mapas + nombre + '.stage.json')
        dx, dy = 0, 0
        chunk_adress = None
        if type(info) == str:
            dx, dy = self.data['entradas'][info]['pos']
            chunk_name = self.data['entradas'][info]['chunk']
        elif type(info) == dict:
            chunk_name = info['chunk']
            chunk_adress = info['adress']
        else:
            raise NotImplementedError

        offx = self.offset_x - dx
        offy = self.offset_y - dy
        self.world_stage = self.data.get("world_stage", False)
        self.zoom_level = self.data.get('zoom_level', "local")

        self.special_adresses = {}
        for special_chunk_key in self.data.get('chunks', {}):
            special_chunk_data = self.data['chunks'][special_chunk_key]
            adress = tuple(special_chunk_data['adress'])
            self.special_adresses[adress] = [special_chunk_key, special_chunk_data]

        self.chunks_csv = {}
        if 'chunks_csv' in self.data:
            if self.data['chunks_csv'] in ModData.preloaded_chunk_csv:
                self.chunks_csv = ModData.preloaded_chunk_csv[self.data['chunks_csv']]
            else:
                self.chunks_csv = load_chunks_csv(self.data['chunks_csv'], silently=not self.world_stage)
            # self.chunks_csv[chunk_name].update({
            #     'mobs': {"hero": [[dx, dy]]},
            #     'refs': {},
            # })
        if "props_csv" in self.data:
            self.props_csv = load_props_csv(self.data['props_csv'])
        else:
            self.props_csv = {}

        # if ModData.use_latitude and 'latitude' in self.data:
        #     self.current_latitude = self.data['latitude']
        # else:
        #     self.current_latitude = 30
        # self.current_longitude = self.data.get('longitude', 30)

        self.unique_props = {}
        if 'props' in self.data:
            self.load_unique_props(self.data)

        mob_req = 'mobs' if use_csv is False else 'csv'

        if chunk_name in self.data.get('chunks', {}):
            singleton = self.data['chunks'][chunk_name]
            chunk = ChunkMap(self, chunk_name, offx, offy, mob, data=singleton, requested=[mob_req, 'props'])
        elif chunk_name in self.chunks_csv:
            singleton = self.chunks_csv[chunk_name]
            chunk = ChunkMap(self, chunk_name, offx, offy, mob, data=singleton, requested=[mob_req, 'props'])
        else:
            chunk = ChunkMap(self, chunk_name, offx, offy, trnsnt_mb=mob,
                             requested=[mob_req, 'props'], adress=chunk_adress)
            chunk.houses_focus = True
        self.chunks.add(chunk)

        self.entradas = {}
        for key in self.data['entradas']:
            adress = self.data['entradas'][key]['adress']
            self.entradas[key] = tuple(adress)

        EventDispatcher.register_many(
            (self.save_map, 'Save'),
            (self.del_interactive, 'DeleteItem')
        )

        self.points_of_interest = {}
        for datapoint in self.data.get('puntos_de_interes_para_la_IA', {}):
            chunk_name = datapoint['chunk']
            if chunk_name not in self.points_of_interest:
                self.points_of_interest[chunk_name] = {}
            self.points_of_interest[chunk_name][datapoint['point']['name']] = datapoint['point']['node']

    def save_map(self, event):
        # abreviaturas
        sprs = self.chunks.sprs
        ent = self.entradas

        chunk = [chunk for chunk in sprs() if chunk.houses_focus][0]  # some chunk houses the focus for sure
        keys = [key for key in ent if ent[key] == tuple(chunk.adress)]  # search for chunks with entradas

        if not len(keys):
            data = {'info': {'stage': self.nombre, 'adress': tuple(chunk.adress), 'chunk': chunk.nombre},
                    'use_csv': True}
        else:
            entrada = [key for key in self.entradas if self.entradas[key] == tuple(chunk.adress)]
            data = {'mapa': self.nombre, 'entrada': entrada, 'use_csv': True}

        EventDispatcher.trigger(event.tipo + 'Data', 'Mapa', data)

        ruta = path.join(Config.savedir, 'mobs.csv')
        fieldnames = ['name', 'x', 'y', 'id', 'chunk', 'adress']
        with open(ruta, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';', lineterminator='\n')
            for mob in Mob_Group.contents():
                chunk = mob.last_map
                if mob.nombre in MobCSV:
                    row = MobCSV[mob.nombre]

                    row['x'] = str(mob.rel_x)
                    row['y'] = str(mob.rel_y)
                    row['chunk'] = chunk.nombre
                    row['adress'] = str(chunk.adress)

                else:
                    row = {'name': mob.nombre, 'x': mob.rel_x, 'y': mob.rel_y, 'id': mob.id,
                           'chunk': chunk.nombre, 'adress': str(chunk.adress)}
                    MobCSV[mob.nombre] = row

                writer.writerow(row)

    def load_unique_props(self, all_data: dict):
        """Carga los props que se hallen definidos en el archivo json del stage.
        Estos props no se repiten como lo harían si fueran definidos en los chunks,
        pues si los chunks se repiten, los props definidos en ellos también lo harán.

        @param all_data: los datos del archivo json.
        """
        prop_data = all_data['props']
        for prop_name in prop_data:
            adress = tuple(prop_data[prop_name]['chunk'])
            if adress not in self.unique_props:
                self.unique_props[adress] = {'props': {}, 'refs': {}}
            self.unique_props[adress]['props'][prop_name] = prop_data[prop_name]['instances']
            if prop_name in all_data['refs']:
                self.unique_props[adress]['refs'][prop_name] = all_data['refs'][prop_name]

    def place_placeable_props(self, prop):
        grupo = prop.grupo
        self.add_property(prop, grupo)

    def add_property(self, obj, _layer):
        add_interactive = False
        if type(obj) is tuple:
            obj, add_interactive = obj
        self.properties.add(obj, layer=_layer)
        if add_interactive:
            self.interactives.append(obj)

    def del_property(self, obj):
        if obj in self.properties:
            self.properties.remove(obj)
        if obj in self.interactives:
            self.interactives.remove(obj)
        Renderer.camara.remove_obj(obj)

    def delete_everything(self):
        sprites = self.properties.sprites()
        for sprite in sprites:
            self.properties.remove(sprite)
        self.properties.empty()
        for chunk in self.chunks.sprs():
            chunk.delete_everything()
        self.chunks.clear()

    def posicion_entrada(self, entrada):
        return self.data['entradas'][entrada]['pos']

    def ubicar_en_entrada(self, mob, entrada):
        datos = self.data['entradas'][entrada]
        ax, ay = datos['adress']

        mapa = self.get_chunk_by_adress(mob.chunk_adresses[self.nombre])
        if self.is_this_adress_special(ax, ay):
            mapa.ubicar(-ax * 800, -ay * 800)
            mob.reubicar(-ax * 800, -ay * 800)
            name, chunk_data = self.get_special_adress_at(ax, ay)
            if type(chunk_data) is dict:
                new_mapa = ChunkMap(self, name, ax * 800, ay * 800, self.data['entradas'],
                                    data=chunk_data, requested=['props', 'mobs'], adress=[ax, ay])
                self.chunks.add(new_mapa)
                self.set_special_adress(ax, ay, new_mapa)

    def __repr__(self):
        return f"Stage {self.nombre} ({self.id})"

    def search_and_delete(self, item):
        folder = None
        if item in self.properties.sprites():
            folder = self.properties
        else:
            for chunk in self.chunks.sprs():
                if item in chunk.properties.sprites():
                    folder = chunk.properties
                    break

        if folder is not None and item in folder:
            folder.remove(item)

    def is_this_adress_special(self, x, y):
        return (x, y) in self.special_adresses

    def get_special_adress_at(self, x, y):
        if (x, y) in self.special_adresses:
            return self.special_adresses[x, y]

    def set_special_adress(self, x, y, mapa):
        if self.is_this_adress_special(x, y):
            self.special_adresses[x, y][1] = mapa

    def exists_within_my_chunks(self, entity: str, key: str):
        for chunk in self.chunks.sprs():
            test1 = key in chunk.datos
            test2 = test1 and entity in chunk.datos[key]
            return test2

    def chunk_where_it_exists(self, entity: str, key: str):
        for chunk in self.chunks.sprs():
            if entity in chunk.datos[key]:
                return chunk

    def get_entitiy_from_my_chunks(self, entity: str):
        for chunk in self.chunks.sprs():
            obj = chunk.get_property(entity)
            if obj is not None:
                return obj

    def get_chunk_by_adress(self, adress):
        return self.chunks[tuple(adress)]

    def del_interactive(self, event):
        obj = event.data['obj']
        if hasattr(obj, 'sombra') and obj.sombra is not None:
            self.del_property(obj.sombra)
        self.del_property(obj)


class ChunkMap(AzoeBaseSprite):
    tipo = 'chunk'
    limites = None
    properties = None
    interactives = None

    adress = None

    salidas = None  # las salidas ahora pertenecen a los chunks, porque la imagen de salidas
    mask_salidas = None  # se lee desde Cámara.chunk_actual
    imagen_salidas = None

    houses_focus = False

    def __init__(self, parent, nombre, off_x=0, off_y=0, trnsnt_mb=None, data=False, requested=None, adress=None):
        self.id = ModData.generate_id()
        self.properties = AzoeGroup('Chunk ' + nombre + ' properties', self.id)
        self.interactives = []

        if not data:
            data = abrir_json(ModData.mapas + nombre + '.' + self.tipo + '.json')

        self.datos = data.copy()
        self.limites = data['limites']
        if adress is not None:
            self.adress = ChunkAdress(self, *adress)
        elif 'adress' in data:
            self.adress = ChunkAdress(self, *data['adress'])
        else:
            self.adress = ChunkAdress(self, 0, 0)

        self.latitude = data.get('latitude', None)

        # these two only work if the hero has been already loaded in another map.
        if 'hero' in data.get('mobs', {}):
            name = Mob_Group.get_by_trait('occupation', 'hero')
            if name is not None:
                data['mobs'][name] = data['mobs'].pop('hero')
                data['refs'][name] = ModData.fd_player + name + '.json'
                data['focus'] = name
                if trnsnt_mb is not None and name == trnsnt_mb['nombre']:
                    del data['mobs'][trnsnt_mb['nombre']]

        if 'csv' in requested:
            # otherwise the Engine doesn't know who the focus is, and the Camera gets unfocused.
            name = Mob_Group.get_by_trait('occupation', 'hero')
            # though, this might be on purpose (AzoeRTS)
            if name is not None:
                data['focus'] = name

        if len(data.get('mobs', {})):
            for mob in Mob_Group.get_existing(data['mobs']):
                del data['mobs'][mob]

        image = cargar_imagen(ModData.graphs + data['fondo']) if type(data['fondo']) is str else data['fondo']
        # data['fondo'] might be preloaded
        rect = image.get_rect(topleft=(off_x, off_y))
        self.noche = Noche(self, rect)

        if data['colisiones'] is not None:
            cols = 'colisiones'  # abreviatura
            colisiones = cargar_imagen(ModData.graphs + data[cols]) if type(data[cols]) is str else data[cols]
            self.mask = mask.from_threshold(colisiones, COLOR_COLISION, (1, 1, 1, 255))
        else:
            self.mask = mask.Mask(rect.size)

        super().__init__(parent, nombre, image, rect)

        if tuple(self.adress) in self.parent.props_csv:
            datos = self.parent.props_csv[tuple(self.adress)]
            if not 'props' in data:
                data['props'] = {datos['nombre']: [datos['pos']]}
                data['refs'] = {datos['nombre']: datos['imagen']}
            else:
                data['props'].update({datos['nombre']: [datos['pos']]})
                data['refs'].update({datos['nombre']: datos['imagen']})

        if tuple(self.adress) in self.parent.unique_props:
            uniques = self.parent.unique_props[tuple(self.adress)]
            data.update(uniques)

        self.cargar_limites(data.get('limites', self.limites))
        if self.nombre in self.parent.data['entradas']:
            # a single chunk only needs to know the points of entry that lie within it, if any.
            data['entradas'] = {self.nombre: self.parent.data['entradas'][self.nombre]}

        for item, grupo in load_something(self, data, requested):
            self.add_property(item, grupo)

        salidas = [salida for salida in self.parent.data['salidas'] if salida['chunk_adress'] == self.adress]
        self.set_salidas(*cargar_salidas(self, salidas))

        EventDispatcher.register(self.del_interactive, 'DeleteItem')

    def set_salidas(self, sld, masc, img):
        self.salidas = sld
        self.imagen_salidas = img
        self.mask_salidas = masc

    def unset_salidas(self):
        self.salidas.clear()
        self.imagen_salidas = None
        self.mask_salidas = None

    @property
    def mascara_salidas(self):
        if self.mask_salidas is None:
            self.mask_salidas = mask.Mask(self.image.get_size())

        return self.mask_salidas

    def ubicar(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def add_property(self, obj, _layer):
        add_interactive = False
        if type(obj) is tuple:
            obj, add_interactive = obj
        if obj not in self.properties:
            self.properties.add(obj, layer=_layer)
        if add_interactive and obj not in self.interactives:
            self.interactives.append(obj)

        if Renderer.camara.is_focus(obj):
            self.houses_focus = True

    def del_property(self, obj, rem_renderer=True):
        if obj in self.properties:
            self.properties.remove(obj)
        if obj in self.interactives:
            self.interactives.remove(obj)

        if rem_renderer:
            Renderer.camara.remove_obj(obj)

        if Renderer.camara.is_focus(obj):
            self.houses_focus = False

    def delete_everything(self):
        sprites = self.properties.sprites()
        for sprite in sprites:
            self.properties.remove(sprite)
        self.properties.empty()

        if self.salidas is not None:
            for salida in self.salidas.values():
                Renderer.camara.remove_obj(salida.sprite)
            self.unset_salidas()

    def get_property(self, name):
        for obj in self.properties.sprs():
            if obj.nombre == name:
                return obj

    def del_interactive(self, event):
        obj = event.data['obj']
        if hasattr(obj, 'sombra') and obj.sombra is not None:
            self.del_property(obj.sombra)
        self.del_property(obj)

    def translate(self, key):
        if key == 'sup':
            return self.adress.top
        elif key == 'inf':
            return self.adress.bottom
        elif key == 'der':
            return self.adress.right
        elif key == 'izq':
            return self.adress.left

    def cargar_limites(self, limites):
        keys = [i for i in limites]
        for key in keys:
            adress = self.translate(key)
            value = self.limites[key]
            mapa = self.parent.chunks[adress]
            if mapa is not None:
                self.limites[adress] = mapa
            else:
                del self.limites[key]
                self.limites[adress] = value

    def checkear_adyacencia(self, clave: str):
        type_adyacente = type(self.limites.get(self.translate(clave), False))
        if type_adyacente is str or type_adyacente is ChunkMap:
            return self.cargar_mapa_adyacente(clave)
        else:
            return False

    def cargar_mapa_adyacente(self, ady: str):
        x, y, w, h = self.rect
        dy = y - h if ady == 'sup' else y + h if ady == 'inf' else y
        dx = x - w if ady == 'izq' else x + w if ady == 'der' else x

        ax, ay = self.translate(ady)
        adress = ax, ay
        if type(self.limites[adress]) is str:
            entradas = self.parent.data['entradas']
            if self.parent.is_this_adress_special(ax, ay):
                name, datos = self.parent.get_special_adress_at(ax, ay)
                mapa = ChunkMap(self.parent, name, dx, dy, entradas, data=datos,
                                requested=['csv', 'props'], adress=(ax, ay))
                self.parent.set_special_adress(ax, ay, mapa)
            elif self.limites[adress] in self.parent.chunks_csv:
                name = self.limites[adress]
                data = self.parent.chunks_csv[name]
                mapa = ChunkMap(self.parent, name, dx, dy, entradas, data=data, requested=['csv', 'props'])
            else:
                mapa = ChunkMap(self.parent, self.limites[adress], dx, dy, requested=['csv', 'props'], adress=(ax, ay))

            self.limites[adress] = mapa
            self.parent.chunks.add(mapa)
        else:
            mapa: ChunkMap = self.limites[adress]
            mapa.ubicar(dx, dy)

        return mapa

    def __repr__(self):
        return f"ChunkMap {self.nombre} ({self.id.split('-')[1]})"

    def __bool__(self):
        return True

    def __eq__(self, other):
        test_1 = self.id == other.id
        test_2 = self.adress.center == other.adress.center
        test_3 = self.nombre == other.nombre

        return all([test_1, test_2, test_3])

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.nombre, self.id, self.adress.center))


class ChunkAdress:
    x = 0
    y = 0

    def __init__(self, parent, x, y):
        self.parent = parent
        self.x = x
        self.y = y

    @property
    def center(self):
        return self.x, self.y

    @property
    def left(self):
        return self.x - 1, self.y

    @property
    def right(self):
        return self.x + 1, self.y

    @property
    def top(self):
        return self.x, self.y - 1

    @property
    def bottom(self):
        return self.x, self.y + 1

    def __str__(self):
        return f'{self.x},{self.y}'

    def __repr__(self):
        return f'{self.parent.nombre} @{self.x}, {self.y}'

    def __bool__(self):
        return False

    def __eq__(self, other):
        if len(other) == 2:
            a = self.x == other[0]
            b = self.y == other[1]
            return all([a, b])
        return False

    def __getitem__(self, item):
        if type(item) is int:
            if item == 0:
                return self.x
            elif item == 1:
                return self.y
            raise StopIteration()

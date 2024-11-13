from .loader import load_something, cargar_salidas, NamedNPCs, load_chunks_csv, load_props_csv
from engine.globs import Tiempo, TimeStamp, ModData, COLOR_COLISION, Noche, Sun, ANCHO, ALTO
from engine.globs.azoe_group import AzoeGroup, AzoeBaseSprite, ChunkGroup
from engine.globs.event_dispatcher import EventDispatcher
from engine.misc import abrir_json, cargar_imagen, Config
from engine.globs.renderer import Renderer
from engine.globs import Mob_Group
from pygame import mask
from math import ceil
from os import path
import csv


class Stage:
    properties = None
    chunks = None
    data = None
    offset_x = ANCHO // 2  # camara.rect.centerx
    offset_y = ALTO // 2  # camara.rect.centery
    mediodia = None  # porque no siempre es a las 12 en punto.
    amanece = None
    atardece = None
    anochece = None

    def __init__(self, parent, nombre, mob, entrada, npcs_with_id=None, use_csv=False):
        NamedNPCs.npcs_with_ids = npcs_with_id
        self.id = ModData.generate_id()
        self.parent = parent  # a Stage's parent is always EngineData
        self.chunks = ChunkGroup()
        self.interactives = []
        self.properties = AzoeGroup('Stage ' + nombre + ' Properties', self.id)
        self.nombre = nombre
        self.data = abrir_json(ModData.mapas + nombre + '.stage.json')
        dx, dy = self.data['entradas'][entrada]['pos']
        chunk_name = self.data['entradas'][entrada]['chunk']
        offx = self.offset_x - dx
        offy = self.offset_y - dy

        self.special_adresses = {}
        for special_chunk_key in self.data.get('chunks', {}):
            special_chunk_data = self.data['chunks'][special_chunk_key]
            adress = tuple(special_chunk_data['adress'])
            self.special_adresses[adress] = [special_chunk_key, special_chunk_data]

        self.chunks_csv = {}
        if 'chunks_csv' in self.data:
            self.chunks_csv = load_chunks_csv(self.data['chunks_csv'])
            self.chunks_csv[chunk_name].update({
                'mobs': {"hero": [[dx, dy]]},
                'refs': {},
            })
        if "props_csv" in self.data:
            self.props_csv = load_props_csv(self.data['props_csv'])
        else:
            self.props_csv = {}

        if ModData.use_latitude and 'latitude' in self.data:
            self.current_latitude = self.data['latitude']
        else:
            self.current_latitude = 30
        self.current_longitude = self.data.get('longitude', 30)

        mob_req = 'mobs' if use_csv is False else 'csv'

        if chunk_name in self.data.get('chunks', {}):
            singleton = self.data['chunks'][chunk_name]
            ChunkMap(self, chunk_name, offx, offy, mob, data=singleton, requested=[mob_req, 'props'])
        elif chunk_name in self.chunks_csv:
            singleton = self.chunks_csv[chunk_name]
            ChunkMap(self, chunk_name, offx, offy, mob, data=singleton, requested=[mob_req, 'props'])
        else:
            ChunkMap(self, chunk_name, offx, offy, mob, requested=[mob_req, 'props'])

        if 'props' in self.data:
            self.load_unique_props(self.data)

        self.entradas = {}
        for key in self.data['entradas']:
            adress = self.data['entradas'][key]['adress']
            self.entradas[key] = tuple(adress)

        self.entrada = entrada

        EventDispatcher.register_many(
            (self.cargar_timestamps, 'UpdateTime'),
            (self.save_map, 'Save'),
            (self.del_interactive, 'DeleteItem', 'MobDeath')
        )

        self.points_of_interest = {}
        for datapoint in self.data.get('puntos_de_interes_para_la_IA', {}):
            chunk_name = datapoint['chunk']
            if chunk_name not in self.points_of_interest:
                self.points_of_interest[chunk_name] = {}
            self.points_of_interest[chunk_name][datapoint['point']['name']] = datapoint['point']['node']

    def cargar_timestamps(self, event):
        horas_dia = event.data['new_daylenght']
        offset = ceil(12 - (horas_dia / 2))
        self.amanece = TimeStamp(offset + 1)
        self.mediodia = TimeStamp(offset + (horas_dia / 2))
        self.anochece = TimeStamp(offset + horas_dia)
        self.atardece = TimeStamp((float(self.mediodia) + float(self.anochece) + 1) / 2)

        Tiempo.update_alarms({self.atardece: 'atardece', self.anochece: 'anochece',
                              self.amanece: 'amanece', self.mediodia: 'mediodía'})

    def save_map(self, event):
        EventDispatcher.trigger(event.tipo + 'Data', 'Mapa', {'mapa': self.nombre, 'entrada': self.entrada,
                                                              'use_csv': True})  # hightlighted new key.
        ruta = path.join(Config.savedir, 'mobs.csv')
        with open(ruta, 'w', newline='') as csvfile:
            # this is not quite good yet, because it doesn't save the mobs from other stages (those that were already
            # explored), but it is a start.
            fieldnames = ['name', 'x', 'y', 'id', 'chunk', 'adress']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';', lineterminator='\n')
            for chunk in self.chunks.sprs():
                for mob in chunk.properties.get_sprites_from_layer(2):
                    row = {'name': mob.nombre, 'x': mob.rel_x, 'y': mob.rel_y, 'id': mob.id,
                           'chunk': chunk.nombre, 'adress': str(chunk.adress)}
                    writer.writerow(row)

    def load_unique_props(self, all_data: dict):
        """Carga los props que se hallen definidos en el archivo json del stage.
        Estos props no se repiten como lo harían si fueran definidos en los chunks,
        pues si los chunks se repiten, los props definidos en ellos también lo harán.

        @param all_data: los datos del archivo json.
        """
        prop_data = all_data['props']
        for key in prop_data:
            chunk = self.get_chunk_by_adress(prop_data[key]['chunk'])
            if chunk is not None:
                data = {'props': {key: prop_data[key]['instances']}}
                if key in all_data['refs']:
                    # esto es para que Stage pueda tener props que son solo imágenes
                    data.update({'refs': {key: all_data['refs'][key]}})
                for item, grupo in load_something(chunk, data, 'props'):
                    self.add_property(item, grupo)

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

    def set_coordinates(self, direccion):
        if direccion == 'arriba':
            self.current_latitude -= 1

        elif direccion == 'abajo':
            self.current_latitude += 1

        elif direccion == 'derecha':
            self.current_longitude += 1

        elif direccion == 'izquierda':
            self.current_longitude -= 1

        Sun.set_latitude(self.current_latitude)

    def __repr__(self):
        return "Stage " + self.nombre

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
            return entity in chunk.datos[key]

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

    def del_property(self, obj):
        if obj in self.properties:
            self.properties.remove(obj)
        if obj in self.interactives:
            self.interactives.remove(obj)
        Renderer.camara.remove_obj(obj)


class ChunkMap(AzoeBaseSprite):
    tipo = 'chunk'
    limites = None
    properties = None
    interactives = None

    adress = None

    salidas = None  # las salidas ahora pertenecen a los chunks, porque la imagen de salidas
    mask_salidas = None  # se lee desde Cámara.chunk_actual
    imagen_salidas = None

    def __init__(self, parent, nombre, off_x, off_y, trnsnt_mb=None, data=False, requested=None, adress=None):
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

        if 'hero' in data.get('mobs', {}):
            name = Mob_Group.character_name
            data['mobs'][name] = data['mobs'].pop('hero')
            data['refs'][name] = ModData.fd_player + name + '.json'
            data['focus'] = name
            if trnsnt_mb is not None and name == trnsnt_mb.character_name:
                del data['mobs'][trnsnt_mb.character_name]

        if 'csv' in requested:
            # otherwise the Engine doesn't know who is the focus, and the Camera gets unfocused.
            name = Mob_Group.character_name
            # though, this might be on purpose (AzoeRTS)
            data['focus'] = name

        if len(data.get('mobs', {})):
            for mob in Mob_Group.get_existing(data['mobs']):
                del data['mobs'][mob]

        image = cargar_imagen(ModData.graphs + data['fondo'])
        rect = image.get_rect(topleft=(off_x, off_y))
        self.noche = Noche(self, rect)

        if data['colisiones'] is not None:
            colisiones = cargar_imagen(ModData.graphs + data['colisiones'])
            self.mask = mask.from_threshold(colisiones, COLOR_COLISION, (1, 1, 1, 255))
        else:
            self.mask = mask.Mask(rect.size)

        super().__init__(parent, nombre, image, rect)
        self.parent.chunks.add(self)

        if tuple(self.adress) in self.parent.props_csv:
            datos = self.parent.props_csv[tuple(self.adress)]
            if not 'props' in data:
                data['props'] = {datos['nombre']: [datos['pos']]}
                data['refs'] = {datos['nombre']: datos['imagen']}
            else:
                data['props'].update({datos['nombre']: [datos['pos']]})
                data['refs'].update({datos['nombre']: datos['imagen']})

        for i, salida in enumerate(self.parent.data['salidas']):
            if salida['chunk_adress'] == self.adress:
                self.set_salidas(*cargar_salidas(self, i, salida))

        self.cargar_limites(data.get('limites', self.limites))
        data['entradas'] = self.parent.data['entradas']
        # if any([len(data[req]) > 0 for req in requested]):
        for item, grupo in load_something(self, data, requested):
            self.add_property(item, grupo)

        EventDispatcher.register(self.del_interactive, 'DeleteItem', 'MobDeath')

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
            return mask.Mask(self.image.get_size())
        else:
            return self.mask_salidas

    def ubicar(self, x, y):
        self.rect.x = x
        self.rect.y = y

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

        if self.salidas is not None:
            for salida in self.salidas:
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
                                requested=['props'], adress=(ax, ay))
                self.parent.set_special_adress(ax, ay, mapa)
            elif self.limites[adress] in self.parent.chunks_csv:
                name = self.limites[adress]
                data = self.parent.chunks_csv[name]
                mapa = ChunkMap(self.parent, name, dx, dy, entradas, data=data, requested=['props'])
            else:
                mapa = ChunkMap(self.parent, self.limites[adress], dx, dy, entradas,
                                requested=['props'], adress=(ax, ay))

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

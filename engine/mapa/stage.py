from engine.globs import Tiempo, TimeStamp, ModData, COLOR_COLISION, Noche, Sun, ANCHO, ALTO, GRUPO_ITEMS
from engine.globs.azoe_group import AzoeGroup, AzoeBaseSprite, ChunkGroup
from .loader import load_something, cargar_salidas, NamedNPCs
from engine.globs.event_dispatcher import EventDispatcher
from engine.misc import abrir_json, cargar_imagen
from engine.globs.renderer import Renderer
from engine.globs import Mob_Group
from pygame import mask, Rect
from math import ceil


class Stage:
    properties = None
    chunks = None
    mapa = None
    data = None
    offset_x = ANCHO // 2  # camara.rect.centerx
    offset_y = ALTO // 2  # camara.rect.centery
    mediodia = None  # porque no siempre es a las 12 en punto.
    amanece = None
    atardece = None
    anochece = None

    def __init__(self, nombre, mob, entrada, npcs_with_id=None):
        NamedNPCs.npcs_with_ids = npcs_with_id
        self.chunks = ChunkGroup()
        self.interactives = []
        self.properties = AzoeGroup('Stage ' + nombre + ' Properties')
        self.nombre = nombre
        self.data = abrir_json(ModData.mapas + nombre + '.stage.json')
        dx, dy = self.data['entradas'][entrada]['pos']
        chunk_name = self.data['entradas'][entrada]['chunk']
        offx = self.offset_x - dx
        offy = self.offset_y - dy
        entradas = self.data['entradas']

        self.special_adresses = {}
        for special_chunk_key in self.data.get('chunks', {}):
            special_chunk_data = self.data['chunks'][special_chunk_key]
            adress = tuple(special_chunk_data['adress'])
            self.special_adresses[adress] = [special_chunk_key, special_chunk_data]

        self.id = ModData.generate_id()

        if ModData.use_latitude and 'latitude' in self.data:
            self.current_latitude = self.data['latitude']
        else:
            self.current_latitude = 30
        self.current_longitude = self.data.get('longitude', 30)

        if chunk_name in self.data.get('chunks', {}):
            singleton = self.data['chunks'][chunk_name]
            chunk = ChunkMap(self, chunk_name, offx, offy, entradas, mob, data=singleton, requested=['mobs', 'props'])
        else:
            chunk = ChunkMap(self, chunk_name, offx, offy, entradas, mob, requested=['mobs', 'props'])

        self.chunks.add(chunk)
        self.mapa = self.chunks.sprs()[0]
        self.rect = self.mapa.rect.copy()

        if 'props' in self.data:
            self.load_unique_props(self.data)

        sld, masc, img = cargar_salidas(self.mapa, self.data)
        self.salidas = sld  # la lista de salidas, igual que siempre.
        self.mask_salidas = masc  # máscara de colisiones de salidas.
        self.img_salidas = img  # imagen de colores codificados.

        self.entrada = entrada

        EventDispatcher.register_many(
            (self.cargar_timestamps, 'UpdateTime'),
            (self.save_map, 'Save')
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
        EventDispatcher.trigger(event.tipo + 'Data', 'Mapa', {'mapa': self.nombre, 'entrada': self.entrada})

    def load_unique_props(self, alldata: dict):
        """Carga los props que se hallen definidos en el archivo json del stage.
        Estos props no se repiten como lo harían si fueran definidos en los chunks,
        pues si los chunks se repiten, los props definidos en ellos también lo harán.

        @param alldata: los datos del archivo json completo.
        """
        for item, grupo in load_something(self.id, alldata, 'props'):
            obj = self.add_property(item, grupo)
            obj.set_parent_map(self.mapa)

    @property
    def noche(self):
        # Para evitar un conflicto con las Luces.
        return self.mapa.noche

    def add_property(self, obj, _layer):
        add_interactive = False
        if type(obj) is tuple:
            obj, add_interactive = obj
        self.properties.add(obj, layer=_layer)
        if add_interactive:
            self.interactives.append(obj)
        return obj

    def posicion_entrada(self, entrada):
        return self.data['entradas'][entrada]['pos']

    def ubicar_en_entrada(self, entrada):
        dx, dy = self.posicion_entrada(entrada)
        datos = self.data['entradas'][entrada]
        ax, ay = datos['adress']

        if self.is_this_adress_special(ax, ay):

            self.mapa.rect.move_ip(-ax * 800, -ay * 800)

            name, chunk_data = self.get_special_adress_at(ax, ay)
            if type(chunk_data) is dict:
                self.mapa = ChunkMap(self, name, 0, 0, self.data['entradas'],
                                     data=chunk_data, requested=['props', 'mobs'], adress=[ax, ay])
            else:
                self.mapa = chunk_data

        x = self.offset_x - dx
        y = self.offset_y - dy
        self.mapa.ubicar(x, y)

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


class ChunkMap(AzoeBaseSprite):
    tipo = 'chunk'
    limites = None
    properties = None
    interactives = None

    adress = None

    def __init__(self, stage, nombre, off_x, off_y, entradas, trnsnt_mb=None, data=False, requested=None, adress=None):
        self.properties = AzoeGroup('Chunk ' + nombre + ' properties')
        self.interactives = []

        if not data:
            data = abrir_json(ModData.mapas + nombre + '.' + self.tipo + '.json')

        self.datos = data.copy()
        self.limites = data['limites']
        if adress is not None:
            self.adress = ChunkAdress(self, *adress)
        else:
            self.adress = ChunkAdress(self, 0, 0)

        data.update({'entradas': entradas})
        if 'hero' in data['mobs']:
            name = Mob_Group.character_name
            data['mobs'][name] = data['mobs'].pop('hero')
            data['refs'][name] = ModData.fd_player + name + '.json'
            if trnsnt_mb is not None and name == trnsnt_mb.character_name:
                del data['mobs'][trnsnt_mb.character_name]

        if len(data['mobs']):
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

        super().__init__(stage, nombre, image, rect)

        self.cargar_limites(data.get('limites', self.limites))
        self.id = ModData.generate_id()
        if any([len(data[req]) > 0 for req in requested]):
            for item, grupo in load_something(self.id, data, requested):
                obj = self.add_property(item, grupo)
                obj.set_parent_map(self)
                obj.set_current_chunk(self)

        EventDispatcher.register(self.del_interactive, 'DeleteItem', 'MobDeath')

    @property
    def mascara_salidas(self):
        return self.parent.mask_salidas

    @property
    def imagen_salidas(self):
        return self.parent.img_salidas

    @property
    def salidas(self):
        return self.parent.salidas

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
        return obj

    def del_property(self, obj):
        if obj in self.properties:
            self.properties.remove(obj)
        if obj in self.interactives:
            self.interactives.remove(obj)
        Renderer.camara.remove_obj(obj)

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
        if type(self.limites[self.translate(ady)]) is str:
            entradas = self.parent.data['entradas']
            if self.parent.is_this_adress_special(ax, ay):
                name, datos = self.parent.get_special_adress_at(ax, ay)
                mapa = ChunkMap(self.parent, name, dx, dy, entradas, data=datos,
                                requested=['props'], adress=(ax, ay))
                self.parent.set_special_adress(ax, ay, mapa)
            else:
                mapa = ChunkMap(self.parent, self.limites[self.translate(ady)], dx, dy, entradas,
                                requested=['props'], adress=(ax, ay))

            self.limites[self.translate(ady)] = mapa
            self.parent.chunks.add(mapa)
        else:
            mapa: ChunkMap = self.limites[self.translate(ady)]
            mapa.ubicar(dx, dy)

        return mapa

    def __repr__(self):
        return "ChunkMap " + self.nombre


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
        return f'{self.parent.nombre} @{self.x}, {self.y}'

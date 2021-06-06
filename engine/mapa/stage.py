from engine.globs import Tiempo, TimeStamp, ModData, COLOR_COLISION, Noche, Sun, ANCHO, ALTO
from engine.globs.azoe_group import AzoeGroup, AzoeBaseSprite
from engine.globs.event_dispatcher import EventDispatcher
from .loader import load_something, cargar_salidas
from engine.misc import abrir_json, cargar_imagen
from engine.globs.renderer import Renderer
from engine.globs import Mob_Group
from pygame import mask, Rect
from math import ceil


class Stage:
    properties = None
    chunks = None
    mapa = None
    data = {}
    offset_x = ANCHO // 2  # camara.rect.centerx
    offset_y = ALTO // 2  # camara.rect.centery
    mediodia = None  # porque no siempre es a las 12 en punto.
    amanece = None
    atardece = None
    anochece = None

    interactives = []

    def __init__(self, nombre, mob, entrada):
        self.chunks = AzoeGroup('Stage ' + nombre + ' chunks')
        self.interactives.clear()
        self.properties = AzoeGroup('Stage ' + nombre + ' Properties')
        self.nombre = nombre
        self.data = abrir_json(ModData.mapas + nombre + '.stage.json')
        dx, dy = self.data['entradas'][entrada]['pos']
        chunk_name = self.data['entradas'][entrada]['chunk']
        offx = self.offset_x - dx
        offy = self.offset_y - dy
        entradas = self.data['entradas']
        latitud = self.data['latitude']
        Sun.init(latitud)
        if chunk_name in self.data.get('chunks', {}):
            singleton = self.data['chunks'][chunk_name]
            chunk = ChunkMap(self, chunk_name, offx, offy, entradas, mob, data=singleton, requested=['mobs', 'props'])
        else:
            chunk = ChunkMap(self, chunk_name, offx, offy, entradas, mob, requested=['mobs', 'props'])

        self.chunks.add(chunk)
        self.mapa = self.chunks.sprs()[0]
        self.rect = self.mapa.rect.copy()

        if 'props' in self.data:
            self.load_unique_props(self.data, 0, 0)

        sld, masc, img = cargar_salidas(self.mapa, self.data, chunk.rect.size)
        self.salidas = sld  # la lista de salidas, igual que siempre.
        self.mask_salidas = masc  # máscara de colisiones de salidas.
        self.img_salidas = img  # imagen de colores codificados
        # estas tres propiedades, dado que se relacionan con las salidas,
        # pertenecen a Stage, pero como se usa el tamaño del Chunk, la
        # distinción es ambigua.

        self.entrada = entrada

        EventDispatcher.register_many(
            (self.cargar_timestamps, 'UpdateTime'),
            (self.save_map, 'Save')
        )

    def cargar_timestamps(self, event):
        horas_dia = event.data['new_daylenght']
        offset = ceil(12 - (horas_dia / 2))
        actual = Tiempo.clock.timestamp()
        self.amanece = TimeStamp(offset + 1)
        self.mediodia = TimeStamp(offset + (horas_dia / 2))
        self.anochece = TimeStamp(offset + horas_dia)
        self.atardece = TimeStamp((float(self.mediodia) + float(self.anochece) + 1) / 2)

        Tiempo.clock.alarms.update({self.atardece: 'atardece', self.anochece: 'anochece',
                                    self.amanece: 'amanece', self.mediodia: 'mediodía'})
        Noche.set_mod(actual, self.amanece, self.mediodia, self.atardece, self.anochece)
        Sun.calculate(actual, self.amanece, self.mediodia, self.atardece, self.anochece)

    def save_map(self, event):
        EventDispatcher.trigger(event.tipo + 'Data', 'Mapa', {'mapa': self.nombre, 'entrada': self.entrada})

    def load_unique_props(self, alldata: dict, dx: int, dy: int):
        """Carga los props que se hallen definidos en el archivo json del stage.
        Estos props no se repiten como lo harían si fueran definidos en los chunks,
        pues si los chunks se repiten, los props definidos en ellos también lo harán.

        @param alldata: los datos del archivo json completo.
        @param dx: el offset en x del stage
        @param dy: el offset en y del stage.
        """
        for item, grupo in load_something(alldata, 'props'):
            obj = self.add_property(item, grupo)
            obj.reubicar(-dx, -dy)
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

    def offseted_possition(self, entrada):
        dx, dy = self.posicion_entrada(entrada)
        x = self.offset_x - dx
        y = self.offset_y - dy
        return x, y

    def ubicar_en_entrada(self, entrada):
        x, y = self.offseted_possition(entrada)
        self.mapa.ubicar(x, y)

    def __repr__(self):
        return "Stage " + self.nombre


class ChunkMap(AzoeBaseSprite):
    tipo = 'chunk'
    limites = None
    properties = None
    interactives = None

    def __init__(self, stage, nombre, off_x, off_y, entradas, transient_mob=None, data=False, requested=None):
        self.properties = AzoeGroup('Chunk ' + nombre + ' properties')
        self.interactives = []

        if not data:
            data = abrir_json(ModData.mapas + nombre + '.' + self.tipo + '.json')

        self.limites = data['limites']

        data.update({'entradas': entradas})
        if 'hero' in data['mobs']:
            name = Mob_Group.character_name
            data['mobs'][name] = data['mobs'].pop('hero')
            data['refs'][name] = ModData.fd_player + name + '.json'
            if transient_mob is not None and name == transient_mob.character_name:
                del data['mobs'][transient_mob.character_name]

        if len(data['mobs']):
            for mob in Mob_Group.get_existing(data['mobs']):
                del data['mobs'][mob]

        if data['colisiones'] is not None:
            colisiones = cargar_imagen(ModData.graphs + data['colisiones'])
            self.mask = mask.from_threshold(colisiones, COLOR_COLISION, (1, 1, 1, 255))
        else:
            self.mask = mask.Mask(self.image.get_size())

        image = cargar_imagen(ModData.graphs + data['fondo'])
        rect = image.get_rect(topleft=(off_x, off_y))
        self.noche = Noche(self, rect)

        super().__init__(stage, nombre, image, rect)
        self.cargar_limites(data.get('limites', self.limites))

        if any([len(data[req]) > 0 for req in requested]):
            for item, grupo in load_something(data, requested):
                obj = self.add_property(item, grupo)
                obj.set_parent_map(self)

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

    def del_interactive(self, event):
        obj = event.data['obj']
        if hasattr(obj, 'sombra') and obj.sombra is not None:
            self.del_property(obj.sombra)
        self.del_property(obj)

    def cargar_limites(self, limites):
        for key in limites:
            x, y, w, h = self.rect
            dy = y - h if key == 'sup' else y + h if key == 'inf' else y
            dx = x - w if key == 'izq' else x + w if key == 'der' else x
            rect = Rect((dx, dy), self.rect.size)
            mapa = self.parent.chunks.get_spr_at(rect.center)
            if mapa is not None:
                self.limites[key.lower()] = mapa

    def checkear_adyacencia(self, clave: str):
        type_adyacente = type(self.limites.get(clave, False))
        if type_adyacente is str or type_adyacente is ChunkMap:
            return self.cargar_mapa_adyacente(clave)
        else:
            return False

    def cargar_mapa_adyacente(self, ady: str):
        x, y, w, h = self.rect
        dy = y - h if ady == 'sup' else y + h if ady == 'inf' else y
        dx = x - w if ady == 'izq' else x + w if ady == 'der' else x

        if type(self.limites[ady]) is str:
            entradas = self.parent.data['entradas']
            mapa = ChunkMap(self.parent, self.limites[ady], dx, dy, entradas, requested=['props'])
            self.limites[ady] = mapa
            self.parent.chunks.add(mapa)
        else:
            mapa: ChunkMap = self.limites[ady]
            mapa.ubicar(dx, dy)

        if ady == 'izq' or ady == 'der':
            self.parent.rect.inflate_ip(mapa.rect.w, 0)

        elif ady == 'sup' or ady == 'inf':
            self.parent.rect.inflate_ip(0, mapa.rect.h)

        return mapa

    def __repr__(self):
        return "ChunkMap " + self.nombre

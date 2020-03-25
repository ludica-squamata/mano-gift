from engine.globs import Tiempo, TimeStamp, ModData, COLOR_COLISION
from engine.globs.azoe_group import AzoeGroup, AzoeBaseSprite
from engine.globs.event_dispatcher import EventDispatcher
from .loader import load_something, cargar_salidas
from engine.misc import abrir_json, cargar_imagen
from engine.globs.renderer import Renderer
from pygame import mask, Rect, transform
from engine.globs import Mob_Group


class Stage:
    properties = None
    cuadrantes = []
    chunks = None
    mapa = None
    data = {}
    offset_x = 320  # camara.rect.centerx
    offset_y = 240  # camara.rect.centery
    amanece = None
    atardece = None
    anochece = None

    def __init__(self, nombre, entrada):
        self.chunks = AzoeGroup('Stage ' + nombre + ' chunks')
        self.cuadrantes.clear()
        self.nombre = nombre
        self.data = abrir_json(ModData.mapas + nombre + '.stage.json')
        dx, dy = self.data['entradas'][entrada]['pos']
        chunk_name = self.data['entradas'][entrada]['chunk']
        offx = self.offset_x - dx
        offy = self.offset_y - dy
        entradas = self.data['entradas']
        if chunk_name in self.data.get('chunks', {}):
            singleton = self.data['chunks'][chunk_name]
            chunk = ChunkMap(self, chunk_name, offx, offy, entradas, data=singleton, requested=['Mobs', 'Props'])
        else:
            chunk = ChunkMap(self, chunk_name, offx, offy, entradas, requested=['Mobs', 'Props'])

        self.chunks.add(chunk)
        self.mapa = self.chunks.sprites()[0]
        self.rect = self.mapa.rect.copy()
        Tiempo.crear_noche(self.rect.size)

        sld, masc, img = cargar_salidas(self.data, chunk.rect.size)
        self.salidas = sld  # la lista de salidas, igual que siempre.
        self.mask_salidas = masc  # máscara de colisiones de salidas.
        self.img_salidas = img  # imagen de colores codificados
        # estas tres propiedades, dado que se relacionan con las salidas,
        # pertenecen a Stage, pero como se usa el tamaño del Chunk, la
        # distinción es ambigua.

        self.entrada = entrada

        EventDispatcher.register(self.cargar_timestamps, 'UpdateTime')
        EventDispatcher.register(self.anochecer, 'HourFlag')
        EventDispatcher.register(self.save_map, 'Save')
        EventDispatcher.register(self.rotate_map, 'RotateEverything')

    def cargar_timestamps(self, event):
        horas_dia = event.data['new_max_time']
        offset = 12 - (horas_dia // 2)  # centra la duración del día a las 12:00
        self.amanece = TimeStamp(offset + 1)
        self.anochece = TimeStamp(horas_dia + offset)

    def anochecer(self, event=None):
        noche = Tiempo.noche
        if event is not None and self.data['ambiente'] == 'exterior':
            ts = event.data['hora']
            # aclararse y oscurecerse son flags de la noche que habilitan su update().
            if ts == self.amanece:
                noche.aclararse = True
            if ts == self.anochece:
                noche.oscurecerse = True

        elif self.data['ambiente'] == 'interior':
            noche.set_transparency(0)

        else:  # el ambiente es exterior, pero no hay evento.
            if self.amanece < Tiempo.clock.timestamp() < self.anochece:
                # mismo resultado, pero es porque es de día.
                noche.set_transparency(0)

    def save_map(self, event):
        EventDispatcher.trigger(event.tipo + 'Data', 'Mapa', {'mapa': self.nombre, 'link': self.entrada})

    def rotate_map(self, event):
        angle = event.data['angle']
        view = event.data['new_view']
        x, y = 0, 0

        for mapa in self.chunks:
            mapa.rotate(angle)

        for obj in self.properties:
            if view == 'north':
                x = obj.left
                y = obj.top
            elif view == 'east':
                x = obj.right
                y = obj.top
            elif view == 'south':
                x = obj.right
                y = obj.bottom
            elif view == 'west':
                x = obj.left
                y = obj.bottom

        EventDispatcher.trigger('RotateMobs', 'Stage', {'x': x, 'y': y})

    def posicion_entrada(self, entrada):
        return self.data['entradas'][entrada]['pos']

    def ubicar_en_entrada(self, entrada):
        dx, dy = self.data['entradas'][entrada]['pos']
        x = self.offset_x - dx
        y = self.offset_y - dy
        self.mapa.ubicar(x, y)

    def __repr__(self):
        return "Stage " + self.nombre


class ChunkMap(AzoeBaseSprite):
    tipo = 'chunk'
    limites = {'sup': None, 'inf': None, 'izq': None, 'der': None}
    properties = None
    interactives = []

    def __init__(self, stage, nombre, off_x, off_y, entradas, data=False, requested=None):
        self.properties = AzoeGroup('Chunk ' + nombre + ' properties')
        self.interactives.clear()
        self.limites = {'sup': None, 'inf': None, 'izq': None, 'der': None}

        if not data:
            data = abrir_json(ModData.mapas + nombre + '.' + self.tipo + '.json')

        data.update({'entradas': entradas})
        if 'hero' in data['mobs']:
            data['mobs'][Mob_Group.character_name] = data['mobs'].pop('hero')
        colisiones = cargar_imagen(data['colisiones'])
        self.mask = mask.from_threshold(colisiones, COLOR_COLISION, (1, 1, 1, 255))

        image = cargar_imagen(data['fondo'])
        rect = image.get_rect(topleft=(off_x, off_y))

        super().__init__(stage, nombre, image, rect)
        self.cargar_limites(data.get('limites', self.limites))

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
            rect = Rect(self._get_newmap_pos(key), self.rect.size)
            mapa = self.parent.chunks.get_sprites_at(rect.center)
            if not mapa:
                self.limites[key.lower()] = limites[key]
            else:
                self.limites[key.lower()] = mapa[0]

    def checkear_adyacencia(self, clave):
        type_adyacente = type(self.limites.get(clave, False))
        if type_adyacente is str or type_adyacente is ChunkMap:
            return self.cargar_mapa_adyacente(clave)
        else:
            return False

    def _get_newmap_pos(self, ady):
        w, h = self.rect.size
        dx, dy = self.rect.topleft

        ady = ady.lower()  # por si acaso.

        if ady == 'sup':
            dy -= h
        elif ady == 'inf':
            dy += h
        elif ady == 'izq':
            dx -= w
        elif ady == 'der':
            dx += w

        return dx, dy

    def cargar_mapa_adyacente(self, ady):
        dx, dy = self._get_newmap_pos(ady)

        if type(self.limites[ady]) is str:
            entradas = self.parent.data['entradas']
            mapa = ChunkMap(self.parent, self.limites[ady], dx, dy, entradas, requested=['Props'])
            self.limites[ady] = mapa
            self.parent.chunks.add(mapa)
        else:
            mapa = self.limites[ady]
            mapa.ubicar(dx, dy)

        if ady == 'izq' or ady == 'der':
            self.parent.rect.inflate_ip(mapa.rect.w, 0)

        elif ady == 'sup' or ady == 'inf':
            self.parent.rect.inflate_ip(0, mapa.rect.h)

        return mapa

    def rotate(self, angle):
        self.image = transform.rotate(self.image, angle)
        # falta rotar la posición de los sprites y de la capa de colisiones

    def __repr__(self):
        return "ChunkMap " + self.nombre

    def update(self):
        self.parent.anochecer()

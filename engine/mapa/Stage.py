from engine.globs import Tiempo, TimeStamp, ModData, GRUPO_ITEMS, COLOR_COLISION
from engine.globs.eventDispatcher import EventDispatcher
from engine.globs.renderer import Renderer
from engine.misc import abrir_json, cargar_imagen
from .LightSource import DayLight  # SpotLight
from .loader import load_everything, cargar_salidas
from .grilla import Grilla
from .cuadrante import Cuadrante
from pygame.sprite import Sprite
from engine.globs.azoegroup import AzoeGroup
from pygame import mask, Rect, transform


class Stage:
    properties = None
    interactives = []
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
        self.properties = AzoeGroup('Stage ' + nombre + ' properties')
        self.interactives.clear()
        self.cuadrantes.clear()
        self.nombre = nombre
        self.data = abrir_json(ModData.mapas + nombre + '.stage.json')
        dx, dy = self.data['entradas'][entrada]['pos']
        chunk_name = self.data['entradas'][entrada]['chunk']
        offx = self.offset_x - dx
        offy = self.offset_y - dy
        if chunk_name in self.data.get('chunks', {}):
            singleton = self.data['chunks'][chunk_name]
            chunk = ChunkMap(self, chunk_name, offx, offy, data=singleton)
        else:
            chunk = ChunkMap(self, chunk_name, offx, offy)

        self.chunks.add(chunk)
        self.mapa = self.chunks.sprites()[0]
        self.rect = self.mapa.rect.copy()
        self.crear_cuadrantes()
        self.cargar_timestamps()
        self.grilla = Grilla(self.mapa.mask, 32)
        self.salidas = cargar_salidas(self.data)
        self.entrada = entrada  # rollback for #147: save_map()

        EventDispatcher.register(self.anochecer, 'HourFlag')
        EventDispatcher.register(self.del_interactive, 'DeleteItem', 'MobDeath')
        EventDispatcher.register(self.save_map, 'Save')
        EventDispatcher.register(self.rotate_map, 'RotateEverything')

    def crear_cuadrantes(self):
        w = self.rect.w // 2
        h = self.rect.h // 2
        self.cuadrantes = [Cuadrante(x, y, w, h) for x in range(2) for y in range(2)]

    def register_at_renderer(self, mob=None):
        Renderer.camara.set_background(self.mapa)
        luz_del_sol = DayLight(1024)
        if Tiempo.noche is None:
            Tiempo.crear_noche(self.rect.size)
        if self.data['ambiente'] == 'exterior':
            Tiempo.noche.set_lights(luz_del_sol)
        # elif self.data['ambiente'] == 'interior':
        #     pass
        to_be_registered = self.properties.sprites()
        if mob is not None:
            to_be_registered.append(mob)

        for obj in to_be_registered:
            ''':type obj: _giftSprite'''
            if obj.stage is not self:
                obj.stage = self
                # obj.bottom = self.rect.h - obj.top
                # obj.right = self.rect.w - obj.left

            obj.sombra = None
            obj._prevLuces = None

            self.rect = self.mapa.rect.copy()
            x = self.rect.x + obj.mapRect.x
            y = self.rect.y + obj.mapRect.y
            obj.ubicar(x, y)

            if obj not in Renderer.camara.real:
                Renderer.camara.add_real(obj)

        # luz_del_sol.add_objs([obj for obj in self.properties if obj.proyectaSombra])

        for salida in self.salidas:
            if salida.sprite is not None:
                Renderer.camara.add_real(salida.sprite)

        for obj in self.properties:
            for quadrant in self.cuadrantes:
                if quadrant.contains(obj):
                    quadrant.add(obj)

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

    def cargar_timestamps(self):
        if self.data['ambiente'] == 'exterior':
            self.amanece = TimeStamp(*self.data["amanece"])
            self.atardece = TimeStamp(*self.data["atardece"])
            self.anochece = TimeStamp(*self.data["anochece"])

    def anochecer(self, event):
        """
        :param event:
        :type event:AzoeEvent
        :return:
        """
        hora = event.data['hora']
        if hora == self.amanece:
            print('amanecer')
        elif hora == self.atardece:
            print('atardecer')
        elif hora == self.anochece:
            print('anochecer')

        if self.data['ambiente'] == 'exterior':
            pass
        elif self.data['ambiente'] == 'interior':
            pass

    def del_interactive(self, event):
        obj = event.data['obj']
        if hasattr(obj, 'sombra') and obj.sombra is not None:
            self.del_property(obj.sombra)
        self.del_property(obj)

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

    def actualizar_grilla(self):
        self.grilla.update()
        for spr in self.properties.get_sprites_from_layer(GRUPO_ITEMS):
            if hasattr(spr, 'accion') and spr.accion == 'mover':
                x, y = spr.mapRect.x // 32, spr.mapRect.y // 32
                self.grilla.set_transitable((x, y), False)

    def posicion_entrada(self, entrada):
        return self.data['entradas'][entrada]['pos']

    def ubicar_en_entrada(self, entrada):
        dx, dy = self.data['entradas'][entrada]['pos']
        x = self.offset_x - dx
        y = self.offset_y - dy
        self.mapa.ubicar(x, y)

    def __repr__(self):
        return "Stage " + self.nombre + ' (' + str(len(self.properties.sprites())) + ' sprites)'

    def update(self):
        self.actualizar_grilla()
        for cuadrante in self.cuadrantes:
            cuadrante.update()
        for salida in self.salidas:
            salida.update()


class ChunkMap(Sprite):
    tipo = 'chunk'
    limites = {'sup': None, 'inf': None, 'izq': None, 'der': None}

    def __init__(self, stage, nombre, off_x, off_y, cargar_todo=True, data=False):
        super().__init__()
        self.limites = {'sup': None, 'inf': None, 'izq': None, 'der': None}
        self.stage = stage
        self.nombre = nombre
        # print(off_x,off_y)

        if not data:
            data = abrir_json(ModData.mapas + self.nombre + '.' + self.tipo + '.json')

        colisiones = cargar_imagen(data['colisiones'])
        self.image = cargar_imagen(data['fondo'])
        self.mask = mask.from_threshold(colisiones, COLOR_COLISION, (1, 1, 1, 255))
        self.rect = self.image.get_rect(topleft=(off_x, off_y))

        self.cargar_limites(data.get('limites', self.limites))

        if cargar_todo:
            # dx = -off_x + self.stage.offset_x
            # dy = -off_y + self.stage.offset_y
            for item, grupo in load_everything(data):  # , dx, dy):
                self.stage.add_property(item, grupo)

    def ubicar(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def cargar_limites(self, limites):

        for key in limites:
            rect = Rect(self._get_newmap_pos(key), self.rect.size)
            mapa = self.stage.chunks.get_sprites_at(rect.center)
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
            mapa = ChunkMap(self.stage, self.limites[ady], dx, dy, cargar_todo=False)
            self.limites[ady] = mapa
            self.stage.chunks.add(mapa)
        else:
            mapa = self.limites[ady]
            mapa.ubicar(dx, dy)

        if ady == 'izq' or ady == 'der':
            self.stage.rect.inflate_ip(mapa.rect.w, 0)

        elif ady == 'sup' or ady == 'inf':
            self.stage.rect.inflate_ip(0, mapa.rect.h)

        return mapa

    def rotate(self, angle):
        self.image = transform.rotate(self.image, angle)
        # falta rotar la posición de los sprites y de la capa de colisiones

    def __repr__(self):
        return "ChunkMap " + self.nombre

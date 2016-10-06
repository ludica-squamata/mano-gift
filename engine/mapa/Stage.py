from engine.globs import Tiempo, TimeStamp, ModData as Md, GRUPO_SALIDAS, GRUPO_ITEMS, COLOR_COLISION
from engine.globs.eventDispatcher import EventDispatcher
from engine.globs.renderer import Renderer
from engine.misc import Resources as Rs
from .LightSource import DayLight  # SpotLight
from .loader import Loader
from .grilla import Grilla
from .cuadrante import Cuadrante
from pygame.sprite import Sprite, LayeredUpdates
from pygame import mask, Rect, Surface


class Stage:
    properties = None
    interactives = []
    cuadrantes = []
    chunks = None
    mapa = None
    data = {}
    quest = None
    offset_x = 320  # camara.rect.centerx
    offset_y = 240  # camara.rect.centery
    amanece = None
    atardece = None
    anochece = None

    def __init__(self, nombre, entrada):
        self.chunks = LayeredUpdates()
        self.interactives.clear()
        self.nombre = nombre
        self.data = Rs.abrir_json(Md.mapas + nombre + '.json')
        dx, dy = self.data['entradas'][entrada]
        self.offset_x -= dx
        self.offset_y -= dy
        self.chunks.add(ChunkMap(self, self.data, self.nombre, self.offset_x, self.offset_y))
        self.mapa = self.chunks.sprites()[0]
        self.rect = self.mapa.rect.copy()
        self.crear_cuadrantes()
        self.grilla = Grilla(self.mapa.mask, 32)
        self.properties = LayeredUpdates()
        self.salidas = []
        self.entrada = entrada
        self.cargar_timestamps()
        Loader.set_stage(self)
        Loader.load_everything(entrada)

        EventDispatcher.register(self.anochecer, 'hora')
        EventDispatcher.register(self.del_interactive, 'DelItem', 'MobMuerto')

    def crear_cuadrantes(self):
        w = self.rect.w // 2
        h = self.rect.h // 2
        self.cuadrantes = [Cuadrante(x, y, w, h) for x in range(2) for y in range(2)]

    def register_at_renderer(self):
        Renderer.camara.set_background(self.mapa)
        luz_del_sol = DayLight(1024)
        if Tiempo.noche is None:
            Tiempo.crear_noche(self.rect.size)  # asumiendo que es uno solo...
        if self.data['ambiente'] == 'exterior':
            Tiempo.noche.set_lights(luz_del_sol)
        # elif self.data['ambiente'] == 'interior':
        #     pass 
        for obj in self.properties:
            ''':type obj: _giftSprite'''
            if obj.stage is not self:
                obj.stage = self
            obj.sombra = None
            obj._prevLuces = None

            x = self.rect.x + obj.mapX
            y = self.rect.y + obj.mapY
            obj.ubicar(x, y)

            if obj not in Renderer.camara.real:
                Renderer.camara.add_real(obj)

        luz_del_sol.add_objs([obj for obj in self.properties if obj.proyectaSombra])

        for salida in self.salidas:
            if salida.sprite is not None:
                Renderer.camara.add_real(salida.sprite)

        for obj in self.properties:
            for quadrant in self.cuadrantes:
                if quadrant.contains(obj):
                    quadrant.add(obj)

    def add_property(self, obj, _layer, add_interactive=False):
        if _layer == GRUPO_SALIDAS:
            self.salidas.append(obj)
        else:
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

    def actualizar_grilla(self):
        self.grilla.update()
        for spr in self.properties.get_sprites_from_layer(GRUPO_ITEMS):
            if hasattr(spr, 'accion') and spr.accion == 'mover':
                x, y = spr.mapX // 32, spr.mapY // 32
                self.grilla.set_transitable((x, y), False)

    def __repr__(self):
        return "Stage " + self.nombre + ' (' + str(len(self.properties.sprites())) + ' sprites)'

    def update(self):
        self.actualizar_grilla()
        for cuadrante in self.cuadrantes:
            cuadrante.update()
        for salida in self.salidas:
            salida.update()


class ChunkMap(Sprite):
    tipo = 'mapa'
    limites = {'sup': '', 'inf': '', 'izq': '', 'der': ''}

    def __init__(self, stage, data, nombre, off_x, off_y):
        super().__init__()
        self.limites = {'sup': '', 'inf': '', 'izq': '', 'der': ''}
        self.stage = stage
        self.nombre = nombre

        imagen = Rs.cargar_imagen(data['capa_background']['fondo'])
        colisiones = Rs.cargar_imagen(data['capa_background']['colisiones'])

        w, h = imagen.get_size()
        if w < 800 or h < 800:
            img = Surface((800, 800))
            col = img.copy()
            col.fill(COLOR_COLISION)

            _rect = img.get_rect()
            topleft = imagen.get_rect(center=_rect.center)

            img.blit(imagen, topleft)
            col.blit(colisiones, topleft)
        else:
            img = imagen
            col = colisiones

        self.image = img
        self.mask = mask.from_threshold(col, COLOR_COLISION, (1, 1, 1, 255))
        self.rect = img.get_rect(topleft=(off_x, off_y))

        self.cargar_limites(data.get('limites', self.limites))

    def __repr__(self):
        return "ChunkMap " + self.nombre

    def ubicar(self, x, y):
        """Coloca al sprite en pantalla
        :param y: int
        :param x: int
        """
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
        if type(self.limites.get(clave, None)) is not ChunkMap:
            return self.cargar_mapa_adyacente(clave)

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

        nmbr = self.limites[ady]

        try:
            data = Rs.abrir_json(Md.mapas + nmbr + '.json')

            dx, dy = self._get_newmap_pos(ady)

            mapa = ChunkMap(self.stage, data, nmbr, dx, dy)

            self.limites[ady] = mapa
            self.stage.chunks.add(mapa)

            if ady == 'izq' or ady == 'der':
                self.stage.rect.inflate_ip(mapa.rect.w, 0)
                if ady == 'izq':
                    for spr in self.stage.properties:
                        spr.stageX += mapa.rect.w
            elif ady == 'sup' or ady == 'inf':
                self.stage.rect.inflate_ip(0, mapa.rect.h)
                if ady == 'sup':
                    for spr in self.stage.properties:
                        spr.stageY += mapa.rect.h

            return mapa
        except IOError:
            pass

        return False

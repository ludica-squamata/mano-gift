from engine.globs import Constants as Cs, Tiempo, TimeStamp
from engine.globs import ModData as Md, EngineData as Ed
from engine.mobs.scripts.a_star import generar_grilla
from pygame.sprite import Sprite, LayeredUpdates
from engine.misc import Resources as r
from .loader import Loader
from .LightSource import DayLight  # SpotLight
from pygame import mask


class Stage:
    properties = None
    interactives = []
    chunks = None
    mapa = None
    data = {}
    quest = None
    offset_x = 320  # camara.rect.centerx
    offset_y = 240  # camara.rect.centery

    def __init__(self, nombre, mobs_data, entrada):
        self.chunks = LayeredUpdates()
        self.nombre = nombre
        self.data = r.abrir_json(Md.mapas + nombre + '.json')
        dx, dy = self.data['entradas'][entrada]
        self.offset_x -= dx
        self.offset_y -= dy
        self.chunks.add(ChunkMap(self, self.data, nombre = self.nombre, off_x = self.offset_x, off_y = self.offset_y))
        self.mapa = self.chunks.sprites()[0]
        self.rect = self.mapa.rect.copy()
        self.grilla = generar_grilla(self.mapa.mask, self.mapa.image)
        self.properties = LayeredUpdates()
        self.salidas = []
        self.cargar_timestamps()
        Loader.set_stage(self)
        Loader.load_everything(entrada, mobs_data)

    def register_at_renderer(self):
        Ed.RENDERER.camara.set_background(self.mapa)
        Tiempo.crear_noche(self.rect.size)  # asumiendo que es uno solo...
        Tiempo.noche.set_lights(DayLight(1024))
        self.add_property(Tiempo.noche, Cs.CAPA_TOP_CIELO)
        for obj in self.properties:
            ''':type obj: _giftSprite'''
            obj.stage = self

            x = self.rect.x + obj.mapX
            y = self.rect.y + obj.mapY
            obj.ubicar(x, y, self.offset_y)

            Ed.RENDERER.camara.add_real(obj)

    def add_property(self, obj, _layer, add_interactive = False):
        if _layer == Cs.CAPA_GROUND_SALIDAS:
            self.salidas.append(obj)
        else:
            self.properties.add(obj, layer = _layer)
            if add_interactive:
                self.interactives.append(obj)

    def del_property(self, obj):
        if obj in self.properties:
            self.properties.remove(obj)
        if obj in self.interactives:
            self.interactives.remove(obj)
        Ed.RENDERER.camara.remove_obj(obj)

    def cargar_timestamps(self):
        if self.data['ambiente'] == 'exterior':
            self.amanece = TimeStamp(*self.data["amanece"])
            self.atardece = TimeStamp(*self.data["atardece"])
            self.anochece = TimeStamp(*self.data["anochece"])

    def anochecer(self, event):
        """
        :param event:
        :type event:GiftEvent
        :return:
        """
        print(event)
        if self.data['ambiente'] == 'exterior':
            pass
        elif self.data['ambiente'] == 'interior':
            pass

    def actualizar_grilla(self):
        for spr in self.properties.get_sprites_from_layer(Cs.CAPA_GROUND_ITEMS):
            if spr.solido:  # and not spr.es('empujable'):
                x = int(spr.mapX / 32)
                y = int(spr.mapY / 32)
                self.grilla[x, y].transitable = False

    def __repr__(self):
        return "Stage " + self.nombre + ' (' + str(len(self.properties.sprites())) + ' sprites)'


class ChunkMap(Sprite):
    tipo = 'mapa'
    offsetX = 0
    offsetY = 0
    limites = {'sup': '', 'supizq': '', 'supder': '',
               'inf': '', 'infizq': '', 'infder': '',
               'izq': '', 'der': ''}

    def __init__(self, stage, data, nombre = '', off_x = 0, off_y = 0):
        super().__init__()
        self.limites = {'sup': '', 'supizq': '', 'supder': '',
                        'inf': '', 'infizq': '', 'infder': '',
                        'izq': '', 'der': ''}
        self.stage = stage
        self.nombre = nombre
        self.cargar_limites(data['limites'])
        self.image = r.cargar_imagen(data['capa_background']['fondo'])
        self.rect = self.image.get_rect(topleft = (off_x, off_y))
        self.mask = mask.from_threshold(r.cargar_imagen(data['capa_background']['colisiones']), Cs.COLOR_COLISION,
                                        (1, 1, 1, 255))

    def __repr__(self):
        return "ChunkMap " + self.nombre

    def ubicar(self, x, y):
        """Coloca al sprite en pantalla"""
        self.rect.x = x
        self.rect.y = y

    def cargar_limites(self, limites):
        for key in limites:
            self.limites[key.lower()] = limites[key]

    def checkear_adyacencia(self, clave):
        if type(self.limites.get(clave, None)) is not ChunkMap:
            return self.cargar_mapa_adyacente(clave)

    def cargar_mapa_adyacente(self, ady):

        nmbr = self.limites[ady]

        try:
            data = r.abrir_json(Md.mapas + nmbr + '.json')

            w, h = self.rect.size
            dx, dy = self.rect.topleft

            if ady == 'sup':
                dy -= h +1
            elif ady == 'inf':
                dy += h -1
            elif ady == 'izq':
                dx -= w +1
            elif ady == 'der':
                dx += w -1

            mapa = ChunkMap(self.stage, data,  nombre = nmbr, off_x = dx, off_y = dy)

            self.limites[ady] = mapa
            self.stage.chunks.add(mapa)
            self.stage.rect.union_ip(mapa.rect)
            return mapa
        except IOError:
            pass

        return False

    def update(self):
        # self.stage.anochecer()
        self.stage.actualizar_grilla()

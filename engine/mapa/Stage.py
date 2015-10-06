from engine.globs import Constants as Cs, Tiempo, timestamp
from engine.globs import ModData as Md, EngineData as Ed
from engine.mobs.scripts.a_star import generar_grilla
from pygame.sprite import Sprite, LayeredUpdates
from engine.misc import Resources as Rs
from .loader import MapDataLoader
from .LightSource import DayLight  # SpotLight
from pygame import mask


class Stage:
    properties = None
    interactives = []
    mapa = None
    limites = {'sup': '', 'supizq': '', 'supder': '',
               'inf': '', 'infizq': '', 'infder': '',
               'izq': '', 'der': ''}
    anochece = None
    atardece = None
    amanece = None

    data = {}
    quest = None

    def __init__(self, nombre, mobs_data, entrada):
        self.nombre = nombre
        self.data = Rs.abrir_json(Md.mapas + nombre + '.json')
        self.mapa = ChunkMap(self, self.data, nombre)  # por ahora es uno solo.
        self.rect = self.mapa.rect.copy()
        self.grilla = generar_grilla(self.mapa.mask, self.mapa.image)
        self.properties = LayeredUpdates()
        self.salidas = []  # aunque en realidad, las salidas deberian ser del chunk, o no?
        self.cargar_timestamps()
        MapDataLoader.set_stage(self)
        MapDataLoader.load_everything(entrada, mobs_data)

    def register_at_renderer(self, entrada):
        Ed.RENDERER.camara.set_background(self.mapa)
        Tiempo.crear_noche(self.rect.size)  # asumiendo que es uno solo...
        Tiempo.noche.set_lights(DayLight(1024))
        self.add_property(Tiempo.noche, Cs.CAPA_TOP_CIELO)
        for obj in self.properties:
            ''':type obj: GiftSprite'''
            obj.stage = self
            Ed.RENDERER.camara.add_real(obj)

        Ed.HERO.ubicar(*self.data['entradas'][entrada])

    def add_property(self, obj, _layer, is_interactive = False):
        if _layer == Cs.CAPA_GROUND_SALIDAS:
            self.salidas.append(obj)
        else:
            self.properties.add(obj, layer = _layer)
            if is_interactive:
                self.interactives.append(obj)

    def del_property(self, obj):
        if obj in self.properties:
            self.properties.remove(obj)
        if obj in self.interactives:
            self.interactives.remove(obj)
        Ed.RENDERER.camara.remove_obj(obj)

    def cargar_mapa_adyacente(self, ady):
        x, y = 0, 0
        if self.limites[ady] != '':
            nombre = self.limites[ady]
            data = Rs.abrir_json(Md.mapas + self.limites[ady] + '.json')

            w, h = self.mapa.rect.size
            if ady == 'sup':
                x, y = 0, -h
            elif ady == 'supizq':
                x, y = -w, -h
            elif ady == 'supder':
                x, y = w, -h
            elif ady == 'inf':
                x, y = 0, h
            elif ady == 'infizq':
                x, y = -w, h
            elif ady == 'infder':
                x, y = w, h
            elif ady == 'izq':
                x, y = -w, 0
            elif ady == 'der':
                x, y = w, 0

            mapa = ChunkMap(self, data, nombre, x, y)

            self.limites[ady] = mapa
            Ed.RENDERER.camara.set_background(mapa)
            self.rect.union_ip(mapa.rect)
            return True
        return False

    def cargar_timestamps(self):
        if self.data['ambiente'] == 'exterior':
            self.amanece = timestamp(*self.data["amanece"])
            self.atardece = timestamp(*self.data["atardece"])
            self.anochece = timestamp(*self.data["anochece"])

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
    # chunkmap: la idea es tener 9 de estos al mismo tiempo.
    tipo = 'mapa'
    offsetX = 0
    offsetY = 0

    def __init__(self, stage, data, nombre = '', off_x = 0, off_y = 0):
        super().__init__()
        self.stage = stage
        self.nombre = nombre
        self.image = Rs.cargar_imagen(data['capa_background']['fondo'])
        self.rect = self.image.get_rect(topleft = (off_x, off_y))
        self.mask = mask.from_threshold(Rs.cargar_imagen(data['capa_background']['colisiones']), Cs.COLOR_COLISION,
                                        (1, 1, 1, 255))
        self.offsetX = off_x
        self.offsetY = off_y

    def __repr__(self):
        return "ChunkMap " + self.nombre

    def ubicar(self, x, y):
        """Coloca al sprite en pantalla"""
        self.rect.x = x
        self.rect.y = y

    def update(self):
        # self.stage.anochecer()
        self.stage.actualizar_grilla()

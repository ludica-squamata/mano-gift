from engine.globs import Constants as Cs, Tiempo, TimeStamp
from engine.globs import ModData as Md, EngineData as Ed
from engine.mobs.scripts.a_star import generar_grilla
from pygame.sprite import Sprite, LayeredUpdates
from engine.misc import Resources as Rs
from .loader import Loader
from .LightSource import DayLight  # SpotLight
from pygame import mask, Rect


class Stage:
    properties = None
    interactives = []
    chunks = None
    mapa = None
    data = {}
    quest = None
    offset_x = 320  # camara.rect.centerx
    offset_y = 240  # camara.rect.centery
    amanece = None
    atardece = None
    anochece = None

    def __init__(self, nombre, mobs_data, entrada):
        self.chunks = LayeredUpdates()
        self.nombre = nombre
        self.data = Rs.abrir_json(Md.mapas + nombre + '.json')
        dx, dy = self.data['entradas'][entrada]
        self.offset_x -= dx
        self.offset_y -= dy
        self.chunks.add(ChunkMap(self, self.data, self.nombre, self.offset_x, self.offset_y))
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

    def update(self):
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

        self.image = Rs.cargar_imagen(data['capa_background']['fondo'])
        self.rect = self.image.get_rect(topleft = (off_x, off_y))
        self.mask = mask.from_threshold(Rs.cargar_imagen(data['capa_background']['colisiones']), Cs.COLOR_COLISION,
                                        (1, 1, 1, 255))

        self.cargar_limites(data['limites'])

    def __repr__(self):
        return "ChunkMap " + self.nombre

    def ubicar(self, x, y):
        """Coloca al sprite en pantalla
        :param y:
        :param x:
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

            mapa = ChunkMap(self.stage, data,  nmbr, dx, dy)

            self.limites[ady] = mapa
            self.stage.chunks.add(mapa)
            
            if ady == 'izq' or ady == 'der':
                self.stage.rect.inflate_ip(mapa.rect.w,0)
                if ady == 'izq':
                    for spr in self.stage.properties:
                        spr.stageX += mapa.rect.w
            elif ady == 'sup' or ady == 'inf':
                self.stage.rect.h.inflate_ip(0,mapa.rect.h)
                if ady == 'sup':
                    for spr in self.stage.properties:
                        spr.stageY += mapa.rect.h
            
            return mapa
        except IOError:
            pass

        return False

    def update(self):
        # self.stage.anochecer()
        self.stage.actualizar_grilla()

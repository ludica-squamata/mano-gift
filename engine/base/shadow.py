from pygame import mask, PixelArray, Surface, SRCALPHA, transform, Rect
from engine.globs import FEATURE_SOMBRAS_DINAMICAS, COLOR_SOMBRA
from engine.globs.eventDispatcher import EventDispatcher
from engine.globs.renderer import Renderer
from engine.misc import ReversibleDict
from .azoeSprite import AzoeSprite
# noinspection PyUnresolvedReferences
from math import floor


class Sombra(AzoeSprite):
    dif_x = 0
    alpha = 0

    def __init__(self, spr, dfx, img, mascara, dz):
        self.spr = spr
        self.tipo = "sombra"
        self.nombre = "sombra de " + self.spr.nombre
        super().__init__(imagen=img, x=spr.rect.x - dfx, y=spr.rect.y, z=spr.z, dz=dz - 1)
        self.mask = mascara
        self.alpha = 150
        self.dif_x = dfx

    def ubicar(self, x, y):
        """Coloca al sprite en pantalla
        :param y: int
        :param x: int
        """

        super().ubicar(x - self.dif_x, y)

    def fade(self, value):
        w, h = self.image.get_size()
        surface = self.image.copy()
        pxarray = PixelArray(surface)
        self.alpha += value
        if 0 <= self.alpha <= 150:
            for y in range(h):
                for x in range(w):
                    if self.mask.get_at((x, y)):
                        pxarray[x, y] = 0, 0, 0, self.alpha
            self.image = pxarray.make_surface()
            del pxarray

    def __repr__(self):
        return self.nombre


class ShadowSprite(AzoeSprite):
    step = 'S'
    _sombras = None
    """:type : list"""
    sombra = None
    """:type : Sprite"""
    proyectaSombra = True
    _luces = None
    """:type : list"""
    _prevLuces = None
    """:type : list"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._sombras = [0, 0, 0, 0, 0, 0, 0, 0]
        self._luces = [0, 0, 0, 0, 0, 0, 0, 0]

        # 4 , 5, 6 , 7,  0, 1,  2, 3
        # SO, O, NO, N, NE, E, SE, S # sombras
        # NE, E, SE, S, SO, O, NO, N # luces
        # 0 , 1, 2 , 0, 4,  5, 6,  7

        self.previousimage = self.image
        if FEATURE_SOMBRAS_DINAMICAS:
            EventDispatcher.register(self.update_luces, 'SolarMovement')

    def add_shadow(self, *args):
        Renderer.camara.remove_obj(self.sombra)
        self.sombra = Sombra(self, *args)

        Renderer.camara.add_visible(self.sombra)

    def crear_sombras(self):

        h = self.rect.h
        w = self.rect.w
        h_2 = h // 2
        z = 0
        dr = 0  # un pequeño ajuste en el eje +x ("delta derecha")

        t_surface = Surface((h * 2, h * 2), SRCALPHA)
        t_rect = t_surface.get_rect()
        centerx = t_surface.get_width() // 4
        """:type t_surface: SurfaceType"""

        surface = self.image
        mascara = mask.from_surface(t_surface)
        mascara.clear()

        if self._sombras[0]:  # Luz: 4
            # print('Luz 4: NE')
            img = self._crear_sombra(surface, "NE")
            t_surface.blit(img, (h_2, 0))
            _draw = mask.from_surface(t_surface, 100)
            mascara.draw(_draw, (0, 0))
        if self._sombras[6]:  # Luz: 3
            # print('Luz 3: NO')
            img = self._crear_sombra(surface, "NO")
            t_surface.blit(img, (0, 0))
            _draw = mask.from_surface(t_surface, 100)
            mascara.draw(_draw, (0, 0))
        if self._sombras[4]:  # Luz: 1
            # print('Luz 1: SO')
            img = self._crear_sombra(surface, "SO")
            t_surface.blit(img, (3, h_2 - 6))
            _draw = mask.from_surface(t_surface, 100)
            mascara.draw(_draw, (0, 0))
            z = h
        if self._sombras[2]:  # Luz: 6
            # print('Luz 6: SE')
            img = self._crear_sombra(surface, "SE")
            t_surface.blit(img, (centerx, h_2 - 4))
            _draw = mask.from_surface(t_surface, 100)
            mascara.draw(_draw, (0, 0))
            z = h
        if self._sombras[1]:  # Luz: 5
            top = h_2 + 5
            dirs = ReversibleDict(abajo='izquierda', arriba='derecha')
            if self.images is not None:
                surface = transform.rotate(self.images[self.step + dirs[self.direccion]], +90)
                if self.direccion == 'abajo':
                    top = h_2 - 5
                elif self.direccion == 'arriba':
                    top = h_2 - 6
                elif self.direccion == 'derecha':
                    top = h_2 - 3
                elif self.direccion == 'izquierda':
                    top = h_2 - 4
            else:
                dr = 15
                surface = transform.rotate(surface, +90)

            img = self._crear_sombra(surface, "E")
            r = img.get_rect(right=t_rect.centerx + dr, top=top)
            t_surface.blit(img, r)
            _draw = mask.from_surface(t_surface, 100)
            mascara.draw(_draw, (0, 0))
            z = h  # incorrecto, pues la sombra se genera por encima del objeto que la proyecta. Los valores que la
            # ponen por debajo del objeto son todos iguales o menores a 0, pero ponerla en ese valor hace que cuando
            # el heroe le camine por encima, la sombra no lo cubre.
        if self._sombras[5]:  # Luz: 2
            top = h_2 + 5
            dirs = ReversibleDict(abajo='derecha', arriba='izquierda')
            if self.images is not None:
                surface = transform.rotate(self.images[self.step + dirs[self.direccion]], -90)
                if self.direccion == 'abajo':
                    top = h_2 - 5
                elif self.direccion == 'arriba':
                    top = h_2 - 6
                elif self.direccion == 'derecha':
                    top = h_2 - 3
                elif self.direccion == 'izquierda':
                    top = h_2 - 4
            else:
                dr = 3
                surface = transform.rotate(surface, -90)

            img = self._crear_sombra(surface, "O")
            r = img.get_rect(left=t_rect.centerx + dr, top=top)
            t_surface.blit(img, r)
            _draw = mask.from_surface(t_surface, 100)
            mascara.draw(_draw, (0, 0))
            z = h  # incorrecto, pues la sombra se genera por encima del objeto que la proyecta. Los valores que la
            # ponen por debajo del objeto son todos iguales o menores a 0, pero ponerla en ese valor hace que cuando
            # el heroe le camine por encima, la sombra no lo cubre.
        if self._sombras[7]:  # Luz: 3
            print('Luz 3: N')
            # img = self._crear_sombra(surface, "N")
            # t_surface.blit(img, (h_2, 0))
        if self._sombras[3]:  # Luz: 0
            img = self._crear_sombra(surface, "S")
            r = img.get_rect(centerx=w // 2 + 1, y=h - 3)
            t_surface = Surface((w, h * 2), SRCALPHA)
            t_surface.blit(img, r)
            _draw = mask.from_surface(t_surface, 100)
            mascara.draw(_draw, (0, 0))
            h_2 = 0
            z = h

        return h_2, t_surface, mascara, z

    @staticmethod
    def _crear_sombra(surface, arg=None, _mask=None):
        h = surface.get_height()
        w = surface.get_width()
        if _mask is None:
            _mask = mask.from_surface(surface)

        pxarray = None
        d = h // 2
        nw = w + d
        nh = h + d

        if arg == 'NE':
            pxarray = PixelArray(Surface((nw, h), 0, surface))
            for y in range(h):
                dd = floor(d * (1 - (y / h)))
                for x in range(w):
                    if _mask.get_at((x, y)):
                        pxarray[x + dd, y] = COLOR_SOMBRA

        if arg == 'NO':
            pxarray = PixelArray(Surface((nw, h), 0, surface))
            for y in range(h):
                dd = floor(d * (y / h))
                for x in range(w):
                    if _mask.get_at((x, y)):
                        pxarray[x + dd, y] = COLOR_SOMBRA

        if arg == 'SE':
            pxarray = PixelArray(Surface((nw, nh), 0, surface))
            for y in range(h - 3):
                dd = floor(d * (1 - (y / h)))
                for x in range(w):
                    if _mask.get_at((x, y)):
                        ax = x + dd - 1
                        ay = (nh - y) - 1
                        pxarray[ax, ay] = COLOR_SOMBRA

        if arg == 'SO':
            pxarray = PixelArray(Surface((nw, nh), 0, surface))
            for y in range(h - 5):
                dd = floor(d * (y / h))
                for x in range(w):
                    if _mask.get_at((x, y)):
                        ax = x + dd - 1
                        ay = (nh - y) - 1
                        pxarray[ax, ay] = COLOR_SOMBRA

        if arg == 'S':
            pxarray = PixelArray(Surface((w, h), 0, surface))
            for x in range(w):
                for y in range(h):
                    if _mask.get_at((x, y)):
                        n = -(x * h + y + 2)
                        ax, ay = n // h, n % h
                        pxarray[ax, ay] = COLOR_SOMBRA

        if arg == 'N':
            pass

        if arg == 'E':
            pxarray = PixelArray(Surface((w, h), 0, surface))
            for x in range(w):
                for y in range(h):
                    if _mask.get_at((x, y)):
                        n = (x * w + y)
                        ax, ay = n // w, n % w
                        pxarray[ax, ay] = COLOR_SOMBRA

        if arg == 'O':
            pxarray = PixelArray(Surface((w, h), 0, surface))
            for x in range(w):
                for y in range(h):
                    if _mask.get_at((x, y)):
                        n = (x * h + y)
                        ax, ay = n // h, n % h
                        pxarray[ax, ay] = COLOR_SOMBRA

        return pxarray.make_surface().convert_alpha()

    @staticmethod
    def dark_overlay(surface, start=0, stop=0):
        w, h = surface.get_size()
        pxarray = PixelArray(Surface((w, h), 0, surface))
        _mask = mask.from_surface(surface)

        if stop == 0:
            stop = w
        # 0, w
        # 0, w//2
        # w//2, w

        for y in range(h):
            for x in range(start, stop):
                if _mask.get_at((x, y)):
                    pxarray[x, y] = COLOR_SOMBRA

        return pxarray.make_surface().convert_alpha()

    def recibir_luz(self, source, t=100):
        """
        :param source:
        :type source:AzoeSprite
        :return:
        :param t:
        :type: int
        """
        if t % 2 == 0:
            t += 1
        size = t, t
        x, y = source.rect.topleft
        a = t // 2
        b = a + t
        topleft = Rect((-b+x, -b+y), size)
        topright = Rect((a + 1, -b), size)
        topmid = Rect((-a, -b), size)
        bottomleft = Rect((-b, a + 1), size)
        bottomright = Rect((a + 1, a + 1), size)
        bottommid = Rect((-a, a + 1), size)
        midleft = Rect((-b, -a), size)
        midright = Rect((a + 1, -a), size)
        if self.proyectaSombra:
            # marcar direccion como iluminada

            self._luces = [0, 0, 0, 0, 0, 0, 0, 0]
            if topleft.contains(self.mapRect):
                self._luces[0] = True
            if topright.contains(self.mapRect):
                self._luces[0] = True
            if topmid.contains(self.mapRect):
                self._luces[0] = True
            if bottomleft.contains(self.mapRect):
                self._luces[0] = True
            if bottomright.contains(self.mapRect):
                self._luces[0] = True
            if bottommid.contains(self.mapRect):
                self._luces[0] = True
            if midleft.contains(self.mapRect):
                self._luces[0] = True
            if midright.contains(self.mapRect):
                self._luces[0] = True

        self.update_sombra()

    def update_sombra(self):
        """
        generar sombra en direccion contraria a los slots iluminados
        si cambio la lista, actualizar imagen de sombra y centrar

        para el calculo de sombras ha de usarse la imagen que veria la fuente de luz.
        ej: si el personaje estuviera en posicion D, la sombra O se hace en base a la imagen R
        si estuviera en posicion U, se usaria L

        a resolver: que imagen usar para las diagonales

        :return:
        """
        if self._prevLuces is None or self._luces != self._prevLuces:
            self._prevLuces = self._luces[:]
            for i in range(0, 7):
                if (self._luces[(i + 4) % 7] - self._luces[i]) == 1:  # bool
                    self._sombras[i] = 1
                else:
                    self._sombras[i] = 0

            if any(self._sombras):
                self.add_shadow(*self.crear_sombras())

    def update_luces(self, event):
        # self._luces = [0, 0, 0, 0, 0, 0, 0, 0]
        p = event.data['light']
        self._luces[p] = 1
        self._luces[(p + 4) % 7] = 0  # las luces de lados contrarios se anulan
        if self.proyectaSombra:
            self.update_sombra()

    def image_has_chaged(self):
        if self.image != self.previousimage and self.sombra is not None:
            self.add_shadow(*self.crear_sombras())
            self.previousimage = self.image

    def update(self, *args):
        if self.proyectaSombra:
            self.image_has_chaged()
        super().update(*args)

    def ubicar(self, dx, dy):
        super().ubicar(dx, dy)
        if self.sombra is not None:
            self.sombra.ubicar(dx, dy)

    def reubicar(self, dx, dy):
        super().reubicar(dx, dy)
        if self.sombra is not None:
            self.sombra.reubicar(dx, dy)

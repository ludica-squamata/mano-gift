from pygame import mask, PixelArray, Surface, SRCALPHA, transform
from engine.globs import FEATURE_SOMBRAS_DINAMICAS, COLOR_SOMBRA
from engine.globs.event_dispatcher import EventDispatcher
from engine.globs.renderer import Renderer
from .azoe_sprite import AzoeSprite
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

    def __repr__(self):
        return self.nombre


class ShadowSprite(AzoeSprite):
    _sombras = None
    """:type : list"""
    sombra = None
    """:type : Sprite"""
    sombras = None
    """:type : list"""
    proyectaSombra = True
    _luces = None
    """:type : list"""
    _prevLuces = None
    """:type : list"""
    alpha = 150

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._sombras = [0, 0, 0, 0, 0, 0, 0, 0]
        self._luces = [0, 0, 0, 0, 1, 0, 0, 0]
        self.sombra = None
        self.spr_sombras = {}
        self._prevLuces = [0, 0, 0, 0, 0, 0, 0, 0]
        EventDispatcher.register(self.set_alpha, 'SetNight')
        # las luces 1 y 5 (este y oeste) producen sombras erroneas.

    def set_alpha(self, event):
        if 'mod' in event.data:
            self.alpha -= event.data['mod'] * 3

        elif 'alpha' in event.data:
            negative = event.data['alpha']
            self.alpha = 0 if self.alpha-negative < 0 else self.alpha-negative

    def add_shadow(self):
        z = self.sombra.z if self.sombra is not None else 0
        Renderer.camara.remove_obj(self.sombra)

        if self.image not in self.spr_sombras:
            self.spr_sombras[self.image] = None

        if self.spr_sombras[self.image] is None:
            s = Sombra(self, *self.crear_sombras())
            self.spr_sombras[self.image] = s

        else:
            s = self.spr_sombras[self.image]

        if z:
            s.z = z

        s.image.set_alpha(self.alpha)
        self.sombra = s
        Renderer.camara.add_visible(self.sombra)

    def crear_sombras(self):

        h = self.rect.h
        w = self.rect.w
        h_2 = h // 2
        z = 0
        # dr = 0  # un pequeño ajuste en el eje +x ("delta derecha")

        t_surface = Surface((h * 2, h * 2), SRCALPHA)
        # t_rect = t_surface.get_rect()
        centerx = t_surface.get_width() // 4
        """:type t_surface: SurfaceType"""

        surface = self.image
        mascara = mask.from_surface(t_surface)
        mascara.clear()

        if self._sombras[0]:
            img = self.orientar_sombra(surface, "NE")
            t_surface.blit(img, (h_2, 0))
            _draw = mask.from_surface(t_surface, 100)
            mascara.draw(_draw, (0, 0))
        if self._sombras[6]:
            img = self.orientar_sombra(surface, "NO")
            t_surface.blit(img, (0, 0))
            _draw = mask.from_surface(t_surface, 100)
            mascara.draw(_draw, (0, 0))
        if self._sombras[4]:
            img = self.orientar_sombra(surface, "SO")
            t_surface.blit(img, (3, h_2 - 6))
            t_surface.blit(self.dark_overlay(surface), (centerx, 0))
            _draw = mask.from_surface(t_surface, 100)
            mascara.draw(_draw, (0, 0))
            z = h
        if self._sombras[2]:
            img = self.orientar_sombra(surface, "SE")
            t_surface.blit(img, (centerx, h_2 - 4))
            t_surface.blit(self.dark_overlay(surface), (centerx, 0))
            _draw = mask.from_surface(t_surface, 100)
            mascara.draw(_draw, (0, 0))
            z = h
        if self._sombras[1]:  # Luz: 5
            print('Luz 5: E')
            # top = h_2 + 5
            # if self.images is not None:
            #     surface = transform.rotate(self.image, +90)
            #     dh = {'abajo': -5, 'arriba': -6, 'derecha': -6, 'izquierda': -4}
            #     top = h_2 + dh[self.direccion]
            # else:
            #     dr = 15
            #     surface = transform.rotate(surface, +90)
            #
            # img = self.orientar_sombra(surface, "E")
            # r = img.get_rect(right=t_rect.centerx + dr, top=top)
            # t_surface.blit(img, r)
            # _draw = mask.from_surface(t_surface, 100)
            # mascara.draw(_draw, (0, 0))
        if self._sombras[5]:
            print('Luz 1: O')
            # top = h_2 + 5
            # if self.images is not None:
            #     surface = transform.rotate(self.image, -90)
            #     dh = {'abajo': -5, 'arriba': -6, 'derecha': -6, 'izquierda': -4}
            #     top = h_2 + dh[self.direccion]
            #     if self.direccion == 'derecha':
            #         dr = -4
            # else:
            #     dr = 3
            #     surface = transform.rotate(surface, -90)
            #
            # img = self.orientar_sombra(surface, "O")
            # r = img.get_rect(left=t_rect.centerx + dr, top=top)
            # t_surface.blit(img, r)
            # _draw = mask.from_surface(t_surface, 100)
            # mascara.draw(_draw, (0, 0))
            # z = h - 2
        if self._sombras[7]:
            img = self.orientar_sombra(surface, "N")
            img = transform.scale(img, [w, h // 2])
            r = img.get_rect(centerx=w // 2, bottom=h - 1)
            t_surface = Surface((w, h * 2), SRCALPHA)
            t_surface.blit(img, r)
            _draw = mask.from_surface(t_surface, 100)
            mascara.draw(_draw, (0, 0))
            h_2 = 0
            z = -h
        if self._sombras[3]:
            img = self.orientar_sombra(surface, "S")
            r = img.get_rect(centerx=w // 2, y=h - 3)
            t_surface = Surface((w, h * 2), SRCALPHA)
            t_surface.blit(img, r)
            t_surface.blit(self.dark_overlay(surface), (0, 0))
            _draw = mask.from_surface(t_surface, 100)
            mascara.draw(_draw, (0, 0))
            h_2 = 0
            z = h

        return h_2, t_surface, mascara, z

    # noinspection PyUnresolvedReferences
    @staticmethod
    def orientar_sombra(surface, arg=None, _mask=None):
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
                for y in range(h - 1):
                    if _mask.get_at((x, y)):
                        n = -(x * h + y + 2)
                        ax, ay = -n // h, n % h
                        if ax < w and ay < h:
                            pxarray[ax, ay] = COLOR_SOMBRA

        if arg == 'N':
            pxarray = PixelArray(Surface((w, h), 0, surface))
            for y in range(h):
                for x in range(w):
                    if _mask.get_at((x, y)):
                        pxarray[x, y] = COLOR_SOMBRA

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

        for y in range(h):
            for x in range(start, stop):
                if _mask.get_at((x, y)):
                    # noinspection PyUnresolvedReferences
                    pxarray[x, y] = COLOR_SOMBRA

        return pxarray.make_surface().convert_alpha()

    @staticmethod
    def filtrar_luces(i):
        return i not in (1, 5)

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
        if self._prevLuces != self._luces:
            self._prevLuces = self._luces[:]
            for i in range(0, 8):
                if self.filtrar_luces(i):
                    if (self._luces[(i + 4) % 8] - self._luces[i]) == 1:  # bool
                        self._sombras[i] = 1
                    else:
                        self._sombras[i] = 0

        if any(self._sombras) and FEATURE_SOMBRAS_DINAMICAS:
            self.add_shadow()

    def update(self, *args):
        if self.proyectaSombra:
            self.update_sombra()
        super().update(*args)

    def ubicar(self, dx, dy):
        super().ubicar(dx, dy)
        if self.sombra is not None:
            self.sombra.ubicar(dx, dy)
            self.sombra.z = self.z-1

    def reubicar(self, dx, dy):
        super().reubicar(dx, dy)
        if self.sombra is not None:
            self.sombra.reubicar(dx, dy)

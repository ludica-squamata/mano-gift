from pygame import mask, PixelArray, Surface, SRCALPHA
from engine.globs.renderer import Renderer
from .azoeSprite import AzoeSprite
from pygame import draw, Rect


class Sombra(AzoeSprite):
    dif_x = 0
    alpha = 0

    def __init__(self, spr, dfx, img, mascara, dz):
        self.spr = spr
        self.tipo = "sombra"
        self.nombre = "sombra de " + self.spr.nombre
        super().__init__(imagen=img, x=spr.rect.x - dfx, y=spr.rect.y, z=spr.z + dz - 1)
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
    _sombras = None
    """:type : list"""
    sombra = None
    """:type : Sprite"""
    proyectaSombra = True
    _luces = None
    """:type : list"""
    _prevLuces = None
    """:type : list"""

    def __init__(self, *args, **kwargs):

        self._sombras = [0, 0, 0, 0, 0, 0, 0, 0]
        self._luces = [0, 0, 0, 0, 0, 0, 0, 0]

        # 4 , 5, 6 , 7,  0, 1,  2, 3
        # SO, O, NO, N, NE, E, SE, S # sombras
        # NE, E, SE, S, SO, O, NO, N # luces
        # 0 , 1, 2 , 3, 4,  5, 6,  7

        super().__init__(*args, **kwargs)
        self.previousimage = self.image

    def add_shadow(self, *args):
        Renderer.camara.remove_obj(self.sombra)
        self.sombra = Sombra(self, *args)

        Renderer.camara.add_visible(self.sombra)

    # def dark_overlay(self):
    #     for y in range(h):
    #         for x in range(w):
    #             if _mask.get_at((x, y)):
    #                 pxarray[x, y] = shadow_color

    def crear_sombras(self):

        h = self.rect.h
        # w = self.rect.w
        h_2 = h // 2
        z = 0

        t_surface = Surface((h * 2, h * 2), SRCALPHA)
        centerx = t_surface.get_width() // 4
        """:type t_surface: SurfaceType"""

        surface = self.image
        mascara = mask.from_surface(t_surface)
        mascara.clear()

        if self._sombras[0]:  # Luz: 4
            img = self._crear_sombra(surface, "NE")
            t_surface.blit(img, (h_2, 0))
            _draw = mask.from_surface(t_surface, 100)
            mascara.draw(_draw, (0, 0))
        if self._sombras[6]:  # Luz: 3
            img = self._crear_sombra(surface, "NO")
            t_surface.blit(img, (0, 0))
            _draw = mask.from_surface(t_surface, 100)
            mascara.draw(_draw, (0, 0))
        if self._sombras[4]:  # Luz: 1
            img = self._crear_sombra(surface, "SO")
            t_surface.blit(img, (3, h_2 - 6))
            _draw = mask.from_surface(t_surface, 100)
            mascara.draw(_draw, (0, 0))
            z = h
        if self._sombras[2]:  # Luz: 6
            img = self._crear_sombra(surface, "SE")
            t_surface.blit(img, (centerx, h_2 - 4))
            _draw = mask.from_surface(t_surface, 100)
            mascara.draw(_draw, (0, 0))
            z = h
        if self._sombras[1]:  # Luz: 5
            print('Luz 5: E')
            # img = self._crear_sombra(surface, "E")
            # t_surface.blit(img, (h_2, 0))
        if self._sombras[5]:  # Luz: 2
            print('Luz 2: O')
            # img = self._crear_sombra(surface, "O")
            # t_surface.blit(img, (h_2, 0))
        if self._sombras[7]:  # Luz: 3
            print('Luz 3: N')
            # img = self._crear_sombra(surface, "N")
            # t_surface.blit(img, (h_2, 0))
        if self._sombras[3]:  # Luz: 7
            print('Luz 7: S')
            # img = self._crear_sombra(surface, "S")
            # t_surface.blit(img, (h_2, 0))

        # draw.rect(t_surface, (255, 0, 0), Rect(1, 1, t_surface.get_width() - 2, t_surface.get_height() - 2), 1)

        return h_2, t_surface, mascara, z

    @staticmethod
    def _crear_sombra(surface, arg=None, _mask=None):
        from math import floor

        h = surface.get_height()
        w = surface.get_width()
        if _mask is None:
            _mask = mask.from_surface(surface)

        shadow_color = 0, 0, 0, 150
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
                        pxarray[x + dd, y] = shadow_color

        if arg == 'NO':
            pxarray = PixelArray(Surface((nw, h), 0, surface))
            for y in range(h):
                dd = floor(d * (y / h))
                for x in range(w):
                    if _mask.get_at((x, y)):
                        pxarray[x + dd, y] = shadow_color

        if arg == 'SE':
            pxarray = PixelArray(Surface((nw, nh), 0, surface))
            for y in range(h):
                dd = floor(d * (1 - (y / h)))
                for x in range(w):
                    if _mask.get_at((x, y)):
                        ax = x + dd - 1
                        ay = (nh - y) - 1
                        pxarray[ax, ay] = shadow_color

        if arg == 'SO':
            pxarray = PixelArray(Surface((nw, nh), 0, surface))
            for y in range(h):
                dd = floor(d * (y / h))
                for x in range(w):
                    if _mask.get_at((x, y)):
                        ax = x + dd - 1
                        ay = (nh - y) - 1
                        pxarray[ax, ay] = shadow_color

        if arg == 'S':
            pass

        if arg == 'N':
            pass

        if arg == 'E':
            pass

        if arg == 'O':
            pass

        return pxarray.make_surface().convert_alpha()

    def recibir_luz(self, source):
        """
        :param source:
        :type source:AzoeSprite
        :return:
        """
        # tolerancia = 10
        if self.proyectaSombra:
            # calcular direccion de origen
            dx = self.rect.centerX - source.rect.centerX
            dy = self.rect.centerY - source.rect.centerY

            # marcar direccion como iluminada
            if dx > 0:
                if dy > 0:
                    self._luces[0] = True  # noreste
                elif dy < 0:
                    self._luces[2] = True  # sureste
                else:
                    self._luces[1] = True  # este
            elif dx < 0:
                if dy > 0:
                    self._luces[6] = True  # noroeste
                elif dy < 0:
                    self._luces[4] = True  # suroeste
                else:
                    self._luces[5] = True  # oeste
            else:
                if dy > 0:
                    self._luces[7] = True  # norte
                else:
                    self._luces[3] = True  # sur

    def update_sombra(self):
        """
        generar sombra en direccion contraria a los slots iluminados
        si cambio la lista,
        actualizar imagen de sombra y centrar

        para el calculo de sombras ha de usarse la imagen que veria la fuente de luz.
        ej: si el personaje estuviera en posicion D, la sombra O se hace en base a la imagen R
        si estuviera en posicion U, se usaria L

        a resolver: que imagen usar para las diagonales

        :return:
        """
        if self._prevLuces is None or self._luces != self._prevLuces:
            self._prevLuces = self._luces[:]
            # las luces de lados contrarios se anulan
            for i in range(0, 7):
                if (self._luces[(i + 4) % 7] - self._luces[i]) == 1:  # bool
                    self._sombras[i] = 1
                else:
                    self._sombras[i] = 0

            # loop unrolling para evitar el costo de %, aunque solo es necesario cada vez que cambian las luces
            # self._sombras[0] = self._luces[4] - self._luces[0]
            # self._sombras[1] = self._luces[5] - self._luces[1]
            # self._sombras[2] = self._luces[6] - self._luces[2]
            # self._sombras[3] = self._luces[7] - self._luces[3]
            # self._sombras[4] = self._luces[0] - self._luces[4]
            # self._sombras[5] = self._luces[1] - self._luces[5]
            # self._sombras[6] = self._luces[2] - self._luces[6]
            # self._sombras[7] = self._luces[3] - self._luces[7]

            if any(self._sombras):
                return self.crear_sombras()

    def image_has_chaged(self):
        if self.image != self.previousimage and self.sombra is not None:
            self.add_shadow(*self.crear_sombras())
            self.previousimage = self.image

    def update(self, *args):
        if self.proyectaSombra:
            self.image_has_chaged()
        # if self.sombra is not None:
        #     self.sombra.z = self.z-1
        super().update(*args)

    def ubicar(self, dx, dy):
        super().ubicar(dx, dy)
        if self.sombra is not None:
            self.sombra.ubicar(dx, dy)

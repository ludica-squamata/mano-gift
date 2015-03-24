from pygame import mask as MASK, PixelArray, Surface, transform, SRCALPHA
from pygame.sprite import DirtySprite
from .giftSprite import _giftSprite
from engine.globs import EngineData as ED


class _sombra(_giftSprite):
    def __init__(self, imagen, rect, x, y, obj):
        super().__init__(imagen=imagen, x=x, y=y)
        self.deltaRect = rect
        self.rect = self.set_pos(x, y)
        self.tipo = "sombra"
        self.obj = obj

    def set_pos(self, x, y):
        # obtiene la posicion final tomando como base la posicion del
        # sprite y la suya propia
        rect = self.image.get_rect()
        rect.x = x + self.deltaRect.x
        rect.y = y + self.deltaRect.y

        return rect

    def ubicar(self, x, y):
        '''Coloca al sprite en pantalla'''
        self.rect.x = x + self.deltaRect.x
        self.rect.y = y + self.deltaRect.y
        if self.image != None:
            self.dirty = 1


class ShadowSprite(_giftSprite):
    _sombras = None
    """:type : list"""
    _sprSombra = None
    """:type : Sprite"""
    proyectaSombra = True
    _luces = None
    """:type : list"""
    _prevLuces = None
    """:type : list"""

    def __init__(self, *args, **kwargs):
        self._sombras = [0, 0, 0, 0, 0, 0, 0, 0]
        self._luces = [0, 0, 0, 0, 1, 0, 0, 0]

        super().__init__(*args, **kwargs)

    def crear_sombras(self):

        h = self.rect.h
        w = self.rect.w
        h_2 = h/2

        if self._sprSombra is None:
            self._sprSombra = _giftSprite(Surface((h-w, h*2), SRCALPHA))
            self._sprSombra.mapY = self.mapY
            self._sprSombra.mapX = self.mapX - h_2
            self._sprSombra.ubicar(self.rect.x - h_2, self.rect.y)
            # self._sprSombra = _sombra(Surface((h-w, h*2), SRCALPHA), self.rect, self.mapX, self.mapY, self)
            ED.RENDERER.addObj(self._sprSombra, self.rect.bottom - 10)


        t_surface = Surface((h*2, h*2), SRCALPHA)
        """:type t_surface: SurfaceType"""

        surface = self.image

        # Sombra Noreste
        if self._sombras[0] == 1:
            img = self._crear_sombra(surface, "NE")
            t_surface.blit(img, (h_2, 0))
        if self._sombras[1] == 1:
            img = self._crear_sombra(surface, "E")
            t_surface.blit(img, (h_2, 0))

        self._sprSombra.image = t_surface
        """
        # Sombra Este
        elif sombra == 1:
            img = self._crear_sombra(surface, "E")
            rect = img.get_rect()
            rect.centery = img_rect.bottom - 6
            rect.left = img_rect.centerx

        #Sombra Sureste
        elif sombra == 2:
            img = self._crear_sombra(surface, "SE")
            rect = img.get_rect()
            rect.top = img_rect.bottom - 6
            rect.centerx = img_rect.centerx + img_rect.w // 4 + 4

        #Sombra Sur
        elif sombra == 3:
            img = self._crear_sombra(surface, "S")
            rect = img.get_rect()
            rect.top = img_rect.bottom - 6
            rect.left = img_rect.left

        #Sombra Suroeste
        elif sombra == 4:
            img = self._crear_sombra(surface, "SO")
            rect = img.get_rect()
            rect.top = img_rect.bottom - 6
            rect.centerx = img_rect.centerx - img_rect.w // 4 - 3

        #Sombra Oeste
        elif sombra == 5:
            img = self._crear_sombra(surface, "O")
            rect = img.get_rect()
            rect.centery = img_rect.bottom - 4
            rect.right = img_rect.centerx

        #Sombra Noroeste
        elif sombra == 6:
            img = self._crear_sombra(surface, "NO")
            rect = img.get_rect()
            rect.top = img_rect.top
            rect.right = img_rect.right + 2

        #Sombra Norte
        elif sombra == 7:
            img = self._crear_sombra(surface, "N")
            rect = img.get_rect(bottomleft=img_rect.bottomleft)

        return img, rect
        """

    @staticmethod
    def _crear_sombra(surface, arg=None, mask=None):
        from math import floor

        h = surface.get_height()
        w = surface.get_width()
        if mask == None:
            mask = MASK.from_surface(surface)

        shadow_color = 0, 0, 0, 150

        # if arg in ('N', 'S', 'E', 'O'):
        #     pxarray = PixelArray(Surface((w, h), 0, surface))
        # else:
        #     pxarray = PixelArray(Surface((int(w + h / 2), h), 0, surface))
        #
        # for x in range(w):
        #     for y in range(h):
        #         if arg in ('N', 'S', 'E', 'O'):
        #             if mask.get_at((x, y)):
        #                 pxarray[x, y] = 0, 0, 0, 150
        #         else:
        #             if mask.get_at((x, y)):
        #                 pxarray[int(x + (h - y) / 2), y] = (0, 0, 0, 150)

        # if arg == 'N':
        #     return transform.smoothscale(pxarray.make_surface().convert_alpha(), (w, h // 2))
        # elif arg == 'S':
        #     return transform.flip(pxarray.make_surface().convert_alpha(), False, True)
        # elif arg == 'E':
        #     return transform.rotate(pxarray.make_surface().convert_alpha(), -90)
        # elif arg == 'O':
        #     return transform.rotate(pxarray.make_surface().convert_alpha(), 90)
        # elif arg == 'NO':
        #     return transform.flip(pxarray.make_surface().convert_alpha(), True, False)
        # elif arg == 'SO':
        #     return transform.flip(pxarray.make_surface().convert_alpha(), True, True)
        # elif arg == 'SE':
        #     return transform.flip(pxarray.make_surface().convert_alpha(), False, True)
        # else:  # NE

        #if arg == 'NE':
        d = h/2
        nw = w + d

        pxarray = PixelArray(Surface((nw, h), 0, surface))
        for y in range(h):
            dd = floor(d * (1-(y/h)))
            for x in range(w):
                if mask.get_at((x, y)):
                    pxarray[x+dd, y] = shadow_color

        return pxarray.make_surface().convert_alpha()

    def recibir_luz(self, source):
        """
        :param source:
        :type source:_giftSprite
        :return:
        """
        tolerancia = 10
        luces = self._luces
        if self.proyectaSombra:
            # calcular direccion de origen
            dx = self.rect.centerX - source.rect.centerX
            dy = self.rect.centerY - source.rect.centerY

            # marcar direccion como iluminada
            if dx > 0:
                if dy > 0:
                    luces[0] = True  # noreste
                elif dy < 0:
                    luces[2] = True  # sureste
                else:
                    luces[1] = True  # este
            elif dx < 0:
                if dy > 0:
                    luces[6] = True  # noroeste
                elif dy < 0:
                    luces[4] = True  # suroeste
                else:
                    luces[5] = True  # oeste
            else:
                if dy > 0:
                    luces[7] = True  # norte
                else:
                    luces[3] = True  # sur

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
            for i in range(0, 7):
                if (self._luces[(i + 4) % 7] - self._luces[i]) == 1:  #bool
                    self._sombras[i] = 1
                else:
                    self._sombras[i] = 0
            self.crear_sombras()

    def update(self, *args):
        self.update_sombra()
        # self._sprSombra.ubicar(self.rect.x - )
        # self._sprSombra.rect.x =
        # self._sprSombra.rect.y = self.rect.y - self.rect.h
        super().update(*args)

    def reubicar(self, dx, dy):
        super().reubicar(dx, dy)
        if self._sprSombra is not None:
            self._sprSombra.reubicar(dx, dy)

from pygame import mask as MASK, PixelArray, Surface, transform, SRCALPHA
from pygame.sprite import Sprite
from .azoeSprite import AzoeSprite
from engine.globs import EngineData as ED


class _sombra(AzoeSprite):
    dif_x = 0
    alpha = 0
    def __init__(self, spr, dfx, img):
        self.spr = spr
        self.tipo = "sombra"
        self.nombre = "sombra de "+self.spr.nombre
        super().__init__(imagen=img, x = spr.rect.x, y = spr.rect.y, z = spr.rect.bottom-1)
        self.alpha = self.image.get_alpha()
        self.dif_x = dfx
        
    def ubicar(self, x, y, z=0):
        """Coloca al sprite en pantalla"""
        if self.z+z < self.spr.z:
            super().ubicar(x - self.dif_x, y, z)
        else:
            super().ubicar(x - self.dif_x, y)
    
    def __repr__(self):
        return self.nombre

class ShadowSprite(AzoeSprite):
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
        self._luces = [0, 0, 0, 0, 1, 0, 0, 0]  # SO, O, NO, N, NE, E, SE, S

        super().__init__(*args, **kwargs)

    def crear_sombras(self):

        h = self.rect.h
        w = self.rect.w
        h_2 = h / 2

        t_surface = Surface((h * 2, h * 2), SRCALPHA)
        """:type t_surface: SurfaceType"""

        surface = self.image

        # Sombra Noreste
        if self._sombras[0] == 1:
            img = self._crear_sombra(surface, "NE")
            t_surface.blit(img, (h_2, 0))
        if self._sombras[5] == 1:
            img = self._crear_sombra(surface, "NO")
            t_surface.blit(img, (0, 0))
        if self._sombras[1] == 1:
            img = self._crear_sombra(surface, "E")
            t_surface.blit(img, (h_2, 0))

        import sys

        if 'pydevd' in sys.modules:
            from pygame import draw, Rect

            draw.rect(t_surface, (255, 0, 0), Rect(1, 1, t_surface.get_width() - 2, t_surface.get_height() - 2), 1)

        if self._sprSombra is None:
            self._sprSombra = _sombra(self, h_2, t_surface)            
            ED.RENDERER.camara.add_visible(self._sprSombra)
        
    @staticmethod
    def _crear_sombra(surface, arg=None, mask=None):
        from math import floor

        h = surface.get_height()
        w = surface.get_width()
        if mask == None:
            mask = MASK.from_surface(surface)

        shadow_color = 0, 0, 0, 150
        pxarray = None

        if arg == 'NE':
            d = h / 2
            nw = w + d

            pxarray = PixelArray(Surface((nw, h), 0, surface))
            for y in range(h):
                dd = floor(d * (1 - (y / h)))
                for x in range(w):
                    if mask.get_at((x, y)):
                        pxarray[x + dd, y] = shadow_color
        if arg == 'NO':
            d = h / 2
            nw = w + d

            pxarray = PixelArray(Surface((nw, h), 0, surface))
            for y in range(h):
                dd = floor(d * (y / h))
                for x in range(w):
                    if mask.get_at((x, y)):
                        pxarray[x + dd, y] = shadow_color

        return pxarray.make_surface().convert_alpha()

    def recibir_luz(self, source):
        """
        :param source:
        :type source:AzoeSprite
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
                if (self._luces[(i + 4) % 7] - self._luces[i]) == 1:  # bool
                    self._sombras[i] = 1
                else:
                    self._sombras[i] = 0
            self.crear_sombras()

    def update(self, *args):
        if self.proyectaSombra:
            self.update_sombra()
        super().update(*args)

    def ubicar(self, dx, dy, z =0):
        super().ubicar(dx, dy, z)
        if self._sprSombra is not None:
            self._sprSombra.ubicar(dx, dy, z)

    def reubicar(self, dx, dy):
        super().reubicar(dx, dy)
        if self._sprSombra is not None:
            self._sprSombra.reubicar(dx, dy)

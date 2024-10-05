from engine.globs import FEATURE_SOMBRAS_DINAMICAS, COLOR_SOMBRA, Light_Group
from pygame import mask, PixelArray, Surface, SRCALPHA, transform, draw
from engine.globs.event_dispatcher import EventDispatcher
from engine.globs.renderer import Renderer
from .azoe_sprite import AzoeSprite
from math import floor


class Sombra(AzoeSprite):
    dif_x = 0
    alpha = 0
    ensombrece = False

    def __init__(self, spr, dfx, img, mascara, over):
        super().__init__(spr, imagen=img, x=spr.rect.x - dfx, y=spr.rect.y)
        self.tipo = "sombra"
        self.nombre = "sombra de " + self.parent.nombre
        self.mask = mascara
        self.ensombrece = over
        self.alpha = 150
        self.dif_x = dfx

    def ubicar(self, x, y):
        """Coloca al sprite en pantalla
        :param y: int
        :param x: int
        """

        super().ubicar(x - self.dif_x, y)

        dz = 1 if self.ensombrece else -1
        self.z = self.parent.z + dz

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
    alpha = 150

    is_fading = None
    fade_shadow = None

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, **kwargs)
        self._sombras = [0] * 9  # la nueva luz y sombra
        self._luces = [0] * 9  # es la sombra en el cénit.
        self._origins = [0] * 9  # lo puse así para que sea más fácil
        self._prevLuces = [0] * 9  # distinguir una lista de 0s de otra
        self.sombra = None
        self.registerd_shadows = {}
        EventDispatcher.register(self.set_fading, 'ShadowFade', 'MinuteFlag')
        # las luces 1 y 5 (este y oeste) producen sombras erroneas.

    def unload(self):
        EventDispatcher.deregister(self.set_fading, 'ShadowFade', 'MinuteFlag')

    def set_fading(self, event):
        if event.tipo == 'ShadowFade':
            self.is_fading = event.data['do_fade']
            self.fade_shadow = event.data['inverted']
        elif event.tipo == 'MinuteFlag':
            if self.is_fading:
                # print(self, 'is fading', event.data['hora'])
                if self.fade_shadow is True:
                    # print('is disapearing')
                    self.alpha -= 1 if self.alpha - 1 >= 0 else 0
                else:
                    # print('is reapearing')
                    self.alpha += 1 if self.alpha + 1 <= 150 else 0

                if self.alpha == 0 or self.alpha == 150:
                    self.is_fading = False

    def add_shadow(self):
        Renderer.camara.remove_obj(self.sombra)
        if self.image not in self.registerd_shadows:
            self.registerd_shadows[self.image] = {}

        idx = self._sombras.index(1)
        if idx not in self.registerd_shadows[self.image]:
            s = Sombra(self, *self.crear_sombras())
            self.registerd_shadows[self.image][idx] = s
        else:
            s = self.registerd_shadows[self.image][idx]

        s.image.set_alpha(self.alpha)
        self.sombra = s
        Renderer.camara.add_visible(self.sombra)

    def crear_sombras(self):

        h = self.rect.h
        w = self.rect.w
        h_2 = h // 2

        t_surface = Surface((h * 2, h * 2), SRCALPHA)
        centerx = t_surface.get_width() // 4
        surface = self.image
        mascara = mask.from_surface(t_surface)
        mascara.clear()
        ensombrece = False
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
            ensombrece = True
            mascara.draw(_draw, (0, 0))
        if self._sombras[2]:
            img = self.orientar_sombra(surface, "SE")
            t_surface.blit(img, (centerx, h_2 - 4))
            t_surface.blit(self.dark_overlay(surface), (centerx, 0))
            _draw = mask.from_surface(t_surface, 100)
            ensombrece = True
            mascara.draw(_draw, (0, 0))
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
        if self._sombras[3]:
            img = self.orientar_sombra(surface, "S")
            r = img.get_rect(centerx=w // 2, y=h - 3)
            t_surface = Surface((w, h * 2), SRCALPHA)
            t_surface.blit(img, r)
            t_surface.blit(self.dark_overlay(surface), (0, 0))
            _draw = mask.from_surface(t_surface, 100)
            mascara.draw(_draw, (0, 0))
            ensombrece = True
            h_2 = 0
        if self._sombras[8]:
            img = Surface((14 if w <= 32 else w, 7 if w <= 32 else w // 2), SRCALPHA)
            dh = 16 if h > 50 else 6  # aunque esto es chapuza para el árbol.
            # debería ser alguna medida relativa a las medidas del sprite. 28/11/2022
            r = img.get_rect(centerx=w, y=h - dh)
            draw.ellipse(img, COLOR_SOMBRA, [0, 0, r.w, r.h])
            t_surface.blit(img, r)
            _draw = mask.from_surface(t_surface, 100)
            mascara.draw(_draw, (0, 0))
            h_2 = w // 2

        return h_2, t_surface, mascara, ensombrece

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
            pxarray = PixelArray(Surface((nw, h), SRCALPHA, surface))
            for y in range(h):
                dd = floor(d * (1 - (y / h)))
                for x in range(w):
                    if _mask.get_at((x, y)):
                        pxarray[x + dd, y] = COLOR_SOMBRA

        if arg == 'NO':
            pxarray = PixelArray(Surface((nw, h), SRCALPHA, surface))
            for y in range(h):
                dd = floor(d * (y / h))
                for x in range(w):
                    if _mask.get_at((x, y)):
                        pxarray[x + dd, y] = COLOR_SOMBRA

        if arg == 'SE':
            pxarray = PixelArray(Surface((nw, nh), SRCALPHA, surface))
            for y in range(h - 3):
                dd = floor(d * (1 - (y / h)))
                for x in range(w):
                    if _mask.get_at((x, y)):
                        ax = x + dd - 1
                        ay = (nh - y) - 1
                        pxarray[ax, ay] = COLOR_SOMBRA

        if arg == 'SO':
            pxarray = PixelArray(Surface((nw, nh), SRCALPHA, surface))
            for y in range(h - 5):
                dd = floor(d * (y / h))
                for x in range(w):
                    if _mask.get_at((x, y)):
                        ax = x + dd - 1
                        ay = (nh - y) - 1
                        pxarray[ax, ay] = COLOR_SOMBRA

        if arg == 'S':
            pxarray = PixelArray(Surface((w, h), SRCALPHA, surface))
            for x in range(w):
                for y in range(h - 1):
                    if _mask.get_at((x, y)):
                        n = -(x * h + y + 2)
                        ax, ay = -n // h, n % h
                        if ax < w and ay < h:
                            pxarray[ax, ay] = COLOR_SOMBRA

        if arg == 'N':
            pxarray = PixelArray(Surface((w, h), SRCALPHA, surface))
            for y in range(h):
                for x in range(w):
                    if _mask.get_at((x, y)):
                        pxarray[x, y] = COLOR_SOMBRA

        if arg == 'E':
            pxarray = PixelArray(Surface((w, h), SRCALPHA, surface))
            for x in range(w):
                for y in range(h):
                    if _mask.get_at((x, y)):
                        n = (x * w + y)
                        ax, ay = n // w, n % w
                        pxarray[ax, ay] = COLOR_SOMBRA

        if arg == 'O':
            pxarray = PixelArray(Surface((w, h), SRCALPHA, surface))
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
        pxarray = PixelArray(Surface((w, h), SRCALPHA, surface))
        _mask = mask.from_surface(surface)

        if stop == 0:
            stop = w

        for y in range(h):
            for x in range(start, stop):
                if _mask.get_at((x, y)):
                    pxarray[x, y] = COLOR_SOMBRA

        return pxarray.make_surface().convert_alpha()

    @staticmethod
    def filtrar_luces(i):
        return i not in (1, 5)

    def recibir_luz_especular(self, source):
        """
        :param source:
        :type source: LightSource
        :return: None
        """
        tolerancia = 8
        light_idx = None
        if self.proyectaSombra:
            # calcular direccion de origen
            dx = self.rect.centerx - source.rect.centerx
            dy = self.rect.centery - source.rect.centery
            self.unset_origin(source)
            self.alpha = 150
            # marcar direccion como iluminada
            if dx > 0:
                if dy > tolerancia:
                    light_idx = 6  # noreste
                elif dy < -tolerancia:
                    light_idx = 4  # sureste
                else:
                    light_idx = 1  # este
            elif dx < -tolerancia:
                if dy > tolerancia:
                    light_idx = 0  # noroeste
                elif dy < -tolerancia:
                    light_idx = 2  # suroeste
                else:
                    light_idx = 5  # oeste
            else:
                if dy > tolerancia:
                    light_idx = 7  # norte
                else:
                    light_idx = 3  # sur

        self._luces[light_idx] = 1
        self._origins[light_idx] = source
        self.update_sombra()

    def recibir_luz_solar(self, light_idx):
        self.unset_origin('Sun')
        if light_idx is not None:
            self._luces[light_idx] = 1
            self._origins[light_idx] = 'Sun'

    def unset_origin(self, source):
        while source in self._origins:
            origin_idx = self._origins.index(source)
            self._luces[origin_idx] = 0
            self._origins[origin_idx] = 0
        if any(self._origins):
            self.update_sombra()

    def desiluminar(self, source):
        if source in self._origins:
            idx = self._origins.index(source)
            self._luces[idx] = 0

    def detect_light_collition(self, dx, dy):
        for spr in Light_Group.list(self.parent.id) + Light_Group.list(self.parent.parent.id):
            spr.colisiona(self, dx, dy)

    def update_sombra(self):
        """
        generar sombra en direccion contraria a los slots iluminados
        si cambio la lista, actualizar imagen de sombra y centrar
        """
        if self._prevLuces != self._luces:
            self._prevLuces = self._luces[:]
            for i in range(0, 8):
                if self.filtrar_luces(i):
                    if (self._luces[(i + 4) % 8] - self._luces[i]) == 1:  # bool
                        self._sombras[i] = 1
                    else:
                        self._sombras[i] = 0
            else:
                if self._luces[8]:
                    self._sombras[8] = 1
                else:
                    self._sombras[8] = 0

        if any(self._sombras) and FEATURE_SOMBRAS_DINAMICAS:
            self.add_shadow()
        elif self.sombra is not None:
            # de otro modo el mob no pierde la sombra icluso si se aleja de la fuente de luz.
            Renderer.camara.remove_obj(self.sombra)

    def update(self, *args):
        if self.proyectaSombra:
            self.update_sombra()
        super().update(*args)

    def ubicar(self, dx, dy):
        super().ubicar(dx, dy)
        if self.sombra is not None:
            self.sombra.ubicar(dx, dy)

    def reubicar(self, dx, dy):
        super().reubicar(dx, dy)
        self.detect_light_collition(dx, dy)

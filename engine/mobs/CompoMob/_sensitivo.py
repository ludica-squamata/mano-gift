# noinspection PyUnresolvedReferences
from math import tan, radians
from pygame import Surface, draw, mask, transform
from ._atribuido import Atribuido


class Sensitivo(Atribuido):
    vision = None  # triangulo de la visión.
    visual_mask = None
    vx, vy = 0, 0  # posicion de la visión
    ultima_direccion = ''

    audicion = None  # circulo de la audición.
    aural_mask = None
    ax, ay = 0, 0  # posición de la audición

    perceived = None  # una lista con los interactives que el mob ve u oye

    def __init__(self, data, **kwargs):
        super().__init__(data, **kwargs)
        self.vision = self._generar_cono_visual(32 * 5)  # (data[vision])
        self.audicion = self._generar_circulo_auditivo(32 * 6)  # cheat
        self.perceived = []

    @staticmethod
    def _generar_cono_visual(largo):
        """Crea el triangulo de la visión (fg azul, bg transparente).

        Devuelve un surface."""

        def _ancho(_largo):
            an = radians(40)
            return round(_largo * round(tan(an), 2))

        ancho = _ancho(largo)

        megasurf = Surface((ancho * 2, largo))
        draw.polygon(megasurf, (0, 0, 255), [[0, 0], [ancho, largo], [ancho * 2, 0]])
        megasurf.set_colorkey((0, 0, 0))

        return megasurf

    @staticmethod
    def _generar_circulo_auditivo(radio):
        """crea un circulo auditivo, que se usa para que el mob
        detecte otros mobs y objetos"""

        surf = Surface((radio * 2, radio * 2))
        draw.circle(surf, (0, 0, 255), [radio, radio], radio, 0)
        surf.set_colorkey((0, 0, 0))
        return surf

    def _mover_triangulo_visual(self, direccion):
        """Gira el triangulo de la visión.

        Devuelve el surface del triangulo rotado, y la posicion en x e y"""
        tx, ty, tw, th = self.mapRect
        img = self.vision
        if direccion == 'abajo':
            surf = transform.flip(img, False, True)
            w, h = surf.get_size()
            y = ty + th
            x = tx + (tw / 2) - w / 2
        elif direccion == 'derecha':
            surf = transform.rotate(img, -90.0)
            w, h = surf.get_size()
            x = tx + tw
            y = ty + (th / 2) - h / 2
        elif direccion == 'izquierda':
            surf = transform.rotate(img, +90.0)
            w, h = surf.get_size()
            x = tx - w
            y = ty + (th / 2) - h / 2
        else:
            surf = img
            w, h = surf.get_size()
            y = ty - h
            x = tx + (tw / 2) - w / 2

        self.vx, self.vy = int(x), int(y)
        self.visual_mask = mask.from_surface(surf)

    def _mover_circulo_auditivo(self):
        tx, ty, tw, th = self.mapRect
        w, h = self.audicion.get_size()
        x = int(tx + (tw / 2) - (w / 2))
        y = int(ty + (th / 2) - (h / 2))

        self.ax, self.ay = x, y
        self.aural_mask = mask.from_surface(self.audicion)

    def ver(self):
        """Realiza detecciones con la visión del mob"""

        direccion = self.direccion
        if direccion == 'ninguna':
            direccion = self.ultima_direccion
        else:
            self.ultima_direccion = self.direccion

        self._mover_triangulo_visual(direccion)
        lista = self.stage.interactives
        idx = lista.index(self)
        for obj in lista[0:idx]+lista[idx+1:]:
            x, y = self.vx - obj.mapRect.x, self.vy - obj.mapRect.y
            if obj.mask.overlap(self.visual_mask, (x, y)):
                self.perceived.append(obj)

    def oir(self):
        self._mover_circulo_auditivo()
        lista = self.stage.interactives
        idx = lista.index(self)
        for obj in lista[0:idx]+lista[idx+1:]:
            x, y = self.ax - obj.mapRect.x, self.ay - obj.mapRect.y
            if obj.mask.overlap(self.aural_mask, (x, y)) and any([
                getattr(obj, 'moviendose',False),  # getattr() es necesario
                getattr(obj, 'hablando', False)]):  # porque Prop no tiene
                self.perceived.append(obj)  # ni 'moviendose' ni 'hablando'

    def update(self, *args):
        super().update(*args)
        self.perceived.clear()
        self.ver()
        self.oir()

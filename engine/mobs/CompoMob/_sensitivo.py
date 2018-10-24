from pygame import Surface, draw, mask as mask_module, transform
from engine.globs.event_dispatcher import EventDispatcher
from engine.globs.azoe_group import AzoeBaseSprite
from ._atribuido import Atribuido
from math import tan, radians


class Sight(AzoeBaseSprite):
    ultima_direccion = ''
    mask = None
    # la mascara se crea al rotarse, por eso no está en el init.

    def __init__(self, parent, lenght):
        image = self._create(lenght)
        rect = image.get_rect()
        super().__init__(parent, 'vision', image, rect)

    @staticmethod
    def _create(largo):
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

    def move(self, direccion):
        """Gira el triangulo de la visión.

        Devuelve el surface del triangulo rotado, y la posicion en x e y"""
        tx, ty, tw, th = self.parent.mapRect
        if direccion == 'abajo':
            surf = transform.flip(self.image, False, True)
            w, h = surf.get_size()
            y = ty + th
            x = tx + (tw / 2) - w / 2
        elif direccion == 'derecha':
            surf = transform.rotate(self.image, -90.0)
            w, h = surf.get_size()
            x = tx + tw
            y = ty + (th / 2) - h / 2
        elif direccion == 'izquierda':
            surf = transform.rotate(self.image, +90.0)
            w, h = surf.get_size()
            x = tx - w
            y = ty + (th / 2) - h / 2
        else:
            surf = self.image.copy()
            w, h = surf.get_size()
            y = ty - h
            x = tx + (tw / 2) - w / 2

        self.rect.topleft = int(x), int(y)
        self.mask = mask_module.from_surface(surf)

    def __call__(self):
        """Realiza detecciones con la visión del mob"""

        direccion = self.parent.direccion
        if direccion == 'ninguna':
            direccion = self.ultima_direccion
        else:
            self.ultima_direccion = self.parent.direccion

        self.move(direccion)
        mapa = self.parent.mapa_actual
        lista = mapa.properties.sprites() if (mapa is not None) and (len(mapa.properties.sprites()) > 0) else [
            self.parent]
        if self.parent in lista:
            idx = lista.index(self.parent)
        else:
            idx = 0
        for obj in lista[0:idx] + lista[idx + 1:]:
            x, y = self.rect.x - obj.mapRect.x, self.rect.y - obj.mapRect.y
            if obj.mask.overlap(self.mask, (x, y)):
                self.parent.perceived['seen'].append(obj)


class Hearing(AzoeBaseSprite):
    def __init__(self, parent):
        super().__init__(parent, 'audicion')
        EventDispatcher.register(self.listener, 'SoundEvent')

    def listener(self, event):
        # acá se podría negar la recepción del sonido por la distancia
        # pero por el momento con que se escuche el sonido basta.
        self.parent.perceived['heard'].append(event)


class Touch(AzoeBaseSprite):
    def __init__(self, parent):
        super().__init__(parent, 'Tacto', rect=parent.rect)

    def __call__(self):
        mapa = self.parent.mapa_actual
        lista = mapa.properties.sprites() if (mapa is not None) and (len(mapa.properties.sprites()) > 0) else [
            self.parent]

        lista.reverse()
        if self.parent in lista:
            idx = lista.index(self.parent)
        else:
            idx = 0
        for obj in lista[0:idx] + lista[idx + 1:]:
            if self.rect.colliderect(obj.rect):
                if obj.accionable:
                    self.parent.perceived['touched'].append(obj)
                else:
                    self.parent.perceived['felt'].append(obj)


class Sensitivo(Atribuido):
    perceived = None  # un diccionario con los interactives que el mob ve, oye, o toca

    def __init__(self, data, **kwargs):
        super().__init__(data, **kwargs)
        self.vista = Sight(self, 32 * 5)  # (data[vision])
        self.oido = Hearing(self)
        self.tacto = Touch(self)
        self.perceived = {"heard": [], "seen": [], "touched": [], "felt": []}

    def update(self, *args):
        super().update(*args)
        for sense in self.perceived:
            self.perceived[sense].clear()
        self.vista()
        self.tacto()

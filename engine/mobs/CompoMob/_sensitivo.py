from pygame import Surface, draw, mask as mask_module, transform
from engine.globs.event_dispatcher import EventDispatcher
from engine.globs.azoe_group import AzoeBaseSprite
from ._caracterizado import Caracterizado
from math import tan, radians, sqrt


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

        ancho = round(largo * round(tan(radians(40)), 2))
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
        else:  # direccion == 'arriba'
            surf = self.image.copy()
            w, h = surf.get_size()
            y = ty - h
            x = tx + (tw / 2) - w / 2

        self.rect.topleft = int(x), int(y)
        self.mask = mask_module.from_surface(surf)

    def _translate(self):
        orientacion = self.parent.head_direction
        direccion = self.parent.body_direction
        sight_direction = None
        if orientacion == 'front':
            sight_direction = direccion
        elif orientacion == 'left':
            if direccion == 'abajo':
                sight_direction = 'iquierda'
            elif direccion == 'arriba':
                sight_direction = 'derecha'
            elif direccion == 'izquierda':
                sight_direction = 'arriba'
            elif direccion == 'derecha':
                sight_direction = 'abajo'

        elif orientacion == 'right':
            if direccion == 'abajo':
                sight_direction = 'derecha'
            elif direccion == 'arriba':
                sight_direction = 'izquierda'
            elif direccion == 'izquierda':
                sight_direction = 'abajo'
            elif direccion == 'derecha':
                sight_direction = 'arriba'

        return sight_direction

    def __call__(self):
        """Realiza detecciones con la visión del mob"""

        direccion = self._translate()
        self.move(direccion)
        mapa = self.parent.mapa_actual
        sprites = mapa.properties.sprites() + mapa.parent.properties.sprites()
        lista = sprites if (mapa is not None) and (len(sprites) > 0) else [self.parent]
        if self.parent in lista:
            idx = lista.index(self.parent)
        else:
            idx = 0
        for obj in lista[0:idx] + lista[idx + 1:]:
            x, y = self.rect.x - obj.mapRect.x, self.rect.y - obj.mapRect.y
            ox, oy = obj.mapRect.topleft
            sx, sy = self.parent.mapRect.topleft
            distance = round(sqrt(abs(oy - sy)**2 + abs(ox - sx)**2))
            if obj.mask.overlap(self.mask, (x, y)):
                self.parent.perceived['seen'].append(obj)
            if distance < 64:
                self.parent.perceived['close'].append(obj)


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

    def __call__(self, passive=True):
        mapa = self.parent.mapa_actual
        sprites = mapa.properties.sprites() + mapa.parent.properties.sprites()
        lista = sprites if (mapa is not None) and (len(sprites) > 0) else [self.parent]

        lista.reverse()
        idx = -1 if self.parent not in lista else lista.index(self.parent)  # it would be the same as str.find()
        for obj in lista[0:idx] + lista[idx + 1:]:
            if self.rect.colliderect(obj.rect):
                if not passive:
                    self.parent.perceived['touched'].append(obj)
                else:
                    self.parent.perceived['felt'].append(obj)

    def touch(self):
        self.__call__(passive=False)


class Sensitivo(Caracterizado):
    perceived = None  # un diccionario con los interactives que el mob ve, oye, o toca

    def __init__(self, data, **kwargs):
        super().__init__(data, **kwargs)
        self.vista = Sight(self, 32 * self['Vista'])
        self.oido = Hearing(self)
        self.tacto = Touch(self)
        self.perceived = {"heard": [], "seen": [], "touched": [], "felt": [], "close": []}
        self.touch = self.tacto.touch

    def update(self, *args):
        super().update(*args)
        for sense in self.perceived:
            self.perceived[sense].clear()
        self.vista()
        self.tacto()

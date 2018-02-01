# noinspection PyUnresolvedReferences
from math import tan, radians
from pygame import Surface, draw, mask as mask_module, transform
# mask entra como mask_module para no generar conflictos.
from pygame.sprite import Sprite
from ._atribuido import Atribuido

class Sense(Sprite):
    mask = None
    # la mascara se crea al rotarse, por eso no está en el init.

    def __init__(self, parent, name, image):
        super().__init__()
        self.parent = parent
        # parent es el mob al cual este sentido pertenece
        self.nombre = name
        # muchas otras clases pieden "self.nombre" pero no piden "self.name".
        # Esto es para evitar conflictos.
        self.image = image
        self.rect = self.image.get_rect()


class Sight(Sense):
    ultima_direccion = ''

    def __init__(self, parent, lenght):
        image = self._create(lenght)
        super().__init__(parent, 'vision', image)

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
        lista = self.parent.stage.properties.sprites()
        idx = lista.index(self.parent)
        for obj in lista[0:idx]+lista[idx+1:]:
            x, y = self.rect.x - obj.mapRect.x, self.rect.y - obj.mapRect.y
            if obj.mask.overlap(self.mask, (x, y)):
                self.parent.perceived['seen'].append(obj)


class Hearing(Sense):
    def __init__(self, parent, radius):
        image = self._create(radius)
        super().__init__(parent, 'audicion', image)
    
    @staticmethod
    def _create(radio):
        """crea un circulo auditivo, que se usa para que el mob
        detecte otros mobs y objetos"""

        surf = Surface((radio * 2, radio * 2))
        draw.circle(surf, (0, 0, 255), [radio, radio], radio, 0)
        surf.set_colorkey((0, 0, 0))
        return surf

    def move(self):
        tx, ty, tw, th = self.parent.mapRect
        w, h = self.image.get_size()
        x = int(tx + (tw / 2) - (w / 2))
        y = int(ty + (th / 2) - (h / 2))

        self.rect.topleft = int(x), int(y)
        self.mask = mask_module.from_surface(self.image)

    def __call__(self):
        self.move()
        lista = self.parent.stage.properties.sprites()
        idx = lista.index(self.parent)
        for obj in lista[0:idx]+lista[idx+1:]:
            x, y = self.rect.x - obj.mapRect.x, self.rect.y - obj.mapRect.y
            if obj.mask.overlap(self.mask, (x, y)) and any([
                getattr(obj, 'moviendose',False),  # getattr() es necesario
                getattr(obj, 'hablando', False)]):  # porque Prop no tiene
                self.parent.perceived['heard'].append(obj)  # ni 'moviendose' ni 'hablando'


class Sensitivo(Atribuido):
    perceived = None  # un diccionario con los interactives que el mob ve u oye

    def __init__(self, data, **kwargs):
        super().__init__(data, **kwargs)
        self.vision = Sight(self, 32 * 5)  # (data[vision])
        self.audicion = Hearing(self, 32 * 6)  # cheat
        self.perceived = {"heard":[], "seen":[]}

    def update(self, *args):
        super().update(*args)
        self.perceived['seen'].clear()
        self.perceived['heard'].clear()
        self.vision()
        self.audicion()

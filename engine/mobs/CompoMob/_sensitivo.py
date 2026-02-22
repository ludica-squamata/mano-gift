from pygame import Surface, draw, mask as mask_module, transform, SRCALPHA
from engine.globs.event_dispatcher import EventDispatcher
from engine.globs.azoe_group import AzoeBaseSprite
from engine.globs.constantes import DEBUG_VISION
from engine.libs.mersenne_twister import randint
from engine.base.azoe_sprite import AzoeSprite
from engine.globs.renderer import Renderer
from ._caracterizado import Caracterizado
from engine.globs.renderer import Camara
from math import tan, radians, sqrt
import sys


class Sight(AzoeBaseSprite):
    ultima_direccion = 'abajo'
    mask = None

    # la mascara se crea al rotarse, por eso no está en el init.

    def __init__(self, parent, lenght):
        image = self._create(lenght)
        rect = image.get_rect()
        super().__init__(parent, 'vision', image, rect)
        self.sprite = SightSprite(self.parent, image, 0, 0)
        if DEBUG_VISION is True and 'pydevd' in sys.modules:
            if self.sprite not in Renderer.camara.real.sprites():
                Renderer.camara.add_real(self.sprite)
        self.rotate(self._translate())

    @staticmethod
    def _create(largo):
        """Crea el triangulo de la visión (fg azul, bg transparente).
        Devuelve un surface."""
        color = randint(0, 255), randint(0, 255), randint(0, 255)
        ancho = round(largo * round(tan(radians(40)), 2))
        megasurf = Surface((ancho * 2, largo), SRCALPHA)
        draw.polygon(megasurf, color, [[0, 0], [ancho, largo], [ancho * 2, 0]])

        return megasurf

    def rotate(self, direccion):
        """Gira el triangulo de la visión.
        Reestablece los puntos x, y del origen del triángulo, aunque esto solo se utiliza en el debugging."""
        if direccion == 'abajo':
            surf = transform.flip(self.image, False, True)
            self.sprite.image = surf
            rect = self.sprite.image.get_rect(midtop=[16, 16])
            self.sprite.x = rect.x
            self.sprite.y = rect.y

        elif direccion == 'derecha':
            surf = transform.rotate(self.image, -90.0)
            self.sprite.image = surf
            rect = self.sprite.image.get_rect(midleft=[16, 16])
            self.sprite.x = rect.x
            self.sprite.y = rect.y

        elif direccion == 'izquierda':
            surf = transform.rotate(self.image, +90.0)
            self.sprite.image = surf
            rect = self.sprite.image.get_rect(midright=[16, 16])
            self.sprite.x = rect.x
            self.sprite.y = rect.y

        else:  # direccion == 'arriba'
            surf = self.image.copy()
            self.sprite.image = surf
            rect = self.sprite.image.get_rect(midbottom=[16, 16])
            self.sprite.x = rect.x
            self.sprite.y = rect.y

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
        if direccion != self.ultima_direccion:
            self.ultima_direccion = direccion
            self.rotate(direccion)

        lista = []
        if Camara.current_map is not None:
            lista = Camara.current_map.properties.sprs()
            lista.extend(Camara.current_map.parent.points_of_interest.get(tuple(Camara.current_map.adress), []))

        if self.parent in lista:
            idx = lista.index(self.parent)
        else:
            idx = 0
        for obj in lista[0:idx] + lista[idx + 1:]:
            x, y = self.parent.x - obj.x, self.parent.y - obj.y
            ox, oy = obj.x, obj.y
            sx, sy = self.parent.x, self.parent.y
            distance = round(sqrt(abs(oy - sy) ** 2 + abs(ox - sx) ** 2))
            if obj.mask.overlap(self.mask, (x, y)):
                self.parent.perceived['seen'].append(obj)
            if distance < 64:
                self.parent.perceived['close'].append(obj)


class Hearing(AzoeBaseSprite):
    def __init__(self, parent):
        super().__init__(parent, 'audicion')
        EventDispatcher.register(self.listener, 'SoundEvent')

    def listener(self, event):
        if event.origin is not self.parent:
            ox, oy = event.origin.x, event.origin.y
            sx, sy = self.parent.x, self.parent.y
            distance = round(sqrt(abs(oy - sy) ** 2 + abs(ox - sx) ** 2))
        else:
            return
            # the mob will always hear itself.

        if distance != 0:  # prevents a weird crash.
            intensity = event.data['intensity'] / distance ** 2
            if intensity > 1E-12:
                # inverse-square law: the intensity of a sound decreses with distance;
                # weak sounds produced far away from the mob won't be heard by it.
                # 1E-12 W/m**2 is the Threshold of human hearing.
                event.data['intensity'] = round(intensity, 6)
                self.parent.perceived['heard'].append(event.origin)
                # print(event.origin, intensity)
        # aunque habría que ver si "podes" escuchar un sonido separándolo del background noise.
        # para que se pueda escuchar por encima del BgN, log(signal/noise) debe ser mayor que 0.


class Touch(AzoeBaseSprite):
    def __init__(self, parent):
        super().__init__(parent, 'Tacto', rect=parent.rect)

    def __call__(self, passive=True):
        lista = []
        if Camara.current_map is not None:
            lista = Camara.current_map.properties.sprs() + Camara.current_map.parent.properties.sprs()
            lista.reverse()

        while self.parent in lista:
            lista.remove(self.parent)
        for obj in lista:
            if self.rect.colliderect(obj.rect):
                if not passive:
                    self.parent.perceived['touched'].append(obj)
                    if obj.accionable:
                        # should Movible Props have an action?
                        obj.action(self.parent)
                else:
                    self.parent.perceived['felt'].append(obj)

    def touch(self):
        self.__call__(passive=False)


class Sensitivo(Caracterizado):
    perceived = None  # un diccionario con los interactives que el mob ve, oye, o toca

    def __init__(self, parent, data, **kwargs):
        super().__init__(parent, data, **kwargs)
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


class SightSprite(AzoeSprite):
    """Una clase muy sencilla que tan solo representa la visión de los mobs para propósitos de debugging."""

    def __repr__(self):
        return f'Sight of {self.parent.nombre}'

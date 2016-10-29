from pygame import Mask, Surface, Rect
from engine.globs import MobGroup
from engine.globs.eventDispatcher import EventDispatcher
from engine.base import AzoeSprite
from engine.globs.renderer import Renderer
import sys


class Salida:
    tipo = 'Salida'
    nombre = ''
    dest = ''  # string, mapa de destino.
    link = ''  # string, nombre de la entrada en dest con la cual conecta
    mask = None
    sprite = None
    solido = False

    def __init__(self, nombre, data):
        self.nombre = self.tipo + '.' + nombre
        x, y, w, h = data['rect']
        self.mapRect = Rect(x, y, w, h)
        self.dest = data['dest']
        self.link = data['link']  # string, nombre de la entrada en dest con la cual conecta
        self.direcciones = data.get('direcciones', ['arriba', 'abajo', 'izquierda', 'derecha'])
        self.mask = Mask((w, h))
        self.mask.fill()
        if 'pydevd' in sys.modules:
            self.sprite = SpriteSalida(self.nombre, x, y, w, h)
            Renderer.camara.add_real(self.sprite)

    def update(self):
        for mob in MobGroup:
            dx, dy = mob.direcciones[mob.direccion]
            dx *= mob.velocidad
            dy *= mob.velocidad
            if mob.colisiona(self, dx, dy) and mob.direccion in self.direcciones:
                EventDispatcher.trigger('CambiarMapa', 'Salida', {"mob": mob, 'dest': self.dest, 'link': self.link})

    def __repr__(self):
        return self.nombre


class SpriteSalida(AzoeSprite):
    """Intented only to debugging"""

    def __init__(self, nombre, x, y, w, h):
        img = Surface((w, h))
        img.fill((255, 255, 0))
        self.nombre = nombre + '.Sprite'

        super().__init__(imagen=img, x=x, y=y, z=5000)

from pygame import Mask, Surface, Rect
from engine.globs import Mob_Group
from engine.globs.eventDispatcher import EventDispatcher
from engine.base import AzoeSprite
from engine.globs.renderer import Renderer
import sys


class Salida:
    tipo = 'Salida'
    nombre = ''
    chunk = ''  # string, mapa de destino.
    link = ''  # string, nombre de la entrada en dest con la cual conecta
    mask = None
    sprite = None
    solido = False

    def __init__(self, nombre, stage, rect, chunk, entrada, direcciones):
        self.nombre = self.tipo + '.' + nombre
        self.mapRect = Rect(*rect)
        self.chunk = chunk
        self.target_stage = stage
        self.link = entrada  # string, nombre de la entrada en dest con la cual conecta
        self.direcciones = direcciones
        self.mask = Mask(self.mapRect.size)
        self.mask.fill()
        # if 'pydevd' in sys.modules:
        self.sprite = SpriteSalida(self.nombre, *self.mapRect)
        Renderer.camara.add_visible(self.sprite)

    def update(self):
        for mob in Mob_Group:
            dx, dy = mob.direcciones[mob.direccion]
            dx *= -mob.velocidad
            dy *= -mob.velocidad
            if mob.colisiona(self, dx, dy):
                EventDispatcher.trigger('SetMap', 'Salida', {'mob': mob,
                                                             'target_stage': self.target_stage,
                                                             'target_chunk': self.chunk,
                                                             'target_entrada': self.link,
                                                             'pos': self.mapRect.center})

    def __repr__(self):
        return self.nombre


class SpriteSalida(AzoeSprite):
    """Intented only to debugging"""

    def __init__(self, nombre, x, y, w, h):
        img = Surface((w, h))
        img.fill((255, 255, 0))
        self.nombre = nombre + '.Sprite'

        super().__init__(imagen=img, x=x, y=y, z=5000)

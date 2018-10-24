from engine.globs.eventDispatcher import EventDispatcher
from engine.globs.gameState import GameState
from pygame import Mask, Surface, Rect
from engine.base import AzoeSprite
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
        self.flag_name = nombre+'.triggered'
        self.mapRect = Rect(*rect)
        self.chunk = chunk
        self.target_stage = stage
        self.link = entrada  # string, nombre de la entrada en dest con la cual conecta
        self.direcciones = direcciones
        self.mask = Mask(self.mapRect.size)
        self.mask.fill()
        GameState.set(self.flag_name, False)
        if 'pydevd' in sys.modules:
            self.sprite = SpriteSalida(self.nombre, *self.mapRect)

    def trigger(self, mob):
        # este método, que antes era update(), toma los datos de la salida
        # y dispara el evento. Ya no se fija qué mob la pisa.
        data = {'mob': mob,
                'target_stage': self.target_stage,
                'target_chunk': self.chunk,
                'target_entrada': self.link}

        EventDispatcher.trigger('SetMap', 'Salida', data)
        GameState.set(self.flag_name, True)

    def __repr__(self):
        return self.nombre


class SpriteSalida(AzoeSprite):
    """Intented only for debugging"""

    def __init__(self, nombre, x, y, w, h):
        img = Surface((w, h))
        img.fill((255, 255, 0))
        self.nombre = nombre + '.Sprite'

        super().__init__(imagen=img, x=x, y=y, z=5000)

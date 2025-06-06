from engine.globs.event_dispatcher import EventDispatcher
from engine.globs.game_state import Game_State
from engine.globs.renderer import Renderer
from pygame import Mask, Surface
from engine.base import AzoeSprite
import sys


class Salida:
    tipo = 'Salida'
    nombre = ''
    chunk = ''
    entrada = ''  # string, nombre de la entrada en dest con la cual conecta
    mask = None
    sprite = None
    solido = False

    def __init__(self, nombre, id, stage, rect, chunk, entrada, direcciones, accion, color):
        self.nombre = self.tipo + '.' + nombre
        self.flag_name = self.nombre + '.triggered'
        self.x, self.y, w, h = rect
        self.chunk = chunk  # The chunk where the Exit is on, or it's adress if it is not loaded yet.
        self.target_stage = stage
        self.entrada = entrada  # string, nombre de la entrada en dest con la cual conecta
        self.direcciones = direcciones
        self.mask = Mask(rect.size)
        self.mask.fill()
        self.action_trigger = accion
        self.id = id
        if 'pydevd' in sys.modules and bool(chunk):
            self.sprite = SpriteSalida(chunk, self.nombre, self.x, self.y, w, h, color)
            chunk.add_property(self.sprite, 10000)
            Renderer.camara.add_real(self.sprite)

    def trigger(self, mob, accion='caminar'):
        # este método, que antes era update(), toma los datos de la salida
        # y dispara el evento. Ya no se fija qué mob la pisa.
        data = {'mob': mob,
                'target_stage': self.target_stage,
                'target_chunk': self.chunk,
                'target_entrada': self.entrada}

        trigger = False
        if mob.body_direction in self.direcciones or not len(self.direcciones):
            if self.action_trigger == "caminar" and mob.moviendose:
                trigger = True
            elif accion == self.action_trigger:
                trigger = True

        if trigger:
            EventDispatcher.trigger('SetMap', 'Salida', data)
            Game_State.set2(self.flag_name)

    def __repr__(self):
        return self.nombre


class SpriteSalida(AzoeSprite):
    """Intented only for debugging"""

    def __init__(self, parent, nombre, x, y, w, h, color):
        img = Surface((w, h))
        img.fill(color)
        self.nombre = nombre + '.Sprite'

        super().__init__(parent, imagen=img, x=x, y=y, z=5000)

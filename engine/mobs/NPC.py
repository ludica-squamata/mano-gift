from engine.globs.eventDispatcher import EventDispatcher
from .CompoMob import Autonomo, Parlante
from .mob import Mob


class NPC(Parlante, Autonomo, Mob):
    memoria = None

    def __init__(self, nombre, x, y, data, recuerdos=None):
        self.nombre = nombre
        self.memoria = {'nombre': self.nombre}
        if recuerdos is not None:
            self.memoria.update(recuerdos)
        EventDispatcher.register(self.save_memories, 'Save')
        super().__init__(data, x, y)

    # noinspection PyMethodOverriding
    def mover(self):
        if not self.hablando:
            super().mover()

    def save_memories(self, event):
        EventDispatcher.trigger(event.tipo + 'Data', 'NPC', self.memoria)

from .CompoMob import Autonomo, Parlante
from .mob import Mob


class NPC(Parlante, Autonomo, Mob):
    def __init__(self, nombre, x, y, data):
        self.nombre = nombre
        super().__init__(data, x, y)

    # noinspection PyMethodOverriding
    def mover(self):
        if not self.hablando:
            super().mover()

    def update(self):
        if not self.hablando:
            super().update()

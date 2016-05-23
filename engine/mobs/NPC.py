from .CompoMob import Autonomo, Parlante
from .mob import Mob


class NPC(Parlante, Autonomo, Mob):
    hablando = False
    hablante = True
    image = None  # para corregir un advertencia en PyCharm

    def __init__(self, nombre, x, y, data):
        self.nombre = nombre
        super().__init__(data, x, y)

    def mover(self):
        if not self.hablando:
            super().mover()

    def iniciar_dialogo(self, direccion):
        self.hablando = True
        self.cambiar_direccion(direccion)
        self.image = self.images['S' + direccion]
        
    def update(self):
        if not self.hablando:
            super().update()

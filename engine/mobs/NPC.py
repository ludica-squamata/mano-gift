from .CompoMob import Autonomo, Parlante
from engine.misc import Resources as Rs
from engine.globs import ModData as Md
from .mob import Mob


class NPC(Autonomo, Parlante, Mob):
    hablando = False
    hablante = True
    image = None  # para corregir un advertencia en PyCharm

    def __init__(self, nombre, x, y, data):
        self.nombre = nombre
        self.dialogo = Rs.abrir_json(Md.dialogos + data['dialog'])
        super().__init__(data, x, y)

    def mover(self):
        if not self.hablando:
            super().mover()

    def iniciar_dialogo(self, direccion):
        self.hablando = True
        self.cambiar_direccion(direccion)
        self.image = self.images['S' + direccion]

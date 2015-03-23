from engine.misc import Resources as r
from engine.globs import ModData as MD
from .CompoMob import Parlante
from .NPC import NPC


class NPCSocial(NPC, Parlante):
    def __init__(self, nombre, x, y, data):
        super().__init__(nombre, x, y, data)
        self.hablante = True
        self.dialogo = r.abrir_json(MD.dialogos + data['dialog'])

    def mover(self, dx, dy):
        #if not self.hablando:
        #    return super().mover(dx, dy)
        pass
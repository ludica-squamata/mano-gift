from engine.misc import Resources as r
from engine.globs import ModData as MD
from .CompoMob import Parlante
from .NPC import NPC


class NPCSocial(NPC, Parlante):
    def __init__(self, nombre, x, y, data):
        super().__init__(nombre, x, y, data)
        self.hablante = True
        self.dialogo = r.abrir_json(MD.dialogos + data['dialog'])

    def mover(self):
        if not self.hablando:
            super().mover()
    
    def iniciar_dialogo(self,inter,direccion):
        self.cambiar_direccion(direccion)
        self.image = self.images['S'+direccion]
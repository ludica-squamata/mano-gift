from .NPC import NPC
from .CompoMob import Parlante

class NPCSocial(NPC,Parlante):
    def __init__(self,nombre,ruta_img,stage,x,y,data):
        super().__init__(nombre,ruta_img,stage,x,y,data)
        self.establecer_dialogos(data)
    
    def mover(self):
        if not self.hablando:
            return super().mover()
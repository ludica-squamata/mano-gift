from engine.misc import Resources as r
from engine.globs import ModData as MD

class Atribuido:
    fuerza = 0 # capacidad del mob para empujar cosas.
    velocidad = 1 # en pixeles por frame
    salud_max = 0 #salud máxima
    salud_act = 0 #salud actual
    
    def __init__(self,*args,**kwargs):
        self.velocidad = self.data['velocidad']
        self.fuerza = self.data['fuerza']
        self.salud_max = self.data['salud']
        self.salud_act = self.salud_max
        super().__init__(*args,**kwargs)
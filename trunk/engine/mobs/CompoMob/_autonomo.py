from engine.mobs.scripts import movimiento
from ._sensitivo import Sensitivo

class Autonomo (Sensitivo): #tiene que poder ver para ser autónomo
    AI = None # determina cómo se va a mover el mob
    objetivo = None # el mob al que este cazador está persiguiendo
    
    def __init__(self,*args,**kwargs):
        AI = args[0]['AI']
        
        if AI == "wanderer":
            self.AI = movimiento.AI_wander # function alias!
        
        self._AI = self.AI #copia de la AI original
        super().__init__(*args,**kwargs)
    
    def determinar_accion(self,mobs_detectados):
        '''Cambia la AI, la velocidad y la visión de un mob
        si su objetivo está entre los detectados'''
        
        if self.objetivo in mobs_detectados:
            self.velocidad = 2
            self.AI = movimiento.AI_pursue
            self.vision = self.cir_vis
            self.mover_vis = self.mover_cir_vis
        else:
            #Esto permite acercarse hasta la espalda del mob, a lo MGS
            self.velocidad = 1
            self.AI = self._AI
            self.vision = self.tri_vis
            self.mover_vis = self.mover_tri_vis
            
class Autonomo:
    AI = None # determina cómo se va a mover el mob
    objetivo = None # el mob al que este cazador está persiguiendo
            
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
            
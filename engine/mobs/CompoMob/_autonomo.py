from engine.mobs.scripts import movimiento

class Autonomo:
    AI = None # determina cómo se va a mover el mob
    objetivo = None # el mob al que este cazador está persiguiendo
    
    def establecer_AI(self,data,x,y):
        self.AI = data['AI']
        
        if self.AI == "wanderer":
            self.AI = movimiento.AI_wander # function alias!
            
        elif self.AI == "patrol":
            inicio = x,y
            self.reversa = data['reversa']
            for x,y in data['camino']:
                destino = x,y
                camino = movimiento.generar_camino(inicio,destino,self.stage.grilla)
                ruta = movimiento.simplificar_camino(camino)
                self.camino.extend(ruta)
                inicio = x,y
            
            self.AI = movimiento.AI_patrol # function alias!
        
        self._AI = self.AI #copia de la AI original
        self._camino = self.camino
    
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
            
from engine.mobs.scripts.dialogo import Dialogo
from engine.globs import EngineData as ED

class Parlante:
    interlocutor = None # para que el mob sepa con quién está hablando, si lo está
    conversaciones = [] # registro de los temas conversados
    hablante = True
    hablando = False
    
    def hablar(self):
        x,y = self.direcciones[self.direccion]
        sprite = self._interactuar_mobs(x,y)
        if sprite != None:
            if sprite.hablante:
                self.interlocutor = sprite
                self.interlocutor.hablando = True
                ED.DIALOG = Dialogo(self.interlocutor.dialogo)
                return True
        return False
from engine.mobs.CompoMob import Atribuido
from engine.mobs.scripts.dialogo import Dialogo
from engine.globs import EngineData as ED


class Parlante(Atribuido):
    interlocutor = None  # para que el mob sepa con quién está hablando, si lo está
    conversaciones = []  # registro de los temas conversados
    hablante = True
    hablando = False

    def hablar(self, sprite):
        if sprite is not None:
            if sprite.hablante:
                self.interlocutor = sprite
                self.interlocutor.hablando = True
                sprite.interlocutor = self
                ED.DIALOG = Dialogo(sprite.dialogo,self,sprite)
                return True
        return False
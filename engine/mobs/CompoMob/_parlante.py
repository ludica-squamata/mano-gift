from ._atribuido import Atribuido
from engine.IO.dialogo import Dialogo
from engine.globs import EngineData as Ed
from engine.UI.circularmenus import DialogCircularMenu


class Parlante(Atribuido):
    interlocutor = None  # para que el mob sepa con quién está hablando, si lo está
    conversaciones = []  # registro de los temas conversados
    hablante = True

    def hablar(self, sprite):
        if sprite.hablante:
            self.interlocutor = sprite
            sprite.interlocutor = self
            Ed.DIALOG = Dialogo(sprite.dialogo, self, sprite)

    def elegir_tema(self, sprite):
        if sprite.hablante:
            self.interlocutor = sprite
            sprite.interlocutor = self
            Ed.DIALOG = DialogCircularMenu()

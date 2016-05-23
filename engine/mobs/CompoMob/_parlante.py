from engine.UI.circularmenus import DialogCircularMenu
from engine.globs import EngineData as Ed, ModData as Md
from engine.misc import Resources as Rs
from engine.IO.dialogo import Dialogo
from ._atribuido import Atribuido


class Parlante(Atribuido):
    interlocutor = None  # para que el mob sepa con quién está hablando, si lo está
    conversaciones = []  # registro de los temas conversados
    hablante = True

    def __init__(self, *args, **kwargs):
        if 'dialog' in args[0]:
            args[0]['dialog'] = Rs.abrir_json(Md.dialogos + args[0]['dialog'])
        super().__init__(*args, **kwargs)

    def hablar(self, sprite):
        if sprite.hablante:
            self.interlocutor = sprite
            sprite.interlocutor = self
            Ed.DIALOG = Dialogo(sprite.dialogo, self, sprite)

    def elegir_tema(self, sprite):
        if sprite.hablante:
            self.interlocutor = sprite
            sprite.interlocutor = self
            Ed.DIALOG = DialogCircularMenu(sprite, self)

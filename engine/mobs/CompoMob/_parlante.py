from engine.UI.circularmenus import DialogCircularMenu
from engine.globs import EngineData, ModData as Md
from engine.misc import Resources as Rs, ReversibleDict
from engine.IO.dialogo import Dialogo
from ._movil import Movil


class Parlante(Movil):
    interlocutor = None  # para que el mob sepa con quién está hablando, si lo está
    conversaciones = []  # registro de los temas conversados
    hablante = True
    hablando = False

    def __init__(self, data, x, y, **kwargs):
        super().__init__(data, x, y, **kwargs)
        if 'states' in data:
            if 'dialog' in data['states'][0]:
                nombre = data['states'][0]['dialog']
                data['states'][0]['dialog'] = Rs.abrir_json(Md.dialogos + nombre)

    def hablar(self, sprite):
        if sprite.hablante:
            self.interlocutor = sprite
            sprite.interlocutor = self
            EngineData.DIALOG = Dialogo(sprite.dialogo, self, sprite)

    def elegir_tema(self, sprite):
        if sprite.hablante:
            self.interlocutor = sprite
            sprite.interlocutor = self
            opuestos = ReversibleDict(arriba='abajo', izquierda='derecha')
            sprite.cambiar_direccion(opuestos[self.direccion])

            locutores = [self, sprite]
            for loc in locutores:
                loc.hablando = True
                loc.detener_movimiento()

            # éste output es porque el héroe inicia diálogo
            # si fuere el NPC via IA, el output, sería:
            # Ed.DIALOG = Dialogo(sprite.dialogo, *locutores)
            EngineData.DIALOG = DialogCircularMenu(sprite, self)

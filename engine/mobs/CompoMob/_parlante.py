from engine.UI.circularmenus import DialogCircularMenu
from engine.globs import EngineData as Ed, ModData as Md
from engine.misc import Resources as Rs
from engine.IO.dialogo import Dialogo
from ._movil import Movil


class Parlante(Movil):
    interlocutor = None  # para que el mob sepa con quién está hablando, si lo está
    conversaciones = []  # registro de los temas conversados
    hablante = True
    hablando = False

    def __init__(self, *args, **kwargs):
        if 'states' in args[0]:
            if 'dialog' in args[0]['states'][0]:
                nombre = args[0]['states'][0]['dialog']
                args[0]['states'][0]['dialog'] = Rs.abrir_json(Md.dialogos + nombre)
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
            x, y = self.direcciones[self.direccion]

            inter_dir = ''
            self_dir = ''
            # quisiera definir "opuestos" sin hacer este if elif
            # algo aprecido a "not True = False"
            if x:
                if x > 0:
                    inter_dir = 'izquierda'
                    self_dir = 'derecha'
                else:
                    inter_dir = 'derecha'
                    self_dir = 'izquierda'
            elif y:
                if y > 0:
                    inter_dir = 'arriba'
                    self_dir = 'abajo'
                else:
                    inter_dir = 'abajo'
                    self_dir = 'arriba'

            # y a partir de acá, hacer un for interlocutor...
            self.cambiar_direccion(self_dir)
            sprite.cambiar_direccion(inter_dir)
            self.hablando = True
            sprite.hablando = True

            # éste output es porque el héroe inicia diálogo
            # si fuere el NPC via IA, el output, sería:
            # Ed.DIALOG = Dialogo(sprite.dialogo, *locutores)
            Ed.DIALOG = DialogCircularMenu(sprite, self)

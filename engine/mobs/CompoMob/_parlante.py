from engine.UI.circularmenus import DialogCircularMenu
from engine.globs import EngineData, ModData
from engine.IO.dialogo import Dialogo
from engine.misc import Resources, ReversibleDict
from ._movil import Movil


class Parlante(Movil):
    interlocutor = None  # para que el mob sepa con quién está hablando, si lo está
    conversaciones = []  # registro de los temas conversados
    hablante = True
    hablando = False
    is_the_speaker = False  # se refiere al mob que INICIA el diálogo

    def __init__(self, data, x, y, **kwargs):
        super().__init__(data, x, y, **kwargs)
        if 'states' in data:
            if 'dialog' in data['states'][0]:
                nombre = data['states'][0]['dialog']
                data['states'][0]['dialog'] = Resources.abrir_json(ModData.dialogos + nombre)

    def hablar(self, sprite):
        if sprite.hablante:
            self.interlocutor = sprite
            sprite.interlocutor = self
            self.is_the_speaker = True
            EngineData.DIALOG = Dialogo(sprite.dialogo, self, sprite)

    def elegir_tema(self, sprite):
        if sprite.hablante:
            self.interlocutor = sprite
            sprite.interlocutor = self

            locutores = [self, sprite]
            for loc in locutores:
                loc.hablando = True
                loc.detener_movimiento()

            # if  NPC.init_dialog():
                # Ed.DIALOG = Dialogo(sprite.dialogo, *locutores)
                # self.is_the_speaker = False
            # else:
            self.is_the_speaker = True
            EngineData.DIALOG = DialogCircularMenu(sprite, self)

    def stop_talking(self):
        self.is_the_speaker = False

    def update(self):
        if not self.hablando:
            super().update()
        else:
            opuesta = ReversibleDict(arriba='abajo', derecha='izquierda')
            direccion = opuesta[self.interlocutor.direccion]
            if self.direccion != direccion and not self.is_the_speaker:
                self.cambiar_direccion(direccion)


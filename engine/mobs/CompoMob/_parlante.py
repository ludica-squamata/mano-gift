from engine.UI.circularmenus import DialogCircularMenu
from engine.IO.dialogo import Monologo
from engine.misc import ReversibleDict
from ._movil import Movil


class Parlante(Movil):
    interlocutor = None  # para que el mob sepa con quién está hablando, si lo está
    hablante = True
    hablando = False

    def hablar(self, sprite):
        locutores = [self, sprite]
        self.interlocutor = sprite
        sprite.interlocutor = self
        for loc in locutores:
            loc.hablando = True
            loc.detener_movimiento()
        opuesta = ReversibleDict(arriba='abajo', derecha='izquierda')
        sprite.cambiar_direccion(opuesta[self.direccion])

    def dialogar(self, sprite):
        """
        :type sprite: engine.mobs.Mob
        """
        if sprite.hablante:
            self.hablar(sprite)
            file = DialogCircularMenu.is_possible(self, sprite)
            if file is not None:
                DialogCircularMenu(file, self, sprite)

            else:
                Monologo(sprite, self)

from engine.globs.event_aware import EventAware
from engine.globs import EngineData
from .CompoMob import Parlante
from engine.UI.propdescription import PropDescription
from .mob import Mob


class PC(EventAware, Parlante, Mob):

    def __init__(self, data, x, y):
        super().__init__(data, x, y, focus=True)
        self.functions['tap'].update({'accion': self.accion})

    # noinspection PyMethodOverriding
    def mover(self, direccion):
        if direccion != self.direccion:
            self.cambiar_direccion(direccion)
        if not self.detectar_colisiones():
            super().mover()

    def accion(self):
        super().accion()
        x, y = self.direcciones[self.direccion]
        sprite = self.quadrant_interaction(x, y)
        if sprite is not None:
            if sprite.tipo == 'Mob':
                if self.estado == 'cmb':
                    x, y = x * self.fuerza, y * self.fuerza
                    self.atacar(sprite, x, y)
                else:
                    self.elegir_tema(sprite)
                    EngineData.MODO = 'Dialogo'
                    self.deregister()

            elif sprite.tipo == 'Prop':
                if sprite.action is not None:
                    sprite.action(self)

                elif self.estado != 'cmb':
                    EngineData.DIALOG = PropDescription(sprite)
                    EngineData.MODO = 'Dialogo'
                    self.deregister()

    def cambiar_estado(self):
        super().cambiar_estado()
        self.register()

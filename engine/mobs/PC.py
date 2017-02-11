from engine.globs.eventDispatcher import EventDispatcher
from engine.globs.event_aware import EventAware
from engine.globs import EngineData
from .Inventory import Inventory
from .CompoMob import Parlante
from engine.UI.propdescription import PropDescription
from .mob import Mob


class PC(EventAware, Parlante, Mob):

    def __init__(self, data, x, y):
        self.inventario = Inventory(10, 10 + self.fuerza)
        self.functions = {
            'tap': {
                'accion': self.accion,
                'contextual': lambda: None,
            },
            'hold': {
                'accion': lambda: None,
                'contextual': lambda: None,
            },
            'release': {
                'accion': lambda: None,
                'contextual': lambda: None,
            }
        }
        super().__init__(data, x, y, focus=True)

    def use_function(self, mode, key):
        if key in self.functions[mode]:
            self.functions[mode][key]()

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

    def atacar(self, sprite, x, y):
        sprite.reubicar(x, y)
        sprite.recibir_danio(self.fuerza)

    def cambiar_estado(self):
        if self.estado == 'idle':
            self.establecer_estado('cmb')

        elif self.estado == 'cmb':
            self.establecer_estado('idle')

        self.animar_caminar()
        self.register()

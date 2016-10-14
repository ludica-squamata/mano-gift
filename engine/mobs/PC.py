from engine.globs.eventDispatcher import EventDispatcher
from engine.globs.event_dialogue import EventAware
from engine.globs import EngineData
from .Inventory import Inventory
from .CompoMob import Parlante
from engine.UI.propdescription import PropDescription
from .mob import Mob


class PC(EventAware, Parlante, Mob):

    def __init__(self, data, x, y):
        super().__init__(data, x, y, focus=True)
        self.inventario = Inventory(10, 10 + self.fuerza)
        self.functions = {
            'tap': {
                'accion': self.accion,
                'contextual': lambda: None,
                'arriba': lambda: self.cambiar_direccion('arriba', True),
                'abajo': lambda: self.cambiar_direccion('abajo', True),
                'izquierda': lambda: self.cambiar_direccion('izquierda', True),
                'derecha': lambda: self.cambiar_direccion('derecha', True),
            },
            'hold': {
                'accion': lambda: None,
                'contextual': lambda: None,
                'arriba': lambda: self.mover('arriba'),
                'abajo': lambda: self.mover('abajo'),
                'izquierda': lambda: self.mover('izquierda'),
                'derecha': lambda: self.mover('derecha'),
            },
            'release': {
                'accion': lambda: None,
                'contextual': lambda: None,
                'arriba': self.detener_movimiento,
                'abajo': self.detener_movimiento,
                'izquierda': self.detener_movimiento,
                'derecha': self.detener_movimiento,
            }
        }

    def use_function(self, mode, key):
        if key in self.functions[mode]:
            # noinspection PyCallingNonCallable
            self.functions[mode][key]()

    # noinspection PyMethodOverriding
    def mover(self, direccion):
        dx, dy = 0, 0
        if direccion == 'derecha':
            dx = +1
        elif direccion == 'izquierda':
            dx = -1
        elif direccion == 'arriba':
            dy = +1
        elif direccion == 'abajo':
            dy = -1

        if direccion != self.direccion:
            self.cambiar_direccion(direccion)
        dx, dy = dx * self.velocidad, dy * self.velocidad
        if not self.detectar_colisiones(dx, dy):
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
                    self.iniciar_dialogo(sprite, x, y)
                    EngineData.MODO = 'Dialogo'
                    self.deregister()

            elif sprite.tipo == 'Prop':
                if sprite.accion is not None:
                    if sprite.accion == 'agarrar':
                        item = sprite()
                        self.inventario.agregar(item)
                        EventDispatcher.trigger('DelItem', self.tipo, {'obj': sprite})

                    elif sprite.accion == 'operar' and sprite.enabled:
                        sprite.operar()

                elif self.estado != 'cmb':
                    EngineData.DIALOG = PropDescription(sprite)
                    EngineData.MODO = 'Dialogo'
                    self.deregister()

    def atacar(self, sprite, x, y):
        sprite.reubicar(x, y)
        sprite.recibir_danio(self.fuerza)

    def usar_item(self, item):
        if item.tipo == 'consumible':
            if item.usar(self):
                return self.inventario.remover(item)

    def cambiar_estado(self):
        if self.estado == 'idle':
            self.establecer_estado('cmb')

        elif self.estado == 'cmb':
            self.establecer_estado('idle')

        self.cambiar_direccion(self.direccion)
        self.animar_caminar()
        self.register()

    def iniciar_dialogo(self, sprite, x, y):
        inter_dir = ''
        self_dir = ''
        if x:
            if x > 0:
                inter_dir = 'izquierda'
                self_dir = 'derecha'
            else:
                inter_dir = 'derecha'
                self_dir = 'izquierda'
        elif y:
            if y < 0:
                inter_dir = 'abajo'
                self_dir = 'arriba'
            else:
                inter_dir = 'arriba'
                self_dir = 'abajo'

        if sprite is not None:
            # este check va a cambiar.
            sprite.iniciar_dialogo(inter_dir)
            self.cambiar_direccion(self_dir)
            if self.iniciativa < sprite.iniciativa:
                # la iniciativa la gana el NPC si se acerca a hablarle al heroe
                super().hablar(sprite)
            else:
                # si es el player el que toca Hablar, entonces se abre el menú
                self.elegir_tema(sprite)
from engine.globs.eventDispatcher import EventDispatcher
from .Inventory import Inventory, InventoryError
from .CompoMob import Parlante
from .mob import Mob


class PC(Parlante, Mob):

    def __init__(self, data, x, y):
        super().__init__(data, x, y, focus=True)
        self.inventario = Inventory(10, 10 + self.fuerza)

    # noinspection PyMethodOverriding
    def mover(self, dx, dy):
        # print(self.idx_quadrant)
        self.animar_caminar()
        direccion = ''
        if dx > 0:
            direccion = 'derecha'
        elif dx < -0:
            direccion = 'izquierda'
        elif dy < 0:
            direccion = 'arriba'
        elif dy > 0:
            direccion = 'abajo'

        self.cambiar_direccion(direccion)
        dx, dy = dx * self.velocidad, dy * self.velocidad
        if not self.detectar_colisiones(dx, dy):
            self.reubicar(dx, dy)

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
                    return self.iniciar_dialogo(sprite, x, y)
            elif sprite.tipo == 'Prop':
                if hasattr(sprite, 'accion'):
                    if sprite.accion == 'agarrar':
                        item = sprite()
                        self.inventario.agregar(item)
                        EventDispatcher.trigger('DelItem', self.tipo, {'obj': sprite})

                    elif sprite.accion == 'operar' and sprite.enabled:
                        sprite.operar()

                else:
                    print(sprite.nombre, sprite.descripcion)

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

        self.image = self.images['S' + self.direccion]
        self.mask = self.mascaras['S' + self.direccion]

        self.cambiar_direccion(self.direccion)
        self.animar_caminar()

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

            return True

        return False

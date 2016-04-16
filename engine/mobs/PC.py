from engine.globs.eventDispatcher import EventDispatcher
from .Inventory import Inventory, InventoryError
from .CompoMob import Parlante
from .mob import Mob


class PC(Parlante,Mob):
    
    def __init__(self, data, x, y, ):
        super().__init__(data, x, y, focus=True)
        self.inventario = Inventory(10, 10 + self.fuerza)

    # noinspection PyMethodOverriding
    def mover(self, dx, dy):
        self.moviendose = True
        self.animar_caminar()
        if dx > 0:
            self.cambiar_direccion('derecha')
        elif dx < -0:
            self.cambiar_direccion('izquierda')

        if dy < 0:
            self.cambiar_direccion('arriba')
        elif dy > 0:
            self.cambiar_direccion('abajo')

        dx, dy = dx * self.velocidad, dy * self.velocidad
        if not self.detectar_colisiones(dx, 0):
            self.reubicar(dx, 0)  # el heroe se mueve en el mapa, no en la camara
        if not self.detectar_colisiones(0, dy):
            self.reubicar(0, dy)
        
    def accion(self):
        x, y = self.direcciones[self.direccion]

        if self.estado == 'cmb':
            # la animacion de ataque se hace siempre,
            # sino pareciera que no pasa nada
            self.atacando = True
            sprite = self._interact_with_mobs(x, y)
            if issubclass(sprite.__class__, Mob):
                if self.estado == 'cmb':
                    x, y = x * self.fuerza, y * self.fuerza
                    self.atacar(sprite, x, y)
        else:
            sprite = self._interact_with_props(x, y)
            if hasattr(sprite, 'accion'):
                if sprite.accion == 'agarrar':
                    try:
                        item = sprite()
                        self.inventario.agregar(item)
                        EventDispatcher.trigger('DelItem', self.tipo, {'obj': sprite})
                    except InventoryError as Error:
                        print(Error)

                elif sprite.accion == 'operar':
                    sprite.operar()

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

    def update(self):
        self.moviendose = False
        if self.atacando:
            self.animar_ataque(5)
        
        super().update()

    def iniciar_dialogo(self):
        x, y = self.direcciones[self.direccion]
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

        sprite = self._interact_with_mobs(x, y)
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

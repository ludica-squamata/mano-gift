from engine.globs.event_aware import EventAware


class ControllableAI(EventAware):

    def __init__(self, entity):
        self.entity = entity
        super().__init__()

    def mover(self, direccion):
        if direccion != self.entity.direccion:
            self.entity.cambiar_direccion(direccion)
        if not self.entity.detectar_colisiones():
            self.entity.mover()

    def cambiar_estado(self):
        self.entity.cambiar_estado()
        self.entity.register()

    def update(self):
        self.entity.accion()
        sprite = self.entity.quadrant_interaction()
        if sprite is not None:
            if self.entity.estado == 'cmb':
                if hasattr(sprite, 'recibir_danio'):
                    self.entity.atacar()

            elif sprite.tipo == 'Prop':
                if sprite.action is not None:
                    sprite.action(self.entity)

                else:
                    sprite.show_description()
                    self.entity.deregister()

            elif sprite.tipo == 'Mob':
                self.entity.elegir_tema(sprite)
                self.entity.deregister()

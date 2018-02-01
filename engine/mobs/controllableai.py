from engine.globs.event_aware import EventAware


class ControllableAI(EventAware):
    accion = None

    def __init__(self, entity):
        self.entity = entity
        super().__init__()
        self.functions['tap'].update({
            'contextual': self.deregister,
            'menu': self.deregister,
            'accion': self.set_action,
            'arriba': lambda: self.entity.cambiar_direccion('arriba'),
            'abajo': lambda: self.entity.cambiar_direccion('abajo'),
            'izquierda': lambda: self.entity.cambiar_direccion('izquierda'),
            'derecha': lambda: self.entity.cambiar_direccion('derecha')
        })
        self.functions['hold'].update({
            'arriba': lambda: self.mover('arriba'),
            'abajo': lambda: self.mover('abajo'),
            'izquierda': lambda: self.mover('izquierda'),
            'derecha': lambda: self.mover('derecha')
        })
        self.functions['release'].update({
            'arriba': self.entity.detener_movimiento,
            'abajo': self.entity.detener_movimiento,
            'izquierda': self.entity.detener_movimiento,
            'derecha': self.entity.detener_movimiento
        })

    def mover(self, direccion):
        if direccion != self.entity.direccion:
            self.entity.cambiar_direccion(direccion)
        if not self.entity.detectar_colisiones():
            self.entity.mover()

    def set_action(self):
        self.accion = True

    def cambiar_estado(self):
        self.entity.cambiar_estado()
        self.register()

    def update(self):
        if self.accion:
            self.entity.accion()
            sprite = self.entity.sprite_interaction()
            if sprite is not None:
                if self.entity.estado == 'cmb':
                    if hasattr(sprite, 'recibir_danio'):
                        self.entity.atacar()

                elif sprite.tipo == 'Prop':
                    if sprite.action is not None:
                        sprite.action(self.entity)

                    else:
                        sprite.show_description()
                        self.deregister()

                elif sprite.tipo == 'Mob':
                    self.entity.elegir_tema(sprite)
                    self.deregister()
        self.accion = False

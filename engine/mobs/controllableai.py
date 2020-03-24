from engine.globs.event_dispatcher import EventDispatcher, AzoeEvent
from engine.globs.event_aware import EventAware
from engine.UI.circularmenus.quick import QuickCircularMenu


class ControllableAI(EventAware):
    accion = None

    def __init__(self, entity):
        self.entity = entity
        super().__init__()
        self.functions['tap'].update({
            'contextual': self.contextual_event_key,
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

        EventDispatcher.register(self.register, AzoeEvent('TogglePause', 'EngineData', {'value': False}))
        EventDispatcher.register(self.deregister, AzoeEvent('TogglePause', 'EngineData', {'value': True}))

    def mover(self, direccion):
        self.entity['Velocidad'] = 3  # El Mob controllable se mueve más rápido que otros mobs. Acá seteamos eso.
        # Este valor debería eliminarse (volver a ser 1) si el control sobre ese mob fuera a perderse.
        if direccion != self.entity.direccion:
            self.entity.cambiar_direccion(direccion)
        if not self.entity.detectar_colisiones():
            self.entity.mover()

    def set_action(self):
        self.accion = True

    def contextual_event_key(self):
        self.entity.detener_movimiento()
        QuickCircularMenu()
        self.deregister()

    def update(self):
        if self.accion:
            self.entity.accion()
            sprites = self.entity.perceived['touched'] + self.entity.perceived['felt']
            for sprite in sprites:
                if sprite is not None:
                    if self.entity.estado == 'cmb':
                        self.entity.atacar(sprite)

                    elif sprite.tipo == 'Mob':
                        self.entity.dialogar(sprite)
                        self.deregister()
                        break

                    elif sprite.tipo == 'Prop':
                        if sprite.accionable and sprite.action is not None:
                            # should Movible Props have an action?
                            sprite.action(self.entity)
                            break

                        else:
                            sprite.show_description()
                            self.deregister()

        self.accion = False

    def __repr__(self):
        return 'Controllable AI ({})'.format(self.entity.nombre)

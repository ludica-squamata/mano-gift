from engine.globs.event_dispatcher import EventDispatcher, AzoeEvent
from engine.globs.event_aware import EventAware
from engine.UI.circularmenus.quick import QuickCircularMenu
from math import sqrt


class ControllableAI(EventAware):
    accion = None

    def __init__(self, entity):
        self.entity = entity
        super().__init__()
        self.functions['tap'].update({
            'contextual': self.contextual_event_key,
            'menu': self.deregister,
            'accion': self.set_action,
            'arriba': lambda: self.entity.cambiar_direccion2('back'),
            'abajo': lambda: self.entity.cambiar_direccion2('front'),
            'izquierda': lambda: self.entity.cambiar_direccion2('left'),
            'derecha': lambda: self.entity.cambiar_direccion2('right')
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

        EventDispatcher.register_many(
            (self.register, AzoeEvent('TogglePause', 'EngineData', {'value': False})),
            (self.deregister, AzoeEvent('TogglePause', 'EngineData', {'value': True}))
        )

    def mover(self, direccion):
        self.entity['Velocidad'] = 3  # El Mob controllable se mueve más rápido que otros mobs. Acá seteamos eso.
        # Este valor debería eliminarse (volver a ser 1) si el control sobre ese mob fuera a perderse.
        if direccion != self.entity.direccion:
            self.entity.cambiar_direccion(direccion)
        if not self.entity.detectar_colisiones():
            self.entity.mover(*self.entity.direcciones[direccion])

        # if self.entity.mapRect.y % 800 == 0 or self.entity.mapRect.x % 800 == 0:
        #     # 800 porque es el tamaño de un chunk. Este valor podría ser configurable.
        #     self.entity.mapa_actual.parent.set_coordinates(direccion)

    def register(self):
        if not self.entity.pause_overridden:
            super().register()

    def set_action(self):
        self.entity.touch()
        self.accion = True

    def contextual_event_key(self):
        self.entity.detener_movimiento()
        QuickCircularMenu()
        self.deregister()

    def update(self):
        self.entity.update_sombra()
        if self.accion:
            self.entity.accion()
            preception = self.entity.perceived
            sprites = set(preception['touched'] + preception['felt'] + preception['close'])
            # a set because it filters repeated units.
            ex, ey = self.entity.rect.center
            close = [[q, sqrt((q.rect.x - ex) ** 2 + (q.rect.y - ey) ** 2)] for q in sprites]
            sprite = None
            if len(close):
                distances = [i[1] for i in close]
                mobs = [i[0] for i in close]
                dist_idx = distances.index(min(distances))
                sprite = mobs[dist_idx]
            if sprite is not None:
                if self.entity.estado == 'cmb':
                    self.entity.atacar(sprite)

                elif sprite.tipo == 'Mob':
                    self.entity.dialogar(sprite)
                    self.deregister()

                elif sprite.tipo == 'Prop' and sprite in preception['touched']:
                    if sprite.accionable and sprite.action is not None:
                        # should Movible Props have an action?
                        sprite.action(self.entity)

                    else:
                        sprite.show_description()
                        self.deregister()

        self.accion = False

    def __repr__(self):
        return 'Controllable AI ({})'.format(self.entity.nombre)

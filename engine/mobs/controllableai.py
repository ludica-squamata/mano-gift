from engine.UI.circularmenus.elements.descriptive_area import EmptyMobWarning
from engine.globs.event_dispatcher import EventDispatcher, AzoeEvent
from engine.globs.event_aware import EventAware
from engine.UI.circularmenus.quick import QuickCircularMenu
from engine.UI.circularmenus import LootingCircularMenu
from math import sqrt


class ControllableAI(EventAware):
    accion = None
    held = False
    released = False

    def __init__(self, entity):
        self.entity = entity
        self.entity['occupation'] = "hero"
        self.name = 'controllable'
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
            'accion': self.set_held_action,
            'arriba': lambda: self.mover('arriba'),
            'abajo': lambda: self.mover('abajo'),
            'izquierda': lambda: self.mover('izquierda'),
            'derecha': lambda: self.mover('derecha')
        })
        self.functions['release'].update({
            'accion': self.set_released_action,
            'arriba': self.entity.detener_movimiento,
            'abajo': self.entity.detener_movimiento,
            'izquierda': self.entity.detener_movimiento,
            'derecha': self.entity.detener_movimiento
        })

        EventDispatcher.register_many(
            (self.register, AzoeEvent('TogglePause', 'EngineData', {'value': False})),
            (self.deregister, AzoeEvent('TogglePause', 'EngineData', {'value': True})),
            (self.deregister_event, 'Deregister'), (self.register_event, 'Register')
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

    def deregister_event(self, event):
        if event.data['mob'] == self.entity:
            self.deregister()

    def register_event(self, event):
        if event.data['mob'] == self.entity:
            self.register()

    def register(self):
        if not self.entity.pause_overridden:
            super().register()

    def set_action(self):
        self.entity.touch()
        self.accion = True

    def set_held_action(self):
        if not self.held:
            del self.functions['hold']['arriba']
            del self.functions['hold']['abajo']
            del self.functions['hold']['izquierda']
            del self.functions['hold']['derecha']
            self.held = True

    def set_released_action(self):
        if not self.released:
            self.functions['release'].update({
            'arriba': lambda: self.mover('arriba'),
            'abajo': lambda: self.mover('abajo'),
            'izquierda': lambda: self.mover('izquierda'),
            'derecha': lambda: self.mover('derecha')
            })
            self.released = True


    def contextual_event_key(self):
        self.entity.detener_movimiento()
        QuickCircularMenu.load()
        QuickCircularMenu()
        self.deregister()

    def unload(self):
        event1 = AzoeEvent('TogglePause', 'EngineData', {'value': False})
        event2 = AzoeEvent('TogglePause', 'EngineData', {'value': True})

        EventDispatcher.deregister(self.register, event1)
        EventDispatcher.deregister(self.deregister, event2)

    def reset(self):
        """This is just a hook that does nothing.
        It's here to prevent a crash with Behaviour Trees"""
        pass

    def set_target(self, sprite):
        self.target = sprite

    def empty_mob_warning(self):
        self.deregister()
        descrip = EmptyMobWarning(self, 'No tiene nada')
        descrip.show()

    def update(self):
        self.entity.update_sombra()
        if self.accion:
            self.entity.accion()
            if self.target is not None:
                if self.entity.estado == 'cmb':
                    self.entity.atacar(self.target)

                elif self.target.tipo == 'Mob':
                    if self.entity.dialogar(self.target):
                        self.deregister()
                    elif self.target.dead and len(self.target.inventario):
                        self.deregister()
                        LootingCircularMenu(self, self.target)
                    elif self.target.dead:
                        self.empty_mob_warning()

        self.accion = False

    def __repr__(self):
        return f'Controllable AI ({self.entity.nombre})'

    def __eq__(self, other):
        # it should be other.name, but "other" in this case is the string "name"
        return self.name == other
from engine.globs import ModData, Mob_Group
from engine.globs.event_dispatcher import EventDispatcher, AzoeEvent
from .rendered import RenderedCircularMenu
from .elements import LetterElement, CommandElement, InventoryElement


class QuickCircularMenu(RenderedCircularMenu):
    radius = 18
    first = 0

    def __init__(self):
        self.entity = Mob_Group.get_controlled_mob()
        cascadas = ModData.QMC

        if cascadas is None:
            cascadas = {
                'inicial': [
                    CommandElement(self, {'name': 'Estado', 'icon': 'S', 'cmd': self.entity.cambiar_estado}),
                    CommandElement(self, {'name': 'Guardar', 'icon': 'G', 'cmd': self.save}),
                    LetterElement(self, 'Consumibles', 'C'),
                    LetterElement(self, 'Equipables', 'E')
                ],
                'Consumibles': [InventoryElement(self, item) for item in self.entity.inventario('consumible')],
                'Equipables': [InventoryElement(self, item) for item in self.entity.inventario('equipable')]
            }

        c = cascadas['inicial']
        for idx, opt in enumerate([c[self.first]] + c[self.first + 1:] + c[:self.first]):
            # Esto no está funcionando. Por alguna razón no recuerda cuál es el primer item.
            opt.idx = idx

        super().__init__(cascadas)
        self.functions['tap'].update({'contextual': self.back})

    def back(self):
        if self.cascadaActual == 'inicial':
            self.salir()
        else:
            super().backward()

    def stop_everything(self, on_spot=None):
        super().stop_everything(on_spot)
        self.set_first(self.last_on_spot.idx)

    @classmethod
    def set_first(cls, f: int):
        cls.first = f

    @staticmethod
    def cmd_rotar_vista(direccion):
        # solo una abreviatura

        EventDispatcher.trigger('Rotate', 'Menu Rápido', {'view': direccion})

    @staticmethod
    def save():
        EventDispatcher.trigger('Save', 'Menu Rápido', {})


EventDispatcher.register(QuickCircularMenu, AzoeEvent('Key', 'Modo.Aventura',
                                                      {'nom': 'contextual',
                                                       'type': 'tap'}))

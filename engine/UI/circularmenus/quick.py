from engine.globs import ModData, Mob_Group, GameState
from engine.globs.event_dispatcher import EventDispatcher
from .rendered import RenderedCircularMenu
from .elements import LetterElement, CommandElement, InventoryElement, DialogTopicElement


class QuickCircularMenu(RenderedCircularMenu):
    radius = 18
    first = 0

    def __init__(self):
        self.entity = Mob_Group.get_controlled_mob()
        cascadas = ModData.QMC
        self.nombre = 'Quick'

        if cascadas is None:
            cascadas = {
                'inicial': [
                    CommandElement(self, {'name': 'Estado', 'icon': 'S', 'cmd': self.entity.cambiar_estado}),
                    CommandElement(self, {'name': 'Guardar', 'icon': 'G', 'cmd': self.save}),
                    LetterElement(self, 'Consumibles', 'C'),
                    LetterElement(self, 'Equipables', 'E'),
                    LetterElement(self, 'Temas', 'T')
                ],
                'Consumibles': [InventoryElement(self, item) for item in self.entity.inventario('consumible')],
                'Equipables': [InventoryElement(self, item) for item in self.entity.inventario('equipable')],
            }

        temas = GameState.variables()
        lista = [item.lstrip('tema.').title() for item in temas if item.startswith('tema.') and temas[item]]
        cascadas.update({
            "Temas": [DialogTopicElement(self, i, t) for i, t in enumerate(lista)]
        })

        inicial = cascadas['inicial']
        for element in inicial:  # aunque me gustaria ponerlo en un onliner.
            element.index = inicial.index(element)  # esto soluciona el tema de recordar la posición del item.

        for idx, opt in enumerate([inicial[self.first]] + inicial[self.first + 1:] + inicial[:self.first]):
            opt.idx = idx

        # La diferencia entre idx e index es sutil. Index el el número que corresponde al ID del item, que es asignado
        # "al momento de su creación". idx por otra parte, indica la posición en pantalla que el item debe tomar.

        super().__init__(cascadas)
        self.functions['tap'].update({'contextual': self.back})

    def back(self):
        if self.cascadaActual == 'inicial':
            self.salir()
        else:
            super().backward()

    def stop_everything(self, on_spot=None):
        super().stop_everything(on_spot)
        self.set_first(self.last_on_spot.index)

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

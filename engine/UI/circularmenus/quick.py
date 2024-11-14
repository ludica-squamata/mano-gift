from engine.globs import ModData, Mob_Group, Game_State
from engine.globs.event_dispatcher import EventDispatcher
from .rendered import RenderedCircularMenu
from .elements import LetterElement, CommandElement, InventoryElement, DialogTopicElement
from .elements import ColocableInventoryElement as Colocable_IE


class QuickCircularMenu(RenderedCircularMenu):
    radius = 18
    first = 0

    def __init__(self):
        self.entity = Mob_Group.get_controlled_mob()
        e = self.entity  # local shortcut
        self.nombre = 'Quick'

        if ModData.QMC is None:
            cascadas = {
                'inicial': [
                    CommandElement(self, {'name': 'Estado', 'icon': 'S', 'cmd': e.cambiar_estado}),
                    CommandElement(self, {'name': 'Guardar', 'icon': 'G', 'cmd': self.save}),
                    LetterElement(self, 'Consumibles', 'C'),
                    LetterElement(self, 'Equipables', 'E'),
                    LetterElement(self, "Utilizables", "U"),
                    LetterElement(self, 'Temas', 'T'),
                    LetterElement(self, 'Colocar', 'P')
                ],
                'Consumibles': [InventoryElement(self, item) for item in e.inventario.get_by_type('consumible')],
                'Equipables': [InventoryElement(self, item) for item in e.inventario.get_by_type('equipable')],
                'Utilizables': [InventoryElement(self, item) for item in e.inventario.get_by_type('utilizable')],
                'Colocar': [Colocable_IE(self, item) for item in e.inventario.uniques() if item.is_colocable]
            }
        else:
            commands = [CommandElement(self, data) for data in ModData.QMC if 'cmd' in data]
            cascades = [LetterElement(self, *data) for data in ModData.QMC if 'csc' in data]
            cascadas = {
                'inicial': [i for i in commands] + [i for i in cascades]
            }

        temas = Game_State.find('tema.')
        lista = [item[5:].title() for item in temas if temas[item]]
        cascadas.update({
            "Temas": [DialogTopicElement(self, i, t) for i, t in enumerate(lista)]
        })

        for n in cascadas:
            cascada = cascadas[n]
            for element in cascada:  # aunque me gustaria ponerlo en un onliner.
                element.index = cascada.index(element)  # esto soluciona el tema de recordar la posición del item.

            if self.first <= len(cascada) - 1:
                for idx, opt in enumerate([cascada[self.first]] + cascada[self.first + 1:] + cascada[:self.first]):
                    opt.idx = idx
            else:
                for idx, opt in enumerate(cascada):
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
    def save():
        EventDispatcher.trigger('Save', 'Menu Rápido', {})

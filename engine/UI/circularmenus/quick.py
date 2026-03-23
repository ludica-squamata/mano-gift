from engine.globs import ModData, Mob_Group, Game_State
from engine.misc.resources import cargar_imagen
from engine.globs.event_dispatcher import EventDispatcher
from .rendered import RenderedCircularMenu
from .elements import CommandElement, InventoryElement, DialogTopicElement, LetterElement
from .elements import ColocableInventoryElement


class QuickCircularMenu(RenderedCircularMenu):
    radius = 18
    first = 0

    def __init__(self):
        self.entity = Mob_Group.get_controlled_mob()
        e = self.entity  # local shortcut
        inv = e.inventario
        self.nombre = 'Quick'

        icons = {
            'G': cargar_imagen(ModData.graphs + 'journal.png'),
            'I': cargar_imagen(ModData.graphs + 'bag_brown.png'),
            'T': cargar_imagen(ModData.graphs + 'menuglob left mini.png'),
            'P': cargar_imagen(ModData.graphs + 'colocar.png')
        }

        if ModData.QMC is None:
            cascadas = {
                'inicial': [
                    StanceElement(self, e),
                    CommandElement(self, {'name': 'Guardar', 'icon': icons['G'], 'cmd': self.save}),
                    LetterElement(self, "Items", icons['I']),
                    LetterElement(self, 'Temas', icons['T']),
                    LetterElement(self, 'Colocar', icons['P'])
                ],
                "Items": [
                    LetterElement(self, 'Consumibles', 'C'),
                    LetterElement(self, 'Equipables', 'E'),
                    LetterElement(self, "Utilizables", "U")],
                'Consumibles': [InventoryElement(self, e, item) for item in inv.get_by_type('consumible')],
                'Equipables': [InventoryElement(self, e, item) for item in inv.get_by_type('equipable')],
                'Utilizables': [InventoryElement(self, e, item) for item in inv.get_by_type('utilizable')],
                'Colocar': [ColocableInventoryElement(self, e, item) for item in inv.uniques() if item.is_colocable]
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


class StanceElement(CommandElement):
    def __init__(self, parent, entity):
        self.entity = entity
        icono = 'S'
        if entity.estado == 'cmb':
            icono = cargar_imagen(ModData.graphs + 'sword_folded.png')
        elif entity.estado == 'idle':
            icono = cargar_imagen(ModData.graphs + 'sword_raised.png')

        item = {'name': 'Postura', 'icon': icono, 'cmd': entity.cambiar_estado}

        super().__init__(parent, item)

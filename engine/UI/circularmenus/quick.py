from engine.globs import ModData, Mob_Group, Game_State
from engine.misc.resources import cargar_imagen, split_spritesheet
from engine.globs.event_dispatcher import EventDispatcher
from .rendered import RenderedCircularMenu
from .elements import CommandElement, InventoryElement, DialogTopicElement, LetterElement
from .elements import ColocableInventoryElement


class QuickCircularMenu(RenderedCircularMenu):
    radius = 18
    first = 0
    icons = None

    def __init__(self):
        self.entity = Mob_Group.get_controlled_mob()
        e = self.entity  # local shortcut
        inv = e.inventario
        self.nombre = 'Quick'

        if ModData.QMC is None:
            cascadas = {
                'inicial': [
                    StanceElement(self, e, self.icon_imgs[5:7]),
                    CommandElement(self, {'name': 'Guardar', 'icon': self.icons['G'], 'cmd': self.save}),
                    LetterElement(self, "Items", self.icons['I']),
                    LetterElement(self, 'Temas', self.icons['T']),
                    LetterElement(self, 'Colocar', self.icons['P'])
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

    @classmethod
    def load(cls):
        if cls.icons is None:
            icon_imgs = split_spritesheet(ModData.graphs + "qmc_spritesheet.png")
            cls.icons = dict(zip("I,P,G,T".split(','), [icon_imgs[0]] + icon_imgs[2:5]))
            cls.icon_imgs = icon_imgs

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
    def __init__(self, parent, entity, icons):
        self.entity = entity
        self.imagenes = {'idle':icons[1], 'cmb':icons[0]}
        icono = self.imagenes[entity.estado]
        item = {'name': 'Postura', 'icon': icono, 'cmd': entity.cambiar_estado}

        super().__init__(parent, item)

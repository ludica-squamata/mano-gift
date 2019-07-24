from .rendered import RenderedCircularMenu
from .elements import DialogObjectElement
from engine.globs import Mob_Group


class ObjectsCircularMenu(RenderedCircularMenu):
    radius = 80
    change_radius = False

    def __init__(self, parent):
        self.parent = parent
        self.entity = Mob_Group.get_controlled_mob()

        cascadas = {
            'inicial': [DialogObjectElement(self, i, item) for i, item in enumerate(self.entity.inventario)]}

        super().__init__(cascadas)

from .rendered import RenderedCircularMenu
from .elements import DialogObjectElement, DialogThemeElement
from engine.globs import Mob_Group, GameState


class ObjectsCircularMenu(RenderedCircularMenu):
    radius = 80
    change_radius = False

    def __init__(self, parent):
        self.parent = parent
        self.entity = Mob_Group.get_controlled_mob()

        cascadas = {
            'inicial': [DialogObjectElement(self, i, item) for i, item in enumerate(self.entity.inventario)]}

        super().__init__(cascadas)
        self.functions['tap'].update({'contextual': self.salir})


class ThemesCircularMenu(RenderedCircularMenu):
    radius = 80
    change_radius = False

    def __init__(self, parent):
        self.parent = parent
        self.entity = Mob_Group.get_controlled_mob()
        temas = GameState.variables()
        lista = [item.lstrip('tema.').title() for item in temas if item.startswith('tema.') and temas[item]]

        cascadas = {
            'inicial': [DialogThemeElement(self, i, item) for i, item in enumerate(lista)]
        }

        super().__init__(cascadas)


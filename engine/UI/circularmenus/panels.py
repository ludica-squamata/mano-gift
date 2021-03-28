from .rendered import RenderedCircularMenu
from .elements import DialogObjectElement, DialogThemeElement
from engine.globs import Mob_Group, GameState


class ObjectsCircularMenu(RenderedCircularMenu):
    radius = 80
    change_radius = False

    def __init__(self, parent):
        self.parent = parent
        self.entity = Mob_Group.get_controlled_mob()
        self.nombre = self.parent.nombre + 'Objects'

        cascadas = {
            'inicial': [DialogObjectElement(self, i, item) for i, item in enumerate(self.entity.inventario)]}

        super().__init__(cascadas)
        self.functions['tap'].update({'contextual': self.salir})

    def turn(self, delta):
        if len(self.cuadros):
            super().turn(delta)


class ThemesCircularMenu(RenderedCircularMenu):
    radius = 80
    change_radius = False

    def __init__(self, parent):
        self.parent = parent
        self.entity = Mob_Group.get_controlled_mob()
        self.nombre = self.parent.nombre + 'Themes'

        temas = GameState.variables()
        lista = [item[5:].title() for item in temas if item.startswith('tema.') and temas[item]]

        cascadas = {
            'inicial': [DialogThemeElement(self, i, item) for i, item in enumerate(lista)]
        }

        super().__init__(cascadas)

    def turn(self, delta):
        if len(self.cuadros):
            super().turn(delta)

    def update_cascades(self):
        temas = GameState.variables()
        lista = [item[5:].title() for item in temas if item.startswith('tema.') and temas[item]]
        cascadas = {
            'inicial': [DialogThemeElement(self, i, item) for i, item in enumerate(lista)]
        }
        self.cascadas.clear()
        self.add_cascades(cascadas)

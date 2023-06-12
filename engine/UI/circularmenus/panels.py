from .rendered import RenderedCircularMenu
from .elements import DialogObjectElement, DialogThemeElement
from engine.globs import Mob_Group, GameState


class PanelCircularMenu(RenderedCircularMenu):
    radius = 60
    change_radius = False

    def __init__(self, parent, name, lista):
        self.parent = parent
        self.nombre = self.parent.nombre + name

        if name == 'Objects':
            element = DialogObjectElement
        else:
            element = DialogThemeElement

        cascadas = {
            'inicial': [element(self, i, item) for i, item in enumerate(lista)]}

        super().__init__(cascadas)
        self.functions['tap'].update({'contextual': self.salir})

    def turn(self, delta):
        if len(self.cuadros):
            super().turn(delta)


class ObjectsCircularMenu(PanelCircularMenu):
    def __init__(self, parent):
        self.entity = Mob_Group.get_controlled_mob()
        super().__init__(parent, 'Objects', self.entity.inventario)

    def turn(self, delta):
        if len(self.cuadros):
            super().turn(delta)


class ThemesCircularMenu(PanelCircularMenu):
    def __init__(self, parent):
        temas = GameState.find('tema.')
        lista = [item[5:].title() for item in temas]

        super().__init__(parent, 'Themes', lista)

    def update_cascades(self):
        temas = GameState.find('tema.')
        lista = [item[5:].title() for item in temas if temas[item]]
        cascadas = {
            'inicial': [DialogThemeElement(self, i, item) for i, item in enumerate(lista)]
        }
        self.cascadas.clear()
        self.add_cascades(cascadas)

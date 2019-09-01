from engine.globs import ANCHO, ALTO, CANVAS_BG, TEXT_FG, CAPA_OVERLAYS_DIALOGOS
from engine.globs.renderer import Renderer
from .widgets import BaseWidget
from pygame import Surface, font


class BasePanel(BaseWidget):
    active = False

    def __init__(self, parent, nombre):
        image = Surface((int(ANCHO), int(ALTO / 5)))
        image.fill(CANVAS_BG)
        self.f = font.SysFont('Verdana', 16)
        self.nombre = nombre
        self.parent = parent
        super().__init__(image)
        self.ubicar(0, ALTO - int(ALTO / 5))
        self.marco = self.crear_marco(*self.rect.size)

    def show(self):
        self.active = True
        Renderer.add_overlay(self, CAPA_OVERLAYS_DIALOGOS)

    def hide(self):
        self.active = False
        Renderer.del_overlay(self)

    def update(self, *args):
        self.image.fill(CANVAS_BG)
        self.image.blit(self.marco, (0, 0))
        self.image.blit(self.f.render(self.nombre, 1, TEXT_FG, CANVAS_BG), (4, 3))


class DialogObjectsPanel(BasePanel):
    menu = None

    def __init__(self, parent):
        super().__init__(parent, 'Objects')

    def set_menu(self):
        from engine.UI.circularmenus.panels import ObjectsCircularMenu
        self.menu = ObjectsCircularMenu(self)

    def show(self):
        super().show()
        if self.menu is None:
            self.set_menu()
        else:
            self.menu.switch_cascades()

    def hide(self):
        super().hide()
        if self.menu is not None:
            Renderer.clear(layer=self.menu.layer)
            self.menu.cuadros.empty()

    def update(self):
        super().update()
        if self.menu.actual is not None:
            render = self.f.render('<mostrar {}>'.format(self.menu.actual.item.nombre), 1, TEXT_FG, CANVAS_BG)
            self.image.blit(render, (3, 23))


class DialogThemesPanel(BasePanel):
    menu = None

    def __init__(self, parent):
        super().__init__(parent, 'Themes')

    def set_menu(self):
        from engine.UI.circularmenus.panels import ThemesCircularMenu
        self.menu = ThemesCircularMenu(self)

    def show(self):
        super().show()
        if self.menu is None:
            self.set_menu()
        else:
            self.menu.update_cascades()
            self.menu.switch_cascades()

    def hide(self):
        super().hide()
        if self.menu is not None:
            Renderer.clear(layer=self.menu.layer)
            self.menu.cuadros.empty()

    def update(self):
        super().update()
        if self.menu.actual is not None:
            render = self.f.render('<mencionar {}>'.format(self.menu.actual.item), 1, TEXT_FG, CANVAS_BG)
            self.image.blit(render, (3, 23))

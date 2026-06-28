from engine.globs.event_dispatcher import EventDispatcher
from engine.globs.azoe_group import AzoeBaseSprite
from engine.globs.colores import Colores
from pygame import Surface, font


class Title(AzoeBaseSprite):
    active = True
    parent = None
    nombre = ''

    def __init__(self, parent, nombre):
        image = self.crear(nombre)
        super().__init__(parent, nombre, image, image.get_rect())

        EventDispatcher.register(self.recolor, 'AlterColor')

    @staticmethod
    def crear(nombre):
        fuente = font.Font('engine/libs/Verdanab.ttf', 15)
        w, h = fuente.size(nombre)
        image = Surface((w + 6, h + 2))
        image.fill(Colores.CANVAS_BG, (1, 1, w + 4, h))
        image.blit(fuente.render(nombre, True, Colores.TEXT_FG, Colores.CANVAS_BG), (2, 1))
        return image

    def center(self, rect):
        y = self.parent.rect.bottom + 12
        self.rect.center = (rect.centerx, y)

    def update(self, *args):
        self.center(self.parent.rect)

    def recolor(self, event):
        if event.data['name'] in ['TEXT_FG', 'CANVAS_BG']:
            self.image = self.crear(self.nombre)

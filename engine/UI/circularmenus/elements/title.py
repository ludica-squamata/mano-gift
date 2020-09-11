from engine.globs.colores import TEXT_FG, CANVAS_BG
from engine.globs.azoe_group import AzoeBaseSprite
from pygame import Surface, font


class Title(AzoeBaseSprite):
    active = True
    parent = None
    nombre = ''

    def __init__(self, parent, nombre):
        fuente = font.Font('engine/libs/Verdanab.ttf', 15)
        w, h = fuente.size(nombre)
        image = Surface((w + 6, h + 2))
        image.fill(CANVAS_BG, (1, 1, w + 4, h))
        image.blit(fuente.render(nombre, True, TEXT_FG, CANVAS_BG), (2, 1))
        super().__init__(parent, nombre, image, image.get_rect())

    def center(self, rect):
        self.rect.center = (rect.centerx, 210)

    def update(self, *args):
        self.center(self.parent.rect)

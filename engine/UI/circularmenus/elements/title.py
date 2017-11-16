from engine.globs.colores import TEXT_FG, CANVAS_BG
from pygame.sprite import Sprite
from pygame import Surface, font


class Title(Sprite):
    active = True
    parent = None
    nombre = ''

    def __init__(self, parent, nombre):
        super().__init__()
        self.nombre = nombre
        self.parent = parent

        fuente = font.Font('engine/libs/Verdanab.ttf', 15)
        w, h = fuente.size(self.nombre)
        self.image = Surface((w + 6, h + 2))
        self.image.fill(CANVAS_BG, (1, 1, w + 4, h))
        self.image.blit(fuente.render(nombre, 1, TEXT_FG, CANVAS_BG), (2, 1))
        self.rect = self.image.get_rect()

    def center(self, rect):
        self.rect.center = (rect.centerx, 210)

    def update(self, *args):
        self.center(self.parent.rect)

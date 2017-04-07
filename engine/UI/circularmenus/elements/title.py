from pygame.sprite import Sprite
from pygame import Surface
from engine.UI.estilo import Estilo


class Title(Sprite, Estilo):
    active = True
    parent = None
    nombre = ''

    def __init__(self, parent, nombre):
        super().__init__()
        self.nombre = nombre
        self.parent = parent

        w, h = self.fuente_Ib.size(self.nombre)
        negro = self.font_none_color
        gris = self.bg_cnvs

        self.image = Surface((w + 6, h + 2))
        self.image.fill(gris, (1, 1, w + 4, h))
        self.image.blit(self.fuente_Ib.render(nombre, 1, negro, gris), (2, 1))
        self.rect = self.image.get_rect()

    def center(self, rect):
        self.rect.center = (rect.centerx, 210)

    def update(self, *args):
        self.center(self.parent.rect)

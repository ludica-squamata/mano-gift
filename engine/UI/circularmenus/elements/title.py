from pygame.sprite import Sprite
from pygame import Surface
from engine.UI.estilo import Estilo


class Title(Sprite, Estilo):
    active = True

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
        self.rect = self.image.get_rect(center=(self.parent.rect.centerx, self.parent.rect.bottom + 15))

    def center(self, rect):
        self.rect.center = (rect.centerx, rect.bottom + 15)

    def update(self, *args):
        self.center(self.parent.rect)

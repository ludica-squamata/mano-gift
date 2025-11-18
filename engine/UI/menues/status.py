from engine.globs import TEXT_FG, CANVAS_BG, Mob_Group
from engine.libs import render_textrect
from pygame.sprite import LayeredUpdates
from pygame import Rect, font
from ..hud import ProgressBar
from .menu import Menu


class MenuStatus(Menu):
    entity = None

    def __init__(self, parent):
        super().__init__(parent, 'status', 'Status')
        self.entity = Mob_Group.get_controlled_mob()
        rect = self.update_charname_display()
        self.properties = LayeredUpdates()

        fuente_1 = font.Font('engine/libs/Verdanab.ttf', 14)
        fuente_2 = font.Font('engine/libs/Verdana.ttf', 14)

        chars = list(self.entity.get_attr_names()) + ['', 'SaludMax', 'ManaMax']

        for i, char in enumerate(chars):
            if char != '':
                value = self.entity[char]
                render_char = fuente_1.render(char, True, TEXT_FG, CANVAS_BG)
                render_rect = render_char.get_rect(left=305, y=rect.y + i * 23)

                render_value = render_textrect(str(value), fuente_2, Rect(0, 0, 32, 32), TEXT_FG, CANVAS_BG, 2)
                value_rect = render_value.get_rect(left=render_rect.left + 100, y=rect.y + i * 23)

                self.image.blit(render_char, render_rect)
                self.image.blit(render_value, value_rect)

        stats = {'SaludMax': [200, 50, 50], 'ManaMax': [125, 0, 255], 'Experiencia': [0, 200, 100]}
        for i, stat in enumerate(stats):
            bar = ProgressBar(self.entity[stat], stat.removesuffix('Max'), stats[stat], CANVAS_BG, rect.right,
                              rect.y + i * 35 + 6, 200, 32, self.entity)
            self.properties.add(bar)

            if i == 0:
                bar.set_variable(divisiones=5)
            bar.actualizar()
            self.image.blit(bar.image, bar.rect)

    def update_charname_display(self):
        r = self.canvas.blit(self.entity.diag_face[0], (6, 100))
        fuente = font.Font('engine/libs/Verdana.ttf', 22)
        w, h = fuente.size(self.entity.nombre)
        rect = Rect(0, r.bottom + 2, w, h + 1)
        rect.centerx = r.centerx

        render = render_textrect(self.entity['nombre'], fuente, rect, TEXT_FG, CANVAS_BG)
        self.canvas.blit(render, rect)
        return r

    def cancelar(self):
        super().cancelar()
        for sprite in self.properties.sprites():
            sprite.force_hide()
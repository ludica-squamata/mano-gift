from engine.UI.widgets import BaseWidget
from engine.globs import ANCHO, ALTO
from engine.libs import render_tagged_text


class DescriptiveArea(BaseWidget):
    active = True
    parent = None

    def __init__(self, parent, item):
        w, h = ANCHO, int(ALTO / 5)
        megacanvas = self.create_raised_canvas(w, h)
        canvas = self.create_sunken_canvas(w - 8, h - 8)
        megacanvas.blit(canvas, (6, 6))
        self.parent = parent
        super().__init__(megacanvas)

        self.ubicar(0, ALTO - h)
        render = render_tagged_text(item.efecto_des, self.tags, w - 16, h - 14, self.bg_cnvs)
        self.image.blit(render, (10, 8))

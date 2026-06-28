from engine.globs import ANCHO, ALTO, Colores, CAPA_OVERLAYS_DIALOGOS
from engine.globs.event_dispatcher import EventDispatcher
from engine.globs.event_aware import EventAware
from engine.globs.renderer import Renderer
from engine.libs import render_tagged_text
from engine.UI.widgets import BaseWidget


class DescriptiveArea(BaseWidget):
    active = True
    parent = None

    def __init__(self, parent, description):
        w, h = ANCHO, int(ALTO / 5)
        megacanvas = self.create_raised_canvas(w, h)
        canvas = self.create_sunken_canvas(w - 8, h - 8)
        megacanvas.blit(canvas, (6, 6))
        super().__init__(parent, imagen=megacanvas)

        self.ubicar(0, ALTO - h)
        self.des = description
        render = render_tagged_text(description, w - 16, h - 14, Colores.CANVAS_BG)
        self.image.blit(render, (10, 8))

        EventDispatcher.register(self.recolor, 'AlterColor')

    def recolor(self, event):
        if event.data['name'] in ['CANVAS_BG']:
            render = render_tagged_text(self.des, ANCHO - 16, int(ALTO / 5) - 14, Colores.CANVAS_BG)
            self.image.blit(render, (10, 8))


class EmptyMobWarning(EventAware, DescriptiveArea):
    def __init__(self, parent, description):
        super().__init__(parent, description)

        self.functions['tap'].update({
            'accion': self.hide,
            'contextual': self.hide
        })

    def show(self):
        Renderer.add_overlay(self, CAPA_OVERLAYS_DIALOGOS)

    def hide(self):
        Renderer.del_overlay(self)
        self.parent.register()
        self.parent.target = None  # prevents ControllableAI's update() method from excuting immediateley.

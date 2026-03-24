from engine.globs import CAPA_OVERLAYS_DIALOGOS, ANCHO, ALTO, Colores
from engine.globs.event_dispatcher import EventDispatcher
from engine.libs.textrect import render_textrect
from engine.globs.event_aware import EventAware
from engine.globs.renderer import Renderer
from engine.UI.widgets import BaseWidget
from pygame import Surface, Rect, font


class PropDescription(EventAware, BaseWidget):
    item = None
    rendered_text = None
    active = True

    def __init__(self, item):
        if item.nombre is None or item.descripcion is None:
            self.salir()
            return

        image = Surface((int(ANCHO), int(ALTO / 5)))
        image.fill(Colores.CANVAS_BG)

        super().__init__(item, imagen=image)
        self.w, self.h = image.get_size()

        self.marco = self.crear_marco(*self.rect.size)
        self.draw_space_rect = Rect((3, 3), (self.w - 6, self.h - 7))
        self.erase_area = Rect(3, 3, self.w - 7, self.h - 7)
        self.text_rect = Rect(0, 3, 0, 0)
        self.loc_rect = Rect(0, 0, 0, 0)
        self.arrow_width = 16
        self.ubicar(0, ALTO - int(ALTO / 5))
        self.crear()

        self.functions['tap'].update({
            'accion': self.salir,
            'contextual': self.salir,
            'arriba': lambda: self.desplazar_texto('arriba'),
            'abajo': lambda: self.desplazar_texto('abajo')})

        self.functions['hold'].update({
            'arriba': lambda: self.desplazar_texto('arriba'),
            'abajo': lambda: self.desplazar_texto('abajo')})

        Renderer.add_overlay(self, CAPA_OVERLAYS_DIALOGOS)

    def crear(self):
        fuente = font.Font('engine/libs/Verdana.ttf', 14)

        self.loc_rect = self.parent.locutor.get_rect(y=3)
        self.loc_rect.x = 3

        self.draw_space_rect.x = self.loc_rect.w + 6
        self.erase_area.w -= self.loc_rect.w
        self.rendered_text = render_textrect(self.parent.descripcion, fuente,
                                             self.erase_area,
                                             Colores.TEXT_FG, Colores.CANVAS_BG)
        self.text_rect.size = self.rendered_text.get_size()
        self.text_rect.x = self.loc_rect.w + 6
        if self.text_rect.h < self.draw_space_rect.h:
            self.text_rect.y = 3  # reset scrolling

    def desplazar_texto(self, direccion):
        if direccion == 'arriba':
            self.scroll(+1)
        elif direccion == 'abajo':
            self.scroll(-1)

    def scroll(self, dy):
        if not self.draw_space_rect.contains(self.text_rect):
            if self.text_rect.top + dy < self.draw_space_rect.top:
                if self.text_rect.bottom + dy > self.draw_space_rect.bottom:
                    self.text_rect.y += dy * 3  # "3" podría ser un setting

    def salir(self):
        self.deregister()
        EventDispatcher.trigger('EndDialog', self, {'layer': CAPA_OVERLAYS_DIALOGOS})

    def update(self):
        self.image.fill(Colores.CANVAS_BG, self.erase_area)
        self.image.blit(self.parent.locutor, self.loc_rect)

        self.image.blit(self.rendered_text, self.text_rect)
        if not self.draw_space_rect.contains(self.text_rect):
            x, y = self.text_rect.right + 1, 0
            w, h = self.arrow_width, self.draw_space_rect.h + 3

            # pintar el area de la flecha, si es que hay más contenido que ver.
            self.image.fill(Colores.SCROLL_BG, (x, y, w, h))

        # dibujar el marco biselado.
        self.image.blit(self.marco, (0, 0))

    def recolor(self, event):
        if event.data['name'] in ['CANVAS_BG', 'TEXT_FG', 'SCROLL_BG']:
            self.crear()
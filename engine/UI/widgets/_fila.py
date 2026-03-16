from engine.libs import render_tagged_text, render_textrect
from engine.globs.event_dispatcher import EventDispatcher
from engine.globs import Colores, Mob_Group
from pygame import Surface, font, Rect
from .base_widget import BaseWidget


class Fila(BaseWidget):
    """Representación de los items del Inventario en la interface"""
    tipo = 'fila'
    item = None
    tag_init = None
    tag_end = None
    tagged = False
    justification = 0
    stack = True
    cantidad = 0

    texto = None

    def __init__(self, parent, item, w, x, y, h=0, tag=None, justification=0):

        self.item = item
        self.w = w
        self.h = h
        self.justification = justification
        if type(item) is str:
            self.set_text(item, w, justification)
            self.texto = item
        elif hasattr(self.item, 'texto'):
            self.set_text(item.texto, w, justification)
        else:
            self.entity = Mob_Group.get_controlled_mob()
            self.stack = self.item.stackable
            self.tag_init = '<' + tag + '>'
            self.tag_end = '</' + tag + '>'
            self.icon = self.item.image
            self.nombre = self.tag_init + self.item.nombre.capitalize() + self.tag_end
            self.cantidad = self.tag_init + 'x' + str(self.entity.inventario.cantidad(self.item)) + self.tag_end
            self.img_uns = self.construir_fila(Colores.CANVAS_BG)
            self.img_sel = self.construir_fila(Colores.TEXT_DIS)
            self.tagged = True

        super().__init__(parent, imagen=self.img_uns)
        self.rect = self.image.get_rect(topleft=(x, y))

        EventDispatcher.register(self.recolor, 'AlterColor')

    def __repr__(self):
        return self.nombre

    def construir_fila(self, bg):
        w = int(self.w // 2)
        h = self.h
        rect = self.item.image.get_rect()
        rect.center = 16, 16

        img_nmbr = render_tagged_text(self.nombre, w, bgcolor=bg, justification=0)
        img_cant = render_tagged_text(self.cantidad, w, bgcolor=bg, justification=1)

        image = Surface((self.w, h))
        image.fill(bg)
        image.blit(self.item.image, rect)
        image.blit(img_nmbr, (32, 6))
        image.blit(img_cant, (w + 1, 6))

        return image

    def set_text(self, texto, w, a):
        """Cambia y asigna el texto de la opción"""

        f = font.Font('engine/libs/Verdana.ttf', 16)
        _, h = f.size(texto)
        rect = Rect(0, 0, w, h+1)
        self.img_uns = render_textrect(texto, f, rect, Colores.TEXT_FG, Colores.CANVAS_BG, justification=a)
        self.img_sel = render_textrect(texto, f, rect, Colores.TEXT_FG, Colores.TEXT_DIS, justification=a)

        self.image = self.img_uns
        self.nombre = texto

    def reset_text(self, texto):
        self.set_text(texto, self.w, self.justification)

    def recolor(self, event):
        if event.data['name'] in ['CANVAS_BG', 'TEXT_DIS']:
            self.reset_text(self.texto)

    def update(self):
        if not hasattr(self.item, 'texto'):
            if self.tagged:
                self.cantidad = self.tag_init + 'x' + str(self.entity.inventario.cantidad(self.item)) + self.tag_end
            else:
                self.cantidad = 'x' + str(self.entity.inventario.cantidad(self.item))

            self.img_uns = self.construir_fila(Colores.CANVAS_BG)
            self.img_sel = self.construir_fila(Colores.TEXT_DIS)

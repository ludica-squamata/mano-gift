from engine.globs import CANVAS_BG, TEXT_DIS, Mob_Group
from engine.libs import render_tagged_text
from .base_widget import BaseWidget
from pygame import Surface


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

    def __init__(self, parent, item, w, x, y, h=0, tag=None, justification=0):
        self.entity = Mob_Group.get_controlled_mob()
        self.item = item
        self.w = w
        self.h = h
        self.justification = justification
        if type(item) is str:
            self.set_text(item, w, justification)
        elif hasattr(self.item, 'texto'):
            self.set_text(item.texto, w, justification)
        else:
            self.stack = self.item.stackable
            self.tag_init = '<' + tag + '>'
            self.tag_end = '</' + tag + '>'
            self.icon = self.item.image
            self.nombre = self.tag_init + self.item.nombre.capitalize() + self.tag_end
            self.cantidad = self.tag_init + 'x' + str(self.entity.inventario.cantidad(self.item)) + self.tag_end
            self.img_uns = self.construir_fila(CANVAS_BG)
            self.img_sel = self.construir_fila(TEXT_DIS)
            self.tagged = True

        super().__init__(parent, imagen=self.img_uns)
        self.rect = self.image.get_rect(topleft=(x, y))

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

        self.img_uns = render_tagged_text(texto, w, bgcolor=CANVAS_BG, justification=a)
        self.img_sel = render_tagged_text(texto, w, bgcolor=TEXT_DIS, justification=a)

        self.image = self.img_uns
        self.nombre = texto

    def reset_text(self, texto):
        self.set_text(texto, self.w, self.justification)

    def update(self):
        if not hasattr(self.item, 'texto'):
            if self.tagged:
                self.cantidad = self.tag_init + 'x' + str(self.entity.inventario.cantidad(self.item)) + self.tag_end
            else:
                self.cantidad = 'x' + str(self.entity.inventario.cantidad(self.item))

            self.img_uns = self.construir_fila(CANVAS_BG)
            self.img_sel = self.construir_fila(TEXT_DIS)

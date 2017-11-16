from .basewidget import BaseWidget
from pygame import Surface
from engine.libs import render_tagged_text
from engine.globs import EngineData, CANVAS_BG, TEXT_DIS


class Fila(BaseWidget):
    """Representación de los items del Inventario en la interface"""
    tipo = 'fila'
    item = None
    tag_init = None
    tag_end = None
    tagged = False
    ancho = 0
    justification = 0
    stack = True
    cantidad = 0

    def __init__(self, item, w, x, y, tag=None, justification=0):
        self.item = item
        self.ancho = w
        self.justification = justification
        if type(item) == str:
            self.set_text(item, w, justification)
        elif hasattr(self.item, 'texto'):
            self.set_text(item.texto, w, justification)
        else:
            if tag is not None:
                _tag = tag
            else:
                if item.tipo == 'equipable':
                    _tag = 'w'
                else:
                    _tag = 'n'

            self.stack = self.item.stackable
            self.tag_init = '<' + _tag + '>'
            self.tag_end = '</' + _tag + '>'
            self.nombre = self.tag_init + self.item.nombre.capitalize() + self.tag_end
            self.cantidad = self.tag_init + 'x' + str(EngineData.HERO.inventario.cantidad(self.item)) + self.tag_end
            self.img_uns = self.construir_fila(CANVAS_BG)
            self.img_sel = self.construir_fila(TEXT_DIS)
            self.tagged = True

        super().__init__(self.img_uns)
        self.rect = self.image.get_rect(topleft=(x, y))

    def __repr__(self):
        return self.nombre

    def construir_fila(self, bg):
        w = int(self.ancho // 2)

        img_nmbr = render_tagged_text(self.nombre, w, bgcolor=bg, justification=1)
        img_cant = render_tagged_text(self.cantidad, w, bgcolor=bg, justification=1)

        image = Surface((self.ancho, img_nmbr.get_height()))
        image.fill(CANVAS_BG)
        image.blit(img_nmbr, (3, 0))
        image.blit(img_cant, (w + 1, 0))

        return image

    def set_text(self, texto, w, a):
        """Cambia y asigna el texto de la opción"""

        self.img_uns = render_tagged_text(texto, w, bgcolor=CANVAS_BG, justification=a)
        self.img_sel = render_tagged_text(texto, w, bgcolor=TEXT_DIS, justification=a)

        self.image = self.img_uns
        self.nombre = texto
    
    def reset_text(self, texto):
        self.set_text(texto, self.ancho, self.justification)

    def update(self):
        if not hasattr(self.item, 'texto'):
            if self.tagged:
                self.cantidad = self.tag_init + 'x' + str(EngineData.HERO.inventario.cantidad(self.item)) + self.tag_end
            else:
                self.cantidad = 'x' + str(EngineData.HERO.inventario.cantidad(self.item))

            self.img_uns = self.construir_fila(CANVAS_BG)
            self.img_sel = self.construir_fila(TEXT_DIS)

from .basewidget import BaseWidget


class Ventana(BaseWidget):
    posicion = x, y = 0, 0
    tamanio = ancho, alto = 0, 0
    sel = 0
    opciones = 0

    def __init__(self, image):
        super().__init__(image)

    def posicionar_cursor(self, i):
        self.sel += i
        if self.sel < 0:
            self.sel = self.opciones - 1

        elif self.sel > self.opciones - 1:
            self.sel = 0

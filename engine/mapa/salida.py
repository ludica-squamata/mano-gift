from pygame import Rect, Mask


class Salida:
    tipo = 'Salida'
    nombre = ''
    x, y = 0, 0
    dest = ''  # string, mapa de destino.
    link = ''  # string, nombre de la entrada en dest con la cual conecta
    rect = None
    mask = None
    solido = False

    def __init__(self, nombre, data):
        self.nombre = self.tipo + '.' + nombre
        self.x, self.y, alto, ancho = data['rect']
        self.mapX = self.x
        self.mapY = self.y
        self.dest = data['dest']
        self.link = data['link']  # string, nombre de la entrada en dest con la cual conecta
        self.rect = Rect((0, 0), (alto, ancho))
        self.ubicar(self.x, self.y)
        self.mask = Mask(self.rect.size)
        self.mask.fill()

    def ubicar(self, x, y):
        self.rect.x = x
        self.rect.y = y

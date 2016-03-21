from pygame import Rect, Mask, Surface
from engine.globs import MobGroup
from engine.globs.eventDispatcher import EventDispatcher
from pygame.sprite import Sprite
from engine.globs.renderer import Renderer
import sys


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
        if 'pydevd' in sys.modules:
            sprite = SpriteSalida(self.rect)
            if sprite not in Renderer.camara.real:
                Renderer.camara.add_real(sprite)

    def ubicar(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def update(self):
        for mob in MobGroup:
            dx, dy = mob.direcciones[mob.direccion]
            dx *= mob.velocidad
            dy *= mob.velocidad
            if mob.colisiona(self, dx, dy):
                EventDispatcher.trigger('CambiarMapa', 'Salida', {"mob": mob, 'dest': self.dest, 'link': self.link})


class SpriteSalida(Sprite):
    """Intented only to debugging"""
    def __init__(self, rect):
        super().__init__()

        self.image = Surface(rect.size)
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(center=rect.center)

        self.z = 5000
        self.mapX = self.rect.x
        self.mapY = self.rect.y

    def ubicar(self, x, y, z=0):
        self.rect.x = x
        self.rect.y = y
        del z

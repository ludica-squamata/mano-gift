from pygame import sprite, mask, Surface, Rect
from engine.misc import cargar_imagen


class AzoeSprite(sprite.Sprite):
    tipo = ''
    nombre = ''  # Para diferenciar mobs del mismo tipo (enemy por ejemplo)
    solido = True  # si es solido, colisiona; si no, no.
    images = None
    mascaras = None
    data = None  # info importada de un json
    z = 0
    stage = None  # stage donde existe el mob

    mapRect = None  # mapX y mapY

    IMAGEN_D = 'abajo'
    IMAGEN_U = 'arriba'
    IMAGEN_L = 'izquierda'
    IMAGEN_R = 'derecha'
    IMAGEN_DL = 'abiz'
    IMAGEN_DR = 'abde'
    IMAGEN_UL = 'ariz'
    IMAGEN_UR = 'arde'
   
    direcciones = {'arriba': [0, -1], 'abajo': [0, 1], 'izquierda': [-1, 0], 'derecha': [1, 0],
                   'ninguna': [0, 0]}
    direccion = 'abajo'
    parent = None

    def __init__(self, imagen=None, rect=None, alpha=False, center=False, x=0, y=0, z=0, dz=0):
        assert imagen is not None or rect is not None, 'AzoeSprite debe tener bien una imagen, bien un rect'
        super().__init__()

        if isinstance(imagen, str):
            self.image = cargar_imagen(imagen)
        elif isinstance(imagen, Surface):
            self.image = imagen
        elif imagen is None:
            self.image = None
            self.visible = 0  # no funciona con dirty
        else:
            raise TypeError('Imagen debe ser una ruta, un Surface o None')

        if center:
            self.rect = self.image.get_rect(center=(320, 240))
        elif imagen is not None:
            self.rect = self.image.get_rect(topleft=(x, y))
        else:
            self.rect = rect

        if alpha:
            self.mask = alpha
        elif self.image is not None:
            self.mask = mask.from_surface(self.image)
        else:
            self.mask = mask.Mask(self.rect.size)

        self.mapRect = Rect(0, 0, *self.rect.size)
        self.mapRect.center = x, y

        if z:
            self.z = z
        elif center:
            self.z = self.mapRect.y + self.rect.h
        else:
            self.z = self.mapRect.bottom
        self.z += dz

    def set_parent_map(self, parent):
        self.stage = parent

    def reubicar(self, dx, dy):
        """mueve el sprite una cantidad de pixeles"""
        self.mapRect.move_ip(dx, dy)
        self.z += dy

    def ubicar(self, x, y):
        """Coloca al sprite en pantalla"""
        self.rect.x = x
        self.rect.y = y

    def colisiona(self, other, off_x=0, off_y=0):
        if self.nombre != other.nombre:
            x = self.mapRect.x - (other.mapRect.x - off_x)
            y = self.mapRect.y - (other.mapRect.y - off_y)
            if other.mask.overlap(self.mask, (x, y)):
                return True
        return False

    def imagen_n(self, n):
        if n in self.images:
            return self.images[n]
        else:
            return self.image

    def ubicar_en_entrada(self, x, y):
        self.mapRect.center = x, y
        self.z = self.mapRect.y + self.rect.h

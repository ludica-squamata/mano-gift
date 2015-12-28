from pygame import sprite, mask, Surface
from engine.misc import Resources


class AzoeSprite(sprite.Sprite):
    # mapX y mapY estan medidas en pixeles y son relativas al mapa
    mapX = 0
    mapY = 0
    stageX = 0
    stageY = 0
    tipo = ''
    nombre = ''  # Para diferenciar mobs del mismo tipo (enemy por ejemplo)
    solido = True  # si es solido, colisiona; si no, no.
    images = None
    data = None  # info importada de un json
    z = 0
    stage = None  # stage donde existe el mob

    IMAGEN_D = 'abajo'
    IMAGEN_U = 'arriba'
    IMAGEN_L = 'izquierda'
    IMAGEN_R = 'derecha'
    IMAGEN_DL = 'abiz'
    IMAGEN_DR = 'abde'
    IMAGEN_UL = 'ariz'
    IMAGEN_UR = 'arde'

    direcciones = {'arriba': [0, -1], 'abajo': [0, 1],
                   'izquierda': [-1, 0], 'derecha': [1, 0],
                   'ninguna': [0, 0]}
    direccion = 'abajo'

    def __init__(self, imagen = None, rect = None, alpha = False, center = False, x = 0, y = 0, z = 0):
        if imagen is None and rect is None:
            raise TypeError('_giftSprite debe tener bien una imagen, bien un rect')

        super().__init__()

        if isinstance(imagen, str):
            self.image = Resources.cargar_imagen(imagen)
        elif isinstance(imagen, Surface):
            self.image = imagen
        elif imagen is None:
            self.image = None
            self.visible = 0  # no funciona con dirty
        else:
            raise TypeError('Imagen debe ser una ruta, un Surface o None')

        if center:
            self.rect = self.image.get_rect(center = (320, 240))
        elif imagen is not None:
            self.rect = self.image.get_rect(topleft = (x, y))
        else:
            self.rect = rect

        if alpha:
            self.mask = alpha
        else:
            if self.image is not None:
                self.mask = mask.from_surface(self.image)
            else:
                self.mask = mask.Mask(self.rect.size)

        if z:
            self.z = z
        elif center:
            self.z = y + self.rect.h
        else:
            self.z = self.rect.bottom

        self.mapX = x
        self.mapY = y
        self.stageX = x
        self.stageY = y
        self.solido = True

    def reubicar(self, dx, dy):
        """mueve el sprite una cantidad de pixeles"""
        self.mapX += dx
        self.mapY += dy
        self.stageX += dx
        self.stageY += dy
        self.z += dy

    def ubicar(self, x, y, z = 0):
        """Coloca al sprite en pantalla"""
        self.rect.x = x
        self.rect.y = y
        self.stageX = x
        self.stageY = y
        if z:
            self.z += z

    def colisiona(self, other, off_x = 0, off_y = 0):
        if self.nombre != other.nombre:
            x = self.mapX - (other.mapX - off_x)
            y = self.mapY - (other.mapY - off_y)
            if other.mask.overlap(self.mask, (x, y)):
                return True
        return False

    def imagen_n(self, n):
        if n in self.images:
            return self.images[n]
        else:
            return self.image

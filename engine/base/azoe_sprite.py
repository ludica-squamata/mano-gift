from engine.globs import ModData, ANCHO, ALTO
from pygame import sprite, mask, Surface
from engine.misc import cargar_imagen


class AzoeSprite(sprite.Sprite):
    tipo = ''
    nombre = ''  # Para diferenciar mobs del mismo tipo (enemy por ejemplo)
    solido = True  # si es solido, colisiona; si no, no.
    images = None
    mascaras = None
    data = None  # info importada de un json
    z = 0
    x = 0  # ésta es la posición del item en el mundo
    y = 0  # no en la cámara. Para esto último se usa su rect.

    direcciones = {'arriba': [0, -1], 'abajo': [0, 1], 'izquierda': [-1, 0], 'derecha': [1, 0], 'ninguna': [0, 0]}
    direccion = 'abajo'
    parent = None  # might be a map, in case of real objects, but things like widgets have their macro structure set as
    # their parent
    chunk_adresses = None
    is_damageable = False

    def __init__(self, parent, imagen=None, rect=None, alpha=False, center=False, x=0, y=0, z=0, dz=0, id=None):
        assert imagen is not None or rect is not None, 'AzoeSprite debe tener bien una imagen, bien un rect'
        super().__init__()

        self.parent = parent

        if isinstance(imagen, str):
            self.image = cargar_imagen(ModData.graphs + imagen)
        elif isinstance(imagen, Surface):
            self.image = imagen
        elif imagen is None:
            self.image = None
            self.visible = 0
        else:
            raise TypeError('Imagen debe ser una ruta, un Surface o None')

        if center:
            self.rect = self.image.get_rect(center=(ANCHO // 2, ALTO // 2))
        elif imagen is not None:
            self.rect = self.image.get_rect(center=(x, y))
        else:
            self.rect = rect

        if alpha:
            self.mask = alpha
        elif self.image is not None:
            self.mask = mask.from_surface(self.image)
        else:
            self.mask = mask.Mask(self.rect.size)

        if hasattr(self.parent, 'adress'):
            self.x = x
            self.y = y
            self.rel_x = x
            self.rel_y = y

        if z:
            self.z = z
        else:
            self.z = self.y + self.rect.h  # bottom

        self.z += dz

        if id is None:
            self.id = ModData.generate_id()
        else:
            self.id = id

    def reubicar(self, dx, dy):
        self.x += dx
        self.y += dy

        if self.rel_x + dx < 0:
            self.rel_x = 800
        elif self.rel_x > 800:
            self.rel_x = 0
        else:
            self.rel_x += dx

        if self.rel_y + dy < 0:
            self.rel_y = 800
            self.z = 800 - 32  # aunque no estoy seguro de esto
        elif self.rel_y + dy > 800:
            self.rel_y = 0
            self.z = 32
        else:
            self.rel_y += dy
            self.z += dy

    def set_parent_map(self, chunk):
        self.parent = chunk
        self.chunk_adresses[chunk.parent.nombre] = chunk.adress.center

    def ubicar(self, x, y):
        """Coloca al sprite en pantalla"""
        self.rect.x = x
        self.rect.y = y

    def ubicar_en_mapa(self, x, y):
        self.x = x
        self.y = y
        self.z = self.y + self.rect.h  # bottom
        self.rel_x = x
        self.rel_y = y

    def colisiona(self, other, off_x=0, off_y=0):
        if self.nombre != other.nombre:
            x = self.rect.x + off_x - other.rect.x
            y = self.rect.y + off_y - other.rect.y
            if other.mask.overlap(self.mask, (x, y)):
                return True
        return False

    def imagen_n(self, n):
        if n in self.images:
            return self.images[n]
        else:
            return self.image

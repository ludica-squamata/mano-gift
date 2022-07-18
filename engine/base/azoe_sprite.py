from pygame import sprite, mask, Surface, Rect
from engine.globs import ModData, ANCHO, ALTO
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

    direcciones = {'arriba': [0, -1], 'abajo': [0, 1], 'izquierda': [-1, 0], 'derecha': [1, 0], 'ninguna': [0, 0]}
    direccion = 'abajo'
    parent = None
    mapa_actual = None

    is_damageable = False

    def __init__(self, imagen=None, rect=None, alpha=False, center=False, x=0, y=0, z=0, dz=0, id=None):
        assert imagen is not None or rect is not None, 'AzoeSprite debe tener bien una imagen, bien un rect'
        super().__init__()

        if isinstance(imagen, str):
            self.image = cargar_imagen(ModData.graphs + imagen)
        elif isinstance(imagen, Surface):
            self.image = imagen
        elif imagen is None:
            self.image = None
            self.visible = 0  # no funciona con dirty
        else:
            raise TypeError('Imagen debe ser una ruta, un Surface o None')

        if center:
            self.rect = self.image.get_rect(center=(ANCHO//2, ALTO//2))
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
        else:
            self.z = self.mapRect.bottom
        self.z += dz

        self.mapa_actual_rect = Rect(*self.mapRect)

        if id is None:
            self.id = ModData.generate_id()
        else:
            self.id = id

    def set_parent_map(self, parent):
        self.stage = parent
        self.mapa_actual = parent

    def reubicar(self, dx, dy):
        """mueve el sprite una cantidad de pixeles"""
        self.mapRect.move_ip(dx, dy)
        self.mapa_actual_rect.move_ip(dx, dy)
        self.z += dy

    def translocate(self, new_map, dx, dy):
        self.mapa_actual = new_map
        x, y = self.mapa_actual.rect.topleft
        self.mapa_actual_rect.center = -x + dx, -y + dy
        self.z = self.mapa_actual_rect.y + self.rect.h

    def ubicar(self, x, y):
        """Coloca al sprite en pantalla"""
        self.rect.x = x
        self.rect.y = y

    def ubicar_en_mapa(self, x, y):
        self.mapRect.centerx = x
        self.mapRect.centery = y
        self.z = self.mapRect.bottom

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

    def ubicar_en_entrada(self, x, y):
        self.mapRect.center = x, y
        self.z = self.mapRect.y + self.rect.h

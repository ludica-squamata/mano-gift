from pygame import sprite,mask,Surface
from collections import UserDict
from engine.misc import Resources as r


class _giftSprite(sprite.DirtySprite):
    #mapX y mapY estan medidas en pixeles y son relativas al mapa
    mapX = 0
    mapY = 0
    tipo = ''
    nombre = '' # Para diferenciar mobs del mismo tipo (enemy por ejemplo)
    solido = True # si es solido, colisiona; si no, no.
    images = None

    IMAGEN_D = 'abajo'
    IMAGEN_U = 'arriba'
    IMAGEN_L = 'izquierda'
    IMAGEN_R = 'derecha'
    IMAGEN_DL = 'abiz'
    IMAGEN_DR = 'abde'
    IMAGEN_UL = 'ariz'
    IMAGEN_UR = 'arde'


    def __init__(self, imagen=None, rect = None, alpha = False, stage = '', x = 0, y = 0):
        super().__init__()
        if imagen == None and rect == None:
            raise TypeError('_giftSprite debe tener bien una imagen, bien un rect')
        if isinstance(imagen, str):
            self.image = r.cargar_imagen(imagen)
        elif isinstance(imagen, Surface):
            self.image = imagen
        elif imagen == None: 
            self.image = None
            self.visible = 0 # no funciona con dirty
        else:
            raise TypeError('Imagen debe ser una ruta, un Surface o None')
            
        if imagen != None:
            self.rect = self.image.get_rect()
        else:
            self.rect = rect
        
        if alpha:
            self.mask = alpha
        else:
            if self.image != None:
                self.mask = mask.from_surface(self.image)
            else:
                self.mask = mask.Mask(self.rect.size)
        
        self.mapX = x
        self.mapY = y
        self.stage = stage
        self.solido = True
    
    def reubicar(self, dx, dy):
        '''mueve el sprite una cantidad de pixeles'''
        self.mapX += dx
        self.mapY += dy
        self.rect.move_ip(dx,dy)
        if self.image != None:
            self.dirty = 1

    def ubicar(self, x, y):
        '''Coloca al sprite en pantalla'''
        self.rect.x = x
        self.rect.y = y
        if self.image != None:
            self.dirty = 1

    def colisiona(self, sprite, off_x = 0, off_y = 0):
        if self.nombre != sprite.nombre:
            x = self.mapX-(sprite.mapX-off_x)
            y = self.mapY-(sprite.mapY-off_y)
            if sprite.mask.overlap(self.mask,(x,y)):
                return True
        return False

    def imagenN(self, n):
        if n in self.images:
            return self.images[n]
        else:
            return self.image
    def mascaraN(self,n):
        if n in self.mascaras:
            return self.mascaras[n]
        else:
            return self.mascaras

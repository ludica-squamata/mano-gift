from pygame import sprite,mask,Surface
from misc import Resources as r
from collections import UserDict

class _giftSprite(sprite.DirtySprite):
    #mapX y mapY estan medidas en pixeles y son relativas al mapa
    mapX = 0
    mapY = 0
    nombre = '' # Para diferenciar mobs del mismo tipo (enemy por ejemplo)
    solido = True # si es solido, colisiona; si no, no.
    def __init__(self, imagen=None, rect = None, alpha = False, stage = '', x = 0, y = 0):
        super().__init__()
        if imagen == None and rect == None:
            raise TypeError('_giftSprite debe tener bien una imagen, bien un rect')
        if isinstance(imagen, str):
            self.image = r.cargar_imagen(imagen)
        elif isinstance(imagen, Surface):
            self.image = imagen
        elif imagen = None: 
            self.image = None
            self.visible = 0 # no funciona con dirty
        else:
            raise TypeError('Imagen debe ser una ruta, un Surface o None')
            
        #queda mejor que el caso =None y el raise en else    
        
        if self.image != None:
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
        
        self.anim_counter = 0
        self.anim_limit = 20
        self.timer_animacion = 0
        self.frame_animacion = 1000/12

    def reubicar(self, dx, dy):
        '''mueve el sprite una cantidad de cuadros'''
        self.mapX += dx
        self.mapY += dy
        self.rect.move_ip(dx,dy)
        if self.image != None:
            self.dirty = 1

    def ubicar(self, x, y):
        '''mueve el sprite a una ubicacion especifica. tiene que ser valor positivo'''
        if x < 0 or y < 0:
            raise ValueError('Coordenadas fuera de rango')
        self.mapX = x
        self.mapY = y
        self.rect.move_ip(x,y)
        if self.image != None:
            self.dirty = 1

    
    def colisiona(self, sprite, off_x = 0, off_y = 0):
        if self.nombre != sprite.nombre:
            x = self.mapX-(sprite.mapX-off_x)
            y = self.mapY-(sprite.mapY-off_y)
            if sprite.mask.overlap(self.mask,(x,y)):
                return True
        return False
from pygame import Surface, Rect, font, Color, draw
from pygame.sprite import DirtySprite
from engine.globs import Constants as C

class HUD (DirtySprite):
    active = True
    
    def __init__(self,image,pos):
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)
        super().__init__()

class ProgressBar(HUD):
    '''Clase base para las barras, de vida, de maná, etc'''
    maximo = 0
    actual = 0
    divisiones = 1
    colorAct = 0,0,0
    colorFnd = 0,0,0
    
    def __init__(self,maximo,colorAct,colorFnd,posicion):
        
        self.colorAct = colorAct
        self.colorFnd = colorFnd
        self.maximo = maximo
        self.actual = maximo
        self.divisiones = 1
        
        self.w,self.h = 10*(C.CUADRO/2),C.CUADRO/2
        self.draw_area_rect = Rect(2,2,self.w-3,self.h-3)
        imagen = Surface((self.w,self.h))
        super().__init__(imagen,posicion)
    
    def _dibujar_actual(self):
        act_w = self.actual/self.maximo*self.w
        img = Surface((act_w-3,self.draw_area_rect.h))
        img.fill(self.colorAct)
        return img
    
    def _dibujar_fondo(self):
        img = Surface(self.draw_area_rect.size)
        img.fill(self.colorFnd)
        return img
    
    def _subdividir(self):
        dw = int(self.w/self.divisiones)
        w = 0
        for i in range(self.divisiones):
            w += dw
            draw.line(self.image,(0,0,0),(w,3),(w,self.h-3))
    
    def setVariable(self,**kwargs):
        '''Función pública para cambiar las variables en una linea'''
        for var in kwargs:
            if hasattr(self,var):
                exec('self.'+var+'='+str(kwargs[var]))
    
    def update(self):
        self.image.blit(self._dibujar_fondo(),self.draw_area_rect)
        self.image.blit(self._dibujar_actual(),self.draw_area_rect)
        self._subdividir()
        self.dirty = 1
        
from pygame import Surface, Rect, font, Color, draw
from pygame.sprite import DirtySprite
from engine.globs import Constants as C, EngineData as ED

class ProgressBar(DirtySprite):
    '''Clase base para las barras, de vida, de maná, etc'''
    maximo = 0
    actual = 0
    divisiones = 0
    colorAct = 0,0,0
    colorFnd = 0,0,0
    active = True
    def __init__(self,maximo,colorAct,colorFnd,posicion):
        super().__init__()
        
        self.colorAct = colorAct
        self.colorFnd = colorFnd
        self.maximo = maximo
        self.actual = maximo
        self.divisiones = 1
        
        self.w,self.h = 10*(C.CUADRO/2),C.CUADRO/2
        self.draw_area_rect = Rect(2,2,self.w-3,self.h-3)
        self.image = Surface((self.w,self.h))
        self.rect = self.image.get_rect(topleft=posicion)
    
    def _actual(self):
        x,y,w,h = self.draw_area_rect
        return Rect((x,y),(self.actual/self.maximo*self.w-3,h))
    
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
        self.image.fill(self.colorAct,self._actual())
        self._subdividir()
        self.dirty = 1

class HUD:
    #ya no es clase base. próximamente será una clase que agrupe
    #y registre en el renderer todos los elementos del hud.
    def __init__(self):
        self.BarraVida = ProgressBar(ED.HERO.salud,(255,0,0),(100,0,0),(1,1))
        self.BarraMana = ProgressBar(ED.HERO.mana,(125,0,255),(75,0,100),(1,20))
        self.BarraVida.setVariable(divisiones=4)
        
        ED.RENDERER.addOverlay(self.BarraVida,1)
        ED.RENDERER.addOverlay(self.BarraMana,1)
        
        
    
    def update(self):
        self.BarraVida.setVariable(actual=ED.HERO.salud)
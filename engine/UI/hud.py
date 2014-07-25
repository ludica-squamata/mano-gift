from pygame import Surface, Rect, font, Color, draw, PixelArray, SRCALPHA
from pygame.sprite import DirtySprite
from engine.globs import Constants as C, EngineData as ED
from .widgets import _espacio_equipable

class ProgressBar(DirtySprite):
    '''Clase base para las barras, de vida, de maná, etc'''
    maximo = 0
    actual = 0
    divisiones = 0
    colorAct = 0,0,0
    colorFnd = 0,0,0
    active = True
    def __init__(self,maximo,colorAct,colorFnd,x,y,w,h):
        super().__init__()
        
        self.colorAct = colorAct
        self.colorFnd = colorFnd
        self.maximo = maximo
        self.actual = maximo
        self.divisiones = 1
        
        self.x,self.y = x,y
        self.w,self.h = w,h
        self.draw_area_rect = Rect(1,1,self.w-1,self.h-2)
        self.image = Surface((self.w,self.h))
        self.rect = self.image.get_rect(topleft=(self.x,self.y))
    
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
                setattr(self,var,kwargs[var])
    
    def update(self):
        self.image.blit(self._dibujar_fondo(),self.draw_area_rect)
        self.image.fill(self.colorAct,self._actual())
        self._subdividir()
        self.dirty = 1

class espacioInventario(DirtySprite):
    isSelected = False
    item = None
    direcciones = {}
    active = True
    
    def __init__(self,x,y):
        '''Inicializa las variables de un espacio equipable.'''
        super().__init__()
        self.image = self.crear_base((125,125,125))
        self.rect = self.image.get_rect(topleft = (x,y))
        self.dirty = 1
    
    @staticmethod
    def crear_base(color):
        '''Crea las imagenes seleccionada y deseleccionada del espacio equipable.'''
        
        rect = Rect(1,1,28,28)
        base = Surface((30,30),flags=SRCALPHA)
        base.fill((0,0,0))
        base.fill((255,0,0),rect)
        pxArray = PixelArray(base)
        pxArray.replace((255,0,0),(175,175,175,100))        
        base = pxArray.surface
        return base
    
    def update(self):
        self.dirty = 1

class HUD:
    #ya no es clase base. próximamente será una clase que agrupe
    #y registre en el renderer todos los elementos del hud.
    cuadros = []
    def __init__(self):
        _rect = ED.RENDERER.camara.rect
        w,h = C.ANCHO//4,C.CUADRO//4
        dx,dy = _rect.centerx,_rect.bottom-33
        self.BarraVida = ProgressBar(ED.HERO.salud_max,(200,50,50),(100,0,0),dx-w-1,dy-11,w,h)
        self.BarraMana = ProgressBar(ED.HERO.mana,(125,0,255),(75,0,100),dx+2,dy-11,w,h)
        self.BarraVida.setVariable(divisiones=4)
        for i in range(10):
            cuadro = espacioInventario(dx-w-1+(i*32.6),dy)
            self.cuadros.append(cuadro)
            ED.RENDERER.addOverlay(cuadro,1)
        
        ED.RENDERER.addOverlay(self.BarraVida,1)
        ED.RENDERER.addOverlay(self.BarraMana,1)
    
    def update(self):
        self.BarraVida.setVariable(actual=ED.HERO.salud_act)
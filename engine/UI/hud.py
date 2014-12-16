from pygame import Surface, Rect, font, Color, draw, PixelArray, SRCALPHA
from pygame.sprite import DirtySprite,LayeredDirty
from engine.globs import Constants as C, EngineData as ED
from engine.UI.estilo import Estilo

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

class espacioInventario(DirtySprite,Estilo):
    item = None
    cant = 0
    item_img = None
    item_rect = None
    
    cant_img = None
    cant_rect = None

    isSelected = False
    active = True
    def __init__(self,idx,x,y):
        '''Inicializa las variables de un espacio equipable.'''
        super().__init__()
        self.id = idx
        self.img_uns = self.crear_base((125,125,125))
        self.img_sel = self.crear_seleccion(self.img_uns.copy())
        self.image = self.img_uns
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
    
    def clear(self):
        rect = Rect(2,2,26,26)
        self.image.fill((175,175,175,100),rect)
    
    @staticmethod
    def crear_seleccion(imagen):
        w,h = imagen.get_size()
        draw.rect(imagen,(255,255,255),(1,1,w-2,h-2),1)
        return imagen
    
    def serElegido(self):
        self.image = self.img_sel
        isSelected = True
        
    def serDeselegido(self):
        self.image = self.img_uns
        isSelected = False
    
    def setItem(self,item):
        _rect = Rect((0,0),self.rect.size)
        self.item = item
        self.item_img = item.image
        self.item_rect = item.image.get_rect(center=_rect.center)
       
    def setCant(self):
        w,h = self.rect.size
        self.cant = ED.HERO.inventario.cantidad(self.item)
        self.cant_img = self.fuente_MP.render(str(self.cant),True,self.font_none_color)
        dw,dh = self.cant_img.get_size()
        self.cant_rect = self.cant_img.get_rect(topleft=(w-dw-1,h-dh-1))
        
    def vaciar(self):
        self.item = None
        self.item_img = None
        self.item_rect = None
        
        self.cant = 0
        self.cant_img = None
        self.cant_rect = None
        
        self.dirty = 1
    
    def update(self):
        self.clear()
        if self.item != None and self.cant != 0:
            self.image.blit(self.item_img,self.item_rect)
            self.image.blit(self.cant_img,self.cant_rect)
        self.dirty = 1

class InventoryDisplay:
    cuadros = []
    onSelect = False
    current = 0
    def __init__(self,dx,dy,w):
        self.current = 0
        self.cuadros = LayeredDirty()
        for i in range(10):
            cuadro = espacioInventario(i,dx-w-1+(i*32.6),dy)
            self.cuadros.add(cuadro)
            
    def SelectCuadro(self,i=0):
        for cuadro in self.cuadros:
            cuadro.serDeselegido()
        if 0 <= self.current+i <= len(self.cuadros)-1:
            self.current += i
        self.cuadros.get_sprite(self.current).serElegido()
        self.onSelect = True
    
    def Item(self):
        cuadro = self.cuadros.get_sprite(self.current)
        item = cuadro.item 
        cuadro.cant = ED.HERO.usar_item(item)
        if cuadro.cant == 0:
            cuadro.vaciar()
            
    def colocar_item(self,item,slot):
        cuadro = self.cuadros.get_sprite(slot-1)
        cuadro.setItem(item)
        cuadro.setCant()
        
    def isOpen (self,slot):
        return self.cuadros.get_sprite(slot-1).item == None
    
    def Salir(self):
        for cuadro in self.cuadros:
            cuadro.serDeselegido()
        self.onSelect = False
        ED.MODO = 'Aventura'
    
    def update(self):
        self.cuadros.update()

class HUD:
    #ya no es clase base. próximamente será una clase que agrupe
    #y registre en el renderer todos los elementos del hud.
    def __init__(self):
        _rect = ED.RENDERER.camara.rect
        w,h = C.ANCHO//4,C.CUADRO//4
        dx,dy = _rect.centerx,_rect.bottom-33
        self.BarraVida = ProgressBar(ED.HERO.salud_max,(200,50,50),(100,0,0),dx-w-1,dy-11,w,h)
        self.BarraMana = ProgressBar(ED.HERO.mana,(125,0,255),(75,0,100),dx+2,dy-11,w,h)
        self.BarraVida.setVariable(divisiones=4)
        self.Inventory = InventoryDisplay(dx,dy,w)
        ED.RENDERER.addOverlay(self.BarraVida,1)
        ED.RENDERER.addOverlay(self.BarraMana,1)
        for cuadro in self.Inventory.cuadros:
             ED.RENDERER.addOverlay(cuadro,1)
        
        self._func_inv = {
            'izquierda':lambda:self.Inventory.SelectCuadro(-1),
            'derecha':lambda:self.Inventory.SelectCuadro(+1),
            'arriba':lambda:None,
            'abajo':lambda:None,
            'cancelar':self.Inventory.Salir,
            'inventario':lambda:None,
            'hablar':self.Inventory.Item
            }
    
    def usar_funcion(self,tecla):
        if self.Inventory.onSelect:
            if tecla in self._func_inv:
                self._func_inv[tecla]()
    
    def update(self):
        self.BarraVida.setVariable(actual=ED.HERO.salud_act)
        for item in ED.HERO.inventario:
            if item.slot != 'No':
                if self.Inventory.isOpen(item.slot):
                    self.Inventory.colocar_item(item,item.slot)
        self.Inventory.update()
from base import _giftSprite
from pygame import Surface, Rect, font, draw
from UI.Colores import Colores as  C

class _espacio_equipable (_giftSprite):
    isSelected = False
    item = None
    direcciones = {}
    
    def __init__(self,nombre,item,direcciones,x,y):
        '''Inicializa las variables de un espacio equipable.'''
        
        self.img_uns = self.crear_base()
        super().__init__(self.img_uns)
        self.img_sel = self.dibujar_seleccion(self.img_uns)
        
        self.draw_area = Surface((28,28))
        self.draw_area.fill((153,153,153))
        self.draw_area_rect = Rect((4,4),self.draw_area.get_size())
        
        self.direcciones = {}
        self.direcciones.update(direcciones)
        if item:
            self.ocupar(item)
        self.nombre = nombre
        self.rect = self.image.get_rect(topleft = (x,y))
        self.dirty = 1
    
    def crear_base(self):
        '''Crea las imagenes seleccionada y deseleccionada del espacio equipable.'''
        
        img = Surface((36,36))
        img.fill(C.bg_cnvs)
        
        rect = Rect(2,2,28,28)
        base = Surface((32,32))
        base.fill((153,153,153),rect)

        img.blit(base,(2,2))
        return img
    
    def dibujar_seleccion (self,img):
        sel = img.copy()
        w,h = sel.get_size()
        for i in range(round(38/3)):
            #linea punteada horizontal superior
            draw.line(sel,C.font_high_color,(i*7,0),((i*7)+5,0),2)
            
            #linea punteada horizontal inferior
            draw.line(sel,C.font_high_color,(i*7,h-2),((i*7)+5,h-2),2)
        
        for i in range(round(38/3)):
            #linea punteada vertical derecha
            draw.line(sel,C.font_high_color,(w-2,i*7),(w-2,(i*7)+5),2)
            
            #linea punteada vertical izquierda
            draw.line(sel,C.font_high_color,(0,i*7),(0,(i*7)+5),2)
        return sel
    
    def serElegido(self):
        '''Cambia la imagen del espacio por su versión seleccionada.'''
        
        self.image = self.img_sel
        self.isSelected = True
        self.dirty = 1
    
    def serDeselegido(self):
        '''Cambia la imagen del espacio por su versión deseleccionada.'''
        
        self.image = self.img_uns
        self.isSelected = False
        self.dirty = 1
    
    def ocupar(self,item):
        '''Inserta un item en ambas imagenes del espacio.'''
        
        self.item = item
        self.draw_area.blit(item.image,(1,5))
        self.img_uns.blit(self.draw_area,self.draw_area_rect)
        self.img_sel.blit(self.draw_area,self.draw_area_rect)
        self.dirty = 1
    
    def desocupar (self):
        '''Restaura las imágenes del espacio a su version sin item.'''

        self.item = None
        self.draw_area.fill((153,153,153))
        self.img_uns.blit(self.draw_area,self.draw_area_rect)
        self.img_sel.blit(self.draw_area,self.draw_area_rect)
        self.dirty = 1
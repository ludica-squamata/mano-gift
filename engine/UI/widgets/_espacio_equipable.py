from pygame import Surface, Rect, font, draw
from .basewidget import BaseWidget

class _espacio_equipable (BaseWidget):
    isSelected = False
    item = None
    direcciones = {}
    
    def __init__(self,nombre,item,direcciones,x,y):
        '''Inicializa las variables de un espacio equipable.'''
        
        self.img_uns = self.crear_base(self.bg_cnvs)
        super().__init__(self.img_uns)
        self.img_sel = self.dibujar_seleccion(self.img_uns,self.font_high_color)
        
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
    
    @staticmethod
    def crear_base(color):
        '''Crea las imagenes seleccionada y deseleccionada del espacio equipable.'''
        
        img = Surface((36,36))
        img.fill(color)
        
        rect = Rect(2,2,28,28)
        base = Surface((32,32))
        base.fill((153,153,153),rect)

        img.blit(base,(2,2))
        return img
    
    @staticmethod
    def dibujar_seleccion (img,color):
        sel = img.copy()
        w,h = sel.get_size()
        for i in range(round(38/3)):
            #linea punteada horizontal superior
            draw.line(sel,color,(i*7,0),((i*7)+5,0),2)
            
            #linea punteada horizontal inferior
            draw.line(sel,color,(i*7,h-2),((i*7)+5,h-2),2)
        
        for i in range(round(38/3)):
            #linea punteada vertical derecha
            draw.line(sel,color,(w-2,i*7),(w-2,(i*7)+5),2)
            
            #linea punteada vertical izquierda
            draw.line(sel,color,(0,i*7),(0,(i*7)+5),2)
        return sel
    
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
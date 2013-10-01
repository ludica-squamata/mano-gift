from .Colores import Colores
from base.base import _giftSprite
from pygame import font, Rect, Surface
from libs.textrect import render_textrect
from globs import Constants as C

class _item_inv (Colores,_giftSprite):
    nombre = ''
    item = None
    
    def __init__(self,item,ancho,pos):
        self.item = item
        self.nombre = self.item.nombre.capitalize()
        cant = self.item.cantidad
        imagen = self.construir_fila(ancho,self.nombre,cant)
        super().__init__(imagen)
        self.rect = self.image.get_rect(topleft=pos)
        self.dirty = 1
        
    def construir_fila(self,ancho,nombre,cantidad):
        fuente = font.SysFont('verdana', 16)
        _rect = Rect((-1,-1),((C.CUADRO*6),fuente.get_height()+1))
        img_nmbr = render_textrect(nombre,fuente,_rect,self.font_high_color,self.bg_cnvs,1)
        img_cant = render_textrect('x'+str(cantidad),fuente,_rect,self.font_high_color,self.bg_cnvs,1)
        
        image = Surface((ancho,_rect.h))
        image.fill(self.bg_cnvs)
        image.blit(img_nmbr,(0,0))
        image.blit(img_cant,((ancho-(C.CUADRO*6)),0))
        
        return image
    
    def __repr__(self):
        return self.nombre+' _item_inv DirtySprite'
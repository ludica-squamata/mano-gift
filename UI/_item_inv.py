from .Colores import Colores
from base.base import _giftSprite
from pygame import font, Rect, Surface
from libs.textrect import render_textrect

class _item_inv (Colores,_giftSprite):
    nombre = ''
    item = None
    
    def __init__(self,item,ancho,pos,fuente):
        self.item = item
        self.nombre = self.item.nombre.capitalize()
        cant = self.item.cantidad
        imagen = self.construir_fila(ancho,self.nombre,cant,fuente)
        super().__init__(imagen)
        self.rect = self.image.get_rect(topleft=pos)
        self.dirty = 1
        
    def construir_fila(self,ancho,nombre,cantidad,fuente):
        _rect = Rect((-1,-1),(int(ancho/2),fuente.get_height()+1))
        img_nmbr = render_textrect(nombre,fuente,_rect,self.font_high_color,self.bg_cnvs,1)
        img_cant = render_textrect('x'+str(cantidad),fuente,_rect,self.font_high_color,self.bg_cnvs,1)
        
        image = Surface((ancho,_rect.h))
        image.fill(self.bg_cnvs)
        image.blit(img_nmbr,(0,0))
        image.blit(img_cant,((ancho-(int(ancho/2))),0))
        
        return image
    
    def __repr__(self):
        return self.nombre+' _item_inv DirtySprite'
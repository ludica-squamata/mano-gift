from UI.estilo import Estilo
from base import _giftSprite
from pygame import font, Rect, Surface
from libs.textrect import render_textrect

class _item_inv (Estilo,_giftSprite):
    '''Representación de los items del Inventario en la internface'''
    nombre = ''
    item = None
    
    def __init__(self,item,ancho,pos,fuente,color):
        self.item = item
        self.nombre = self.item.nombre.capitalize()
        self.stack = self.item.esStackable
        cant = self.item.cantidad
        imagen = self.construir_fila(ancho,self.nombre,cant,fuente,color)
        super().__init__(imagen)
        self.rect = self.image.get_rect(topleft=pos)
        self.dirty = 1
        
    def construir_fila(self,ancho,nombre,cantidad,fuente,color):
        _rect = Rect((-1,-1),(int(ancho/2),fuente.get_height()+1))        
        img_nmbr = render_textrect(nombre,fuente,_rect,color,self.bg_cnvs,1)
        img_cant = render_textrect('x'+str(cantidad),fuente,_rect,color,self.bg_cnvs,1)
        
        image = Surface((ancho,_rect.h))
        image.fill(self.bg_cnvs)
        image.blit(img_nmbr,(0,0))
        image.blit(img_cant,((ancho-(int(ancho/2))),0))
        
        return image
    
    def serElegido(self):
        pass
    
    def serDeselegido(self):
        pass
    
    def __repr__(self):
        return self.nombre+' _item_inv DirtySprite'
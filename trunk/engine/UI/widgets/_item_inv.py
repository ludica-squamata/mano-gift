from engine.UI.estilo import Estilo
from .basewidget import BaseWidget
from engine.base import _giftSprite
from pygame import font, Rect, Surface
from engine.libs.textrect import render_textrect
from engine.globs import EngineData as ED

class _item_inv (BaseWidget):
    '''Representación de los items del Inventario en la internface'''
    nombre = ''
    item = None
    
    def __init__(self,item,cantidad,ancho,pos,fuente,color):
        self.item = item
        self.nombre = self.item.nombre.capitalize()
        self.stack = self.item.stackable
        self.img_uns = self.construir_fila(ancho,self.nombre,cantidad,fuente,color,self.bg_cnvs)
        self.img_sel = self.construir_fila(ancho,self.nombre,cantidad,fuente,color,self.font_low_color)
        super().__init__(self.img_uns)
        self.rect = self.image.get_rect(topleft=pos)
        self.dirty = 1
    
    @staticmethod
    def construir_fila(ancho,nombre,cantidad,fuente,fgcolor,bgcolor):
        _rect = Rect((-1,-1),(int(ancho/2),fuente.get_height()+1))        
        img_nmbr = render_textrect(nombre,fuente,_rect,fgcolor,bgcolor,1)
        img_cant = render_textrect('x'+str(cantidad),fuente,_rect,fgcolor,bgcolor,1)
        
        image = Surface((ancho,_rect.h))
        image.fill(bgcolor)
        image.blit(img_nmbr,(0,0))
        image.blit(img_cant,((ancho-(int(ancho/2))),0))
        
        return image
       
    def __repr__(self):
        return self.nombre+' _item_inv DirtySprite'
    
    def update(self):
        cant = ED.HERO.inventario.cantidad(item)
        self.img_uns = self.construir_fila(ancho,self.nombre,cant,fuente,color,self.bg_cnvs)
        self.img_sel = self.construir_fila(ancho,self.nombre,cant,fuente,color,self.font_low_color)
        self.dirty = 1
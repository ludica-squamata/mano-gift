from engine.UI.estilo import Estilo
from .basewidget import BaseWidget
from engine.base import _giftSprite
from pygame import font, Rect, Surface
from engine.libs.textrect import render_textrect
from engine.globs import EngineData as ED

class _base_fila (BaseWidget):
    '''Representación de los items del Inventario en la interface'''
    nombre = ''
    tipo = 'fila'
    item = None
    slot = '-'
    isSelected = False
    def __init__(self,item,ancho,fuente,color,pos):
        self.item = item
        self.ancho = ancho
        self.color = color
        self.fuente = fuente
        self.nombre = self.item.nombre.capitalize()
        self.stack = self.item.stackable
        self.cantidad = ED.HERO.inventario.cantidad(self.item)
        self.img_uns = self.construir_fila(self.bg_cnvs)
        self.img_sel = self.construir_fila(self.font_low_color)
        super().__init__(self.img_uns)
        self.rect = self.image.get_rect(topleft=pos)
    
    def __repr__(self):
        return self.nombre+' _item_inv Sprite'
    
    def update(self):
        self.cantidad = ED.HERO.inventario.cantidad(self.item)
        self.item.slot = self.slot
        self.img_uns = self.construir_fila(self.bg_cnvs)
        self.img_sel = self.construir_fila(self.font_low_color)
        if self.isSelected:
            self.image = self.img_sel
        else:
            self.image = self.img_uns
from .Colores import Colores
from libs.textrect import TextRectException
from base.base import _giftSprite
from pygame import font, Rect
from libs.textrect import render_textrect

class _opcion (Colores,_giftSprite):
    isSelected = False
    
    def __init__(self,texto,ancho,pos,size=16,aling=0):
        self.nombre = texto
        self.pos = pos
        self.size = size
        self.fuente = font.SysFont('verdana', size)
        self.rect = Rect((-1,-1),(ancho,self.fuente.get_height()+1))
        self.aling = aling
        
        self.setText(texto)
        super().__init__(self.img_none)
        self.serDeselegido()
        
    def serElegido(self):
        self.image = self.img_high
        self.isSelected = True
        self.rect = self.img_high.get_rect(topleft=self.pos)
        self.dirty = 1
        
    def serDeselegido(self):
        self.image = self.img_none
        self.isSelected = False
        self.rect = self.img_none.get_rect(topleft=self.pos)
        self.dirty = 1
    
    def setText(self,texto):
        f = self.fuente
        r = self.rect
        bg = self.bg_cnvs
        a = self.aling
        ok = False
        while ok == False:
            try:
                self.img_none = render_textrect(texto,f,r,self.font_none_color,bg,a)
                self.img_high = render_textrect(texto,f,r,self.font_high_color,bg,a)
                ok = True
            except TextRectException:
                self.size -= 1
                f = font.SysFont('verdana', self.size)
                
        if self.isSelected: self.serElegido()
        else: self.serDeselegido()

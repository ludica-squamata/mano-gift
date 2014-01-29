from .Colores import Colores
from libs.textrect import TextRectException
from base.base import _giftSprite
from pygame import font, Rect
from libs.textrect import render_textrect

class _opcion (Colores,_giftSprite):
    '''Opción única que es parte de una lista más grande.
    No tiene cantidad, pero puede ser seleccionada (resaltando)
    mediante serElegido.'''
    
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
        '''Cambia la imagen a la versión resaltada'''
        self.image = self.img_high
        self.isSelected = True
        self.rect = self.img_high.get_rect(topleft=self.pos)
        self.dirty = 1
        
    def serDeselegido(self):
        '''Cambia la imagen a la versión no elegida'''
        
        self.image = self.img_none
        self.isSelected = False
        self.rect = self.img_none.get_rect(topleft=self.pos)
        self.dirty = 1
    
    def setText(self,texto):
        '''Cambia y asigna el texto de la opción'''
        
        f = self.fuente
        r = self.rect
        bg = self.bg_cnvs
        a = self.aling
        
        while True:
            try:
                #Si el texto es muy grande para el rect...
                self.img_none = render_textrect(texto,f,r,self.font_none_color,bg,a)
                self.img_high = render_textrect(texto,f,r,self.font_high_color,bg,a)
                break
            except TextRectException:
                # Acá se achica.
                self.size -= 1
                f = font.SysFont('verdana', self.size)
                
        if self.isSelected: self.serElegido()
        else: self.serDeselegido()

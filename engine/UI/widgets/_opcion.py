from pygame import font, Rect
from .basewidget import BaseWidget
from engine.libs.textrect import TextRectException, render_textrect

class _opcion (BaseWidget):
    '''Opción única que es parte de una lista más grande.
    No tiene cantidad, pero puede ser seleccionada (resaltando)
    mediante serElegido.'''
    tipo = 'fila'
    isSelected = False
    
    def __init__(self,texto,ancho,pos,size=16,aling=0,extra_data=None):
        self.pos = pos
        self.size = size
        self.fuente = font.SysFont('verdana', size)
        self.rect = Rect((-1,-1),(ancho,self.fuente.get_height()+1))
        self.aling = aling
        self.extra_data = extra_data
        
        self.setText(texto)
        super().__init__(self.img_uns)
        self.rect = self.img_uns.get_rect(topleft=self.pos)
        
    def setText(self,texto):
        '''Cambia y asigna el texto de la opción'''
        
        f = self.fuente
        r = self.rect
        bg = self.bg_cnvs
        a = self.aling
        
        while True:
            try:
                #Si el texto es muy grande para el rect...
                self.img_uns = render_textrect(texto,f,r,self.font_none_color,bg,a)
                self.img_sel = render_textrect(texto,f,r,self.font_none_color,self.font_low_color,a)
                break
            except TextRectException:
                # Acá se achica.
                self.size -= 1
                f = font.SysFont('verdana', self.size)
                
        if self.isSelected: self.serElegido()
        else: self.serDeselegido()
        
        self.nombre = texto
    
    def __repr__(self):
        return self.nombre

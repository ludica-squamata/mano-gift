from engine.libs import render_textrect, render_tagged_text
from engine.misc.tagloader import load_tagarrayfile
from .dialogFrontEnd import DialogFrontEnd
from .widgets import _opcion
from pygame import Rect

class DialogInterface (DialogFrontEnd):  
    def __init__(self):
        super().__init__('RAISED')
        w,h = self.canvas.get_size()
        self.draw_space_rect = Rect((3,3),(w-100, h-7))
        self.erase_area = Rect(3,3,w-7,h-7)
    
    def setText(self,texto):
        w,h = self.draw_space_rect.size
        render = render_tagged_text(texto,w,h,self.tags,fgcolor=self.font_none_color,bgcolor=self.bg_cnvs)
        self.canvas.blit(render,self.text_pos)
        self.image = self.canvas
    
    def setSelMode(self,opciones):
        self.opciones = len(opciones)
        h = self.altura_del_texto
        x = self.draw_space_rect.x
        w = self.draw_space_rect.w
        for i in range(self.opciones):
            opcion = _opcion(opciones[i].texto,w,(x,i*h+i+3),extra_data=opciones[i].leads)
            self.filas.add(opcion)
        
        self.filas.draw(self.canvas)
    
    def setLocImg(self,locutor):
        """carga y dibuja la imagen de quien está hablando. También setea
        la posición del texto a izquierda o derecha según la "cara" del hablante"""
        img = locutor.diag_face
        if locutor.direccion == 'derecha' or locutor.direccion == 'abajo':
            dest = 3,3
            self.text_pos = 96,3
            self.draw_space_rect.topleft = 96,3
        else:
            dest = self.canvas.get_width()-93,3
            self.text_pos = 3,3
            self.draw_space_rect.topleft = 3,3
        
        self.canvas.blit(img,dest)
    
    def elegir_opcion (self,i):
        for fila in self.filas:
            fila.serDeselegido()
        self.posicionar_cursor(i)
        current = self.filas.get_sprite(self.sel)
        current.serElegido()
        return current.extra_data
    
    def borrar_todo(self):
        w,h = self.canvas.get_size()
        self.canvas.fill(self.bg_cnvs,self.erase_area)
        self.filas.empty()
        self.sel = 0
        
    def update (self):
        self.filas.draw(self.canvas)
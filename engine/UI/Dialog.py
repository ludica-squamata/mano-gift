from pygame import Rect
from engine.misc import Resources as r
from engine.libs.textrect import render_textrect
from .dialogFrontEnd import DialogFrontEnd
from .widgets import _opcion

class DialogInterface (DialogFrontEnd):  
    def __init__(self):
        super().__init__('RAISED')
        w,h = self.canvas.get_size()
        self.draw_space_rect = Rect((-1,-1),(w-96, h-7))
    
    def setText(self,texto):
        render = render_textrect(texto,self.fuente_M,self.draw_space_rect,self.font_none_color,self.bg_cnvs)
        self.canvas.blit(render,self.text_pos)
        self.image = self.canvas
    
    def setSelMode(self,opciones):
        self.borrar_todo()
        h = self.altura_del_texto
        self.opciones = len(opciones)
        for i in range(self.opciones):
            opcion = _opcion(opciones[i],self.draw_space_rect.w,(3,i*h+i+3))
            self.filas.add(opcion)
        
        #self.filas.draw(self.canvas)
        self.elegir_opcion(0)
    
    def setLocImg(self,locutor):
        '''carga y dibuja la imagen de quien está hablando. También setea
        la posición del texto a izquierda o derecha según la "cara" del hablante'''
        img = r.cargar_imagen('mobs/'+locutor.lower()+'_face.png')
        if locutor != 'PC':
            dest = 3,3
            self.text_pos = 96,3
        else:
            x = self.canvas.get_width()-92
            dest = x,3
            self.text_pos = 3,3
        
        self.canvas.blit(img,dest)
    
    def elegir_opcion (self,i):
        for fila in self.filas:
            fila.serDeselegido()
        self.sel = self.posicionar_cursor(i,self.sel,self.opciones)
        current = self.filas.get_sprite(self.sel)
        current.serElegido()
        return self.sel
    
    def borrar_todo(self):
        self.canvas.fill(self.bg_cnvs,((3,3),self.draw_space_rect.size))
        self.filas.empty()
        self.sel = 1
        
    def update (self):
        self.filas.draw(self.canvas)
        self.dirty = 1
from .Ventana import Ventana
from UI.widgets import _opcion
from pygame import font, sprite, Rect, draw
from globs import Constants as C, World as W
from misc import Resources as r
from libs.textrect import render_textrect

class Dialog (Ventana):
    posicion = 0,384
    filas = sprite.LayeredDirty()
    text_pos = 3,3
    active = True
    
    def __init__(self):
        self.canvas = self.crear_canvas(int(C.ANCHO), int(C.ALTO/5))
        self.altura_del_texto = self.fuente_M.get_height()+1
        self.draw_space = Rect((-1,-1),(self.canvas.get_width()-96, int(self.canvas.get_height())-7))
        super().__init__(self.canvas)
        self.ubicar(*self.posicion)
        self.dirty = 1
        
        #registrar en el Renderer
        W.RENDERER.overlays.add(self)#,layer=C.CAPA_OVERLAYS_DIALOGOS)
    
    def setText(self,texto):
        render = render_textrect(texto,self.fuente_M,self.draw_space,self.font_none_color,self.bg_cnvs)
        self.canvas.blit(render,self.text_pos)
        self.image = self.canvas
    
    def setSelMode(self,opciones):
        self.borrar_todo()
        h = self.altura_del_texto
        self.opciones = len(opciones)
        for i in range(self.opciones):
            opcion = _opcion(opciones[i],self.draw_space.w,(3,i*h+i+3))
            self.filas.add(opcion)
        
        self.filas.draw(self.canvas)
        #self.elegir_opcion(-1)
    
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
        self.sel = self.posicionar_cursor(i,self.sel,self.opciones)
        current = self.filas.get_sprite(self.sel-1)
        current.serElegido()
        return self.sel
    
    def borrar_todo(self):
        self.canvas.fill(self.bg_cnvs,((3,3),self.draw_space.size))
        self.filas.empty()
        self.sel = 1
        
    def update (self):
        self.dirty = 1
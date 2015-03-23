from engine.globs import EngineData as ED, Constants as C, ModData as MD, Tiempo as T
from pygame import Surface, font, sprite, event as EVENT, KEYDOWN, QUIT
from engine.misc import Resources as r, Util
from engine.UI.widgets import _opcion
from .menu import Menu
import os

class Menu_Debug (Menu):
    escenas = []
    def __init__ (self):
        super().__init__("Mano-Gift: Selector de Escenas")
        self.funciones = {
            'arriba':self.elegir_opcion,
            'abajo':self.elegir_opcion,
            'izquierda':lambda dummy:None,
            'derecha':lambda dummy:None,
            'hablar':self.cargar_escena}
        self.filas = sprite.LayeredDirty()
        self.crear_espacio_de_escenas(C.ANCHO-37,C.ALTO/2.4)
        self.elegir_opcion('arriba')
    
    @staticmethod
    def cargar_escenas():
        ok = []
        for scn in os.listdir(MD.scenes):
            scn = scn.split('.')
            ok.append(scn[0])
        
        return ok
    
    def crear_espacio_de_escenas (self,ancho,alto):
        escenas = self.crear_espacio_titulado(ancho,alto,'Elija una escena')
        rect = self.canvas.blit(escenas,(7,40))
        self.draw_space = escenas.subsurface(((0,0),(rect.w-8,rect.h-30)))
        self.draw_space.fill(self.bg_cnvs)
        self.draw_space_rect = escenas.get_rect(topleft=(11,65))
        
        self.altura_del_texto = h = self.fuente_M.get_height()+1
        self.escenas = self.cargar_escenas() # lista
        self.opciones = len(self.escenas)
        for i in range(len(self.escenas)):
            opcion = _opcion(self.escenas[i],self.draw_space_rect.w-10,(0,i*h+i+2))
            self.filas.add(opcion)

    def elegir_opcion(self,direccion):
        if direccion == 'arriba': i = -1
        elif direccion == 'abajo': i = +1
        self.DeselectAll(self.filas)
        self.sel = self.posicionar_cursor(i,self.sel,self.opciones)
        elegido = self.filas.get_sprite(self.sel)
        elegido.serElegido()
    
    def cargar_escena(self):
        ED.MODO = 'Aventura'
        ED.setear_escena(self.escenas[self.sel])
        ED.onPause = False
        ED.menu_previo = ''
    
    def update(self):
        self.filas.draw(self.draw_space)
        self.canvas.blit(self.draw_space,self.draw_space_rect)
        self.dirty = 1
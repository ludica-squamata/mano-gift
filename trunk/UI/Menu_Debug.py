from .Menu import Menu
from ._opcion import _opcion
from misc import Resources as r
from globs import World as W, Constants as C
from pygame import Surface, font, sprite
import os

class Menu_Debug (Menu):
    mapas = []
    elegir_uno = False
    sel = 0
    def __init__ (self):
        super().__init__("Mano-Gift:Debug Screen")
        self.funciones = {
            'arriba':self.elegir_opcion,
            'abajo':self.elegir_opcion,
            'izquierda':lambda dummy:None,
            'derecha':lambda dummy:None,
            'hablar':self.cargar_mapa}
        self.filas = sprite.LayeredDirty()
        self.crear_espacio_de_mapas(C.ANCHO-37,200)
    
    def cargar_mapas_iniciales(self):
        ok = []
        for mapa in os.listdir('data/maps'):
            ar = r.abrir_json('data/maps/'+mapa)
            if 'inicial' in ar['entradas']:
                ok.append(mapa[0:-5])
        
        return ok
    
    def crear_espacio_de_mapas (self,ancho,alto):
        mapas = self.crear_espacio_titulado(ancho,alto,'Elija un mapa')
        rect = self.canvas.blit(mapas,(7,40))
        self.draw_space = mapas.subsurface(((0,0),(rect.w-8,rect.h-30)))
        self.draw_space.fill(self.bg_cnvs)
        self.draw_space_rect = mapas.get_rect(topleft=(11,65))
        self.canvas.blit(self.draw_space,self.draw_space_rect)
        
        fuente = font.SysFont('verdana', 16)
        self.altura_del_texto = h = fuente.get_height()+1
        self.mapas = self.cargar_mapas_iniciales() # lista
        self.opciones = len(self.mapas)
        for i in range(len(self.mapas)):
            opcion = _opcion(self.mapas[i],self.draw_space_rect.w,(0,i*h+i+2))
            self.filas.add(opcion)
        
        self.filas.draw(self.draw_space)
    
    def elegir_opcion(self,direccion):
        if direccion == 'arriba': i = -1
        elif direccion == 'abajo': i = +1
        self.DeselectAll(self.botones)
        self.elegir_uno = True
        self.sel = self.dibujar_lineas_cursor (i,self.draw_space,self.draw_space_rect.w-12,self.sel,self.opciones)
    
    def cargar_mapa(self):
        W.cargar_hero()
        W.setear_mapa(self.mapas[self.sel-1], 'inicial')
        W.MAPA_ACTUAL.endDialog()
        W.onPause = False
    
    def update(self):
        self.canvas.blit(self.draw_space,self.draw_space_rect)
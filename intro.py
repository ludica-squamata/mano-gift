# intro.py
# módulo de introducción y selección de modo.
from pygame import Surface, Rect, QUIT, KEYDOWN, KEYUP, sprite, Color
from pygame import display as pantalla, event as EVENT,font
from globs import Tiempo as T, Constants as C, World as W
from misc import Resources as r, Util
from UI import Menu_Debug
from libs.textrect import render_textrect
import os,os.path

###TODO###
# menu de selección (opciones):
# # game (deshabilitada)
# # configuracion (deshabilitada)
# # debug screen
# # # seleccion de mapa.
# # # play.

class introduccion (Menu_Debug):
    running = True
    def __init__ (self):
        super().__init__()
        
    def ejecutar (self,fondo):
        while self.running:
            T.FPS.tick(60)
            for event in EVENT.get():
                if event.type == QUIT:
                    Util.salir()
                    
                elif event.type == KEYDOWN:
                    if event.key == C.TECLAS.SALIR:
                        Util.salir()
                    
                    elif event.key == C.TECLAS.IZQUIERDA:
                        self.usar_funcion('izquierda')
                        
                    elif event.key == C.TECLAS.DERECHA:
                        self.usar_funcion('derecha')
                    
                    elif event.key == C.TECLAS.ARRIBA:
                        self.usar_funcion('arriba')
                    
                    elif event.key == C.TECLAS.ABAJO:
                        self.usar_funcion('abajo')
                    
                    elif event.key == C.TECLAS.HABLAR:
                        self.running = False
                        self.usar_funcion('hablar')
                        break
            
            self.update()
            fondo.blit(self.canvas,(10,10))
            pantalla.update()

class intro:
    timer = 0
    def __init__(self,fondo):        
        self.fuente_1 = font.SysFont('Verdana',24,bold=True)
        self.nombre = 'Lúdica Squamata'
        w,h = self.fuente_1.size(self.nombre)
        self.nom_rect = Rect((0,0),(w,h+10))
        
        self.fuente_2 = font.SysFont('Verdana',16,italic=True)
        self.presenta ='Presenta...'
        w,h = self.fuente_2.size(self.presenta)
        self.pre_rect = Rect((0,0),(w,h+10))
        
        self.fuente_3 = font.SysFont('Verdana',16)
        self.produccion = 'una producción de\nZeniel Danaku & Einacio Spiegel'
        w,h = self.fuente_3.size(self.produccion)
        self.pro_rect = Rect((0,0),(w,h+40))
        
        self.fuente_4 = font.SysFont('Verdana',30,bold=True)
        self.titulo = 'Proyecto\nMano-Gift'
        w,h = self.fuente_4.size(self.titulo)
        self.ttl_rect = Rect((0,0),(C.ANCHO,h+40))
        
        self.continuar = '< Presione una tecla para continuar >'
        w,h = self.fuente_3.size(self.continuar)
        self.cont_rect = Rect(0,0,C.ANCHO,h+10)
        
        self.rojo = Color(255,0,0)
        self.verde = Color(0,255,0)
        self.azul = Color(0,0,255)
        self.negro = Color(0,0,0)
        self.blanco = Color(255,255,255)
        self.gris = Color(125,125,125)
        
        self.go(fondo)
    
    def go(self,fondo):
        running = 1
        j = 0
        while running == 1:
            T.FPS.tick(60)
            for event in EVENT.get():
                if event.type == QUIT: running = 0
                
                if event.type == KEYDOWN:
                    if event.key == C.TECLAS.SALIR:
                        Util.salir()
                    else:
                        running = 0
            self.timer += 1
            if self.timer <= 60:
                fondo.fill(self.negro)
            
            # Lúdica Squamata
            i = 0
            render = render_textrect(self.nombre,self.fuente_1,self.nom_rect,self.azul,self.negro)
            if 61 <= self.timer <180:
                i+=10
                render.set_alpha(i)
                fondo.blit(render,(192,192))
            
            # Presenta...
            i = 0
            render = render_textrect(self.presenta,self.fuente_2,self.pre_rect,self.verde,self.negro)
            if 181 <= self.timer < 300:
                i += 10
                render.set_alpha(i)
                fondo.blit(render,(288,230))
            
            # Una producción de Zeniel Danaku & Einacio Spiegel    
            i = 0
            render = render_textrect(self.produccion,self.fuente_3,self.pro_rect,self.rojo,self.negro,1)
            if 301 <= self.timer < 600:
                i += 10
                render.set_alpha(i)
                fondo.blit(render,(32,192))
            
            # Proyecto Mano-Gift 
            render = render_textrect(self.titulo,self.fuente_4,self.ttl_rect,self.negro,self.blanco,1)
            if 601 <= self.timer < 661:
                fondo.fill(self.blanco)
            
            if 662 <= self.timer < 900:
                fondo.blit(render,(0,96))
            
            # <Presione una tecla para continuar>
            if self.timer > 1200:
                j += 1
                h = self.fuente_3.get_height()
                render = render_textrect(self.continuar,self.fuente_3,self.cont_rect,self.rojo,self.blanco,1)
                
                if j <= 32:
                    fondo.blit(render,(0,332))
                elif j <= 64:
                    fondo.fill(self.blanco,(0,332,C.ANCHO,h+10))
                else:
                    j = 0
                
            pantalla.flip()
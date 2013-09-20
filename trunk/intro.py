# intro.py
# módulo de introducción y selección de modo.
from pygame import Surface, Rect, QUIT, KEYDOWN
from pygame import display as pantalla, event as EVENT,quit as py_quit,font
from globs import Tiempo as T, Constants as C
from UI import Menu
import sys 

# tiene una duración
# es previo al mainloop
# comienza con un cuadro negro
# aparece (fundido) el logo (o el titulo) Virtual Interactive
# presenta... (o en inglés, presents...)
# un juego de Lúdica Squamata
# a Ludica Squamata game
# ...
# Proyect Mano Gift
# menu de selección (opciones):
# # game (deshabilitada)
# # configuracion (deshabilitada)
# # debug screen
# # # seleccion de mapa.
# # # play.
class introduccion (Menu):
    canvas = ''
    running = True
    #bg_color = 0,0,0
    #fg_color = 0,0,255
    #bg_cnvs = 125,125,125
    #bg_bisel_bg = 175,175,175
    #bg_bisel_fg = 100,100,100
    #
    def __init__ (self,ancho,alto):
        self.canvas = self.crear_canvas(ancho,alto)
        self.crear_titulo("Mano-Gift",self.font_high_color,self.bg_cnvs,ancho)
    
    def ejecutar (self,fondo):
        while self.running:
            T.FPS.tick(60)
            for event in EVENT.get():
                if event.type == QUIT:
                    py_quit()
                    sys.exit()
                    
                elif event.type == KEYDOWN:
                    if event.key == C.TECLAS.MENU:
                        self.running = False
                        
                    elif event.key == C.TECLAS.SALIR:
                        py_quit()
                        print('Saliendo...')
                        sys.exit()
                        
            fondo.blit(self.canvas,(10,10))
            pantalla.update()
            
    def seleccion_mapa(self):
        pass
    def play (self):
        pass
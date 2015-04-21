# intro.py
# módulo de introducción y selección de modo.
from pygame import Surface, Rect, QUIT, KEYDOWN, KEYUP, sprite, Color
from pygame import display as pantalla, event as EVENT,font
from engine.globs import Tiempo as T, Constants as C
from engine.libs.textrect import render_textrect
from engine.misc import Util
import os,os.path

###TODO###
# menu de selección (opciones):
# # game (deshabilitada)
# # configuracion (deshabilitada)
# # debug screen
# # # seleccion de mapa.
# # # play.

def intro (fondo):
    timer = 0
    _rect = fondo.get_rect()
    
    fuente_1 = font.SysFont('Verdana',24,bold=True)
    nombre = 'Lúdica Squamata'
    w,h = fuente_1.size(nombre)
    nom_rect = Rect((0,0),(w,h+10))
    nom_rect.center = _rect.center
    
    fuente_2 = font.SysFont('Verdana',16,italic=True)
    presenta ='Presenta...'
    w,h = fuente_2.size(presenta)
    pre_rect = Rect((0,C.ALTO//2+10),(w,h+10))
    pre_rect.centerx = _rect.centerx+30
    
    fuente_3 = font.SysFont('Verdana',16)
    produccion = 'una producción de\nZeniel Danaku & Einacio Spiegel'
    w,h = fuente_3.size(produccion)
    pro_rect = Rect((0,0),(w,h+40))
    pro_rect.center = _rect.center
    
    fuente_4 = font.SysFont('Verdana',30,bold=True)
    titulo = 'Proyecto\nMano-Gift'
    w,h = fuente_4.size(titulo)
    ttl_rect = Rect((0,30),(C.ANCHO,h+40))
    ttl_rect.centerx = _rect.centerx
    
    continuar = '< Presione una tecla para continuar >'
    w,h = fuente_3.size(continuar)
    cont_rect = Rect(0,C.ALTO-(h+30),C.ANCHO,h+10)
    cont_rect.centerx = _rect.centerx
    
    rojo = Color(255,0,0)
    verde = Color(0,255,0)
    amarillo = Color(255,255,0)
    negro = Color(0,0,0)
    blanco = Color(255,255,255)
    gris = Color(125,125,125)
    
    
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
        timer += 1
        if timer <= 60:
            fondo.fill(negro)
        
        # Lúdica Squamata
        i = 0
        render = render_textrect(nombre,fuente_1,nom_rect,verde,negro,1)
        if 61 <= timer <180:
            i+=10
            render.set_alpha(i)
            fondo.blit(render,nom_rect)
        
        # Presenta...
        i = 0
        render = render_textrect(presenta,fuente_2,pre_rect,amarillo,negro)
        if 181 <= timer < 300:
            i += 10
            render.set_alpha(i)
            fondo.blit(render,pre_rect)
        
        # Una producción de Zeniel Danaku & Einacio Spiegel    
        i = 0
        render = render_textrect(produccion,fuente_3,pro_rect,rojo,negro,1)
        
        if 301 <= timer < 600:
            
            i += 10
            render.set_alpha(i)
            fondo.blit(render,pro_rect)
        
        # Proyecto Mano-Gift 
        render = render_textrect(titulo,fuente_4,ttl_rect,negro,blanco,1)
        if 601 <= timer < 661:
            fondo.fill(blanco)
        
        if 662 <= timer < 900:
            fondo.blit(render,ttl_rect)
        
        # <Presione una tecla para continuar>
        if timer > 1200:
            j += 1
            h = fuente_3.get_height()
            render = render_textrect(continuar,fuente_3,cont_rect,rojo,blanco,1)
            
            if j <= 32:
                fondo.blit(render,cont_rect)
            elif j <= 64:
                fondo.fill(blanco,cont_rect)
            else:
                j = 0
            
        pantalla.flip()
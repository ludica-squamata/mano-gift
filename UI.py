import pygame
from libs.textrect import render_textrect
from globs import fondo, pantalla, Constants as C


class Dialog:
    def __init__(self, texto):
        self.texto = texto
    
    def show(self):
        fuente = pygame.font.Font(None, 22)
        fg_color = 0,255,0
        bg_color = 0,0,0
        rect = pygame.Rect((30, 325, C.ANCHO, int(C.ALTO/5)))
        
        render = render_textrect(self.texto,fuente,rect,fg_color,bg_color)
        fondo.blit(render,(0,400))
        pantalla.update()

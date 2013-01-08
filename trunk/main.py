#import pygame
from mapa import Stage
import mobs
import misc

pygame.init()

tamanio = alto, ancho = 512,512
blanco = 255,255,255
pantalla = pygame.display.set_mode(tamanio)
pantalla.fill(blanco)

running = 1
while running == 1:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running=0
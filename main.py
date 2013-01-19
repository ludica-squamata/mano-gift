import pygame
import sys
from mapa import Stage
from mobs import PC
import misc

pygame.init()

tamanio = alto, ancho = 512,512
blanco = 255,255,255
pantalla = pygame.display
fondo = pantalla.set_mode(tamanio)
fondo.fill(blanco)
fondo_r = fondo.get_rect()
FPS = pygame.time.Clock()
pygame.key.set_repeat(30,15)

hero = PC('grafs/hero_ph.png')
fondo.blit(hero.sprite,hero.pos)


while True:
    try:
        FPS.tick(30)
        fondo.fill(blanco)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                key = pygame.key.name(event.key)
                if key == 'left':
                    hero.reubicar(-1,0)
    
                elif key == 'right':
                    hero.reubicar(+1,0)
    
                elif key == 'up':
                    hero.reubicar(0,-1)
    
                elif key == 'down':
                    hero.reubicar(0,+1)
                
                elif key == 'return': # debug
                    print (hero.pos)    
    
        fondo.blit(hero.sprite,hero.pos)
        pantalla.update([hero.rect,fondo_r])
    except Exception: # debug
        file = open('error.txt','w')
        file.write(Exception)
        file.close()
        sys.exit()
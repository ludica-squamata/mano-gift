import pygame,sys
from mapa import Stage,Prop
from mobs import PC
from misc import Resources as r
from globs import Constants as C, World as W

pygame.init()

tamanio = C.ALTO, C.ANCHO
pantalla = pygame.display # screen
fondo = pantalla.set_mode(tamanio) # surface
FPS = pygame.time.Clock()
pygame.key.set_repeat(30,15)


W.cargar_hero()
W.setear_mapa('map1', 'inicial')
rect_fondo = W.MAPA_ACTUAL.render(fondo)

while True:
        FPS.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                dx = 0
                dy = 0
                if event.key == pygame.K_LEFT:
                    dx +=1

                elif event.key == pygame.K_RIGHT:
                    dx -= 1

                elif event.key == pygame.K_UP:
                    dy += 1

                elif event.key == pygame.K_DOWN:
                    dy -= 1

                elif event.key == pygame.K_RETURN: # debug
                    print (W.HERO.mapX, W.HERO.mapY)
                    print(W.MAPA_ACTUAL.mapa.mask.overlap(W.HERO.mask,(W.HERO.mapX,W.HERO.mapY)))

                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                W.MAPA_ACTUAL.mover(dx,dy)

        cambios = W.MAPA_ACTUAL.render(fondo)
        #fondo.blit(hero.sprite,hero.pos)
        pantalla.update(cambios)

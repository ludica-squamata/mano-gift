import pygame,sys
from mapa import Stage
from mobs import PC
from misc import Resources as r
from globs import Constants as C

pygame.init()

tamanio = C.ALTO, C.ANCHO
negro = pygame.Color('black')
pantalla = pygame.display # screen
fondo = pantalla.set_mode(tamanio) # surface
mapa = Stage(r.abrir_json('maps/map1.json'),C.CUADRO)
FPS = pygame.time.Clock()
pygame.key.set_repeat(30,15)

hero = PC('grafs/hero_ph.png')
rect_fondo = mapa.render(fondo)

mapa.cargar_hero(hero, 'inicial')

while True:
        FPS.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    mapa.mover(1,0)

                elif event.key == pygame.K_RIGHT:
                    mapa.mover(-1,0)

                elif event.key == pygame.K_UP:
                    mapa.mover(0,+1)

                elif event.key == pygame.K_DOWN:
                    mapa.mover(0,-1)

                elif event.key == pygame.K_RETURN: # debug
                    print (hero.mapX, hero.mapY)
                    print(mapa.mapa.mask.overlap(hero.mask,(hero.mapX,hero.mapY)))

                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        cambios = mapa.render(fondo)
        #fondo.blit(hero.sprite,hero.pos)
        pantalla.update(cambios)

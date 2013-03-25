import pygame,sys,os
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
                os.system(['clear','cls'][os.name == 'nt'])
                print(W.mapas)
                print(W.MAPA_ACTUAL)
                print(W.MAPA_ACTUAL.contents.get_sprites_from_layer(C.CAPA_GROUND_ITEMS))
                print ("x:",W.HERO.mapX, "y:",W.HERO.mapY,'\n')
                print ("Gx:",str(int(W.HERO.mapX/32)), "Gy:",str(int(W.HERO.mapY/32)),'\n')
                print("Colisión:", str(W.MAPA_ACTUAL.mapa.mask.overlap(W.HERO.mask,(W.HERO.mapX,W.HERO.mapY))))

            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            W.MAPA_ACTUAL.mover(dx,dy)

        elif event.type == pygame.USEREVENT:
            W.setear_mapa(event.dict['dest'], event.dict['link'])
            #print('Alcanzada una salida!',event,sep = '\n')

    cambios = W.MAPA_ACTUAL.render(fondo)
    pantalla.update(cambios)

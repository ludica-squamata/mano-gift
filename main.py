import pygame,sys,os
from mapa import Stage,Prop
from mobs import PC
from misc import Resources as r
from globs import Constants as C, World as W

configs = r.abrir_json('config.json')

pygame.init()

tamanio = C.ALTO, C.ANCHO
pantalla = pygame.display # screen
fondo = pantalla.set_mode(tamanio) # surface
FPS = pygame.time.Clock()
pygame.key.set_repeat(30,15)

W.cargar_hero()
W.setear_mapa(configs['mapa_inicial'], 'inicial')

while True:
    FPS.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            dx = 0
            dy = 0
            if event.key == C.TECLAS.IZQUIERDA: 
                W.HERO.cambiar_direccion('derecha')
                dx +=1

            elif event.key == C.TECLAS.DERECHA:
                W.HERO.cambiar_direccion('izquierda')
                dx -= 1

            elif event.key == C.TECLAS.ARRIBA:
                W.HERO.cambiar_direccion('arriba')
                dy += 1

            elif event.key == C.TECLAS.ABAJO:
                W.HERO.cambiar_direccion('abajo')
                dy -= 1
            
            elif event.key == C.TECLAS.ACCION:
                print('Presionada la tecla de acción, oh yeah!')
            
            elif event.key == C.TECLAS.MENU: # debug
                os.system(['clear','cls'][os.name == 'nt'])
                print('Este sería el menú :P')
                #print(W.mapas)
                #print(W.MAPA_ACTUAL)
                #print(W.MAPA_ACTUAL.data)
                #for x in W.MAPA_ACTUAL.contents.get_sprites_from_layer(C.CAPA_GROUND_ITEMS):
                #    print(x.mask.overlap(W.HERO.mask,(x.mapX - W.HERO.mapX, x.mapY - (W.HERO.mapY - dy))))
                #    print(W.HERO.mask.overlap(x.mask,(x.mapX - W.HERO.mapX, x.mapY - (W.HERO.mapY - dy))))
                #    print(x.rect, x.mask.get_size())
                #
                #print (W.HERO.rect)
                #print ("x:",W.HERO.mapX, "y:",W.HERO.mapY,'\n')
                #print ("Gx:",str(int(W.HERO.mapX/32)), "Gy:",str(int(W.HERO.mapY/32)),'\n')
                #print("Colisión:", str(W.MAPA_ACTUAL.mapa.mask.overlap(W.HERO.mask,(W.HERO.mapX,W.HERO.mapY))))
            
            elif event.key == C.TECLAS.SALIR:
                pygame.quit()
                print('Saliendo...')
                sys.exit()

            W.MAPA_ACTUAL.mover(dx,dy)

    cambios = W.MAPA_ACTUAL.render(fondo)
    pantalla.update(cambios)

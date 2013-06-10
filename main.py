import pygame,sys,os
from mapa import Stage,Prop
from mobs import PC
from misc import Resources as r
from globs import Constants as C, World as W,FPS

configs = r.abrir_json('config.json')

pygame.init()
tamanio = C.ALTO, C.ANCHO
pantalla = pygame.display # screen
fondo = pantalla.set_mode(tamanio) # surface
pygame.key.set_repeat(30,15)

W.cargar_hero()
W.setear_mapa(configs['mapa_inicial'], 'inicial')

inAction = False
#FPS_f = pygame.font.Font(pygame.font.match_font('Courier New,Arial'),20)
onSelect = False
while True:
    FPS.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYUP:
            if event.key == C.TECLAS.ACCION or event.key == C.TECLAS.HABLAR:
                inAction = False

        elif event.type == pygame.KEYDOWN:
            dx,dy = 0,0
            if W.onDialog:
                if W.onSelect:
                    if event.key == C.TECLAS.ARRIBA:
                        W.HERO.cambiar_opcion_dialogo(-1)
        
                    elif event.key == C.TECLAS.ABAJO:
                        W.HERO.cambiar_opcion_dialogo(+1)
                                        
            else:
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
                    
            if event.key == C.TECLAS.ACCION:
                if not inAction:
                    W.HERO.accion()
                    inAction = True

            elif event.key == C.TECLAS.HABLAR:
                if not inAction:
                    if W.onSelect:
                        W.HERO.confirmar_seleccion()
                    else:
                        W.onDialog = W.HERO.hablar()
                    inAction = True

            elif event.key == C.TECLAS.CANCELAR_DIALOGO:
                if W.onDialog:
                    W.MAPA_ACTUAL.endDialog()
                    W.onDialog = False

            elif event.key == C.TECLAS.INVENTARIO:
                if not inAction:
                    W.HERO.ver_inventario()
                    W.onDialog = True
                    inAction = True
                        

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
                print (W.HERO.rect)
                print ("map_x:",W.HERO.mapX, "map_y:",W.HERO.mapY,'\n')
                print ("Gx:",str(int(W.HERO.mapX/32)), "Gy:",str(int(W.HERO.mapY/32)),'\n')
                print(W.HERO.direccion)

            elif event.key == C.TECLAS.SALIR:
                    pygame.quit()
                    print('Saliendo...')
                    sys.exit()

            W.MAPA_ACTUAL.mover(dx,dy)

    cambios = W.MAPA_ACTUAL.render(fondo)
    #fondo.blit((FPS_f.render(str(int(FPS.get_fps())),False,(255,255,255,255))),(0,0))
    pantalla.update(cambios)

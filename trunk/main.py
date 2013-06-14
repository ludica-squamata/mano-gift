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
pygame.key.set_repeat(50,15)

W.cargar_hero()
W.setear_mapa(configs['mapa_inicial'], 'inicial')
sel = 0
inAction = False
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
            if event.key == C.TECLAS.IZQUIERDA:
                if not W.onPause:
                    if not W.onDialog:
                        W.HERO.cambiar_direccion('derecha')
                        dx +=1
                else:
                    W.MENU.selectOne(+0,-1)

            elif event.key == C.TECLAS.DERECHA:
                if not W.onPause:
                    if not W.onDialog:
                        W.HERO.cambiar_direccion('izquierda')
                        dx -= 1
                else:
                    W.MENU.selectOne(+0,+1)
                    
            elif event.key == C.TECLAS.ARRIBA:
                if W.onDialog:
                    if W.onSelect:
                        W.HERO.cambiar_opcion_dialogo(-1)
                    elif W.onPause:
                        W.MENU.selectOne(-1,+0)
                else:
                    if not W.onPause:
                        W.HERO.cambiar_direccion('arriba')
                        dy += 1

            elif event.key == C.TECLAS.ABAJO:
                if W.onDialog:
                    if W.onSelect:
                        W.HERO.cambiar_opcion_dialogo(+1)
                    elif W.onPause:
                        W.MENU.selectOne(+1,+0)
                else:
                    if not W.onPause:
                        W.HERO.cambiar_direccion('abajo')
                        dy -= 1
                      
            elif event.key == C.TECLAS.ACCION:
                if not inAction:
                    W.HERO.accion()
                    inAction = True

            elif event.key == C.TECLAS.HABLAR:
                if not inAction:
                    if W.onSelect:
                        W.HERO.confirmar_seleccion()
                    else:
                        if not W.onPause:
                            W.onDialog = W.HERO.hablar()
                        inAction = True
                else:
                    W.MENU.cambiar_menu()
                        

            elif event.key == C.TECLAS.CANCELAR_DIALOGO:
                if W.onDialog:
                    if not W.onPause:
                        W.MAPA_ACTUAL.endDialog()

            elif event.key == C.TECLAS.INVENTARIO:
                if not inAction:
                    if not W.onPause:
                        W.HERO.ver_inventario()
                        W.onDialog = True
                        inAction = True
                else:
                    if not W.onPause:
                        inAction = False
                        W.MAPA_ACTUAL.endDialog()
                    
            elif event.key == C.TECLAS.MENU:
                if not inAction:
                    if not W.onPause:
                        W.MAPA_ACTUAL.popMenu()
                        inAction = True
                else:
                    inAction = False
                    W.onPause = False
                    W.MAPA_ACTUAL.endDialog()
                
            elif event.key == C.TECLAS.SALIR:
                    pygame.quit()
                    print('Saliendo...')
                    sys.exit()

            W.MAPA_ACTUAL.mover(dx,dy)

    cambios = W.MAPA_ACTUAL.render(fondo)
    pantalla.update(cambios)

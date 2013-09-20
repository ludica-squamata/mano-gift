import sys
from pygame import display as pantalla # screen
from pygame import event as EVENT, image, font
from pygame import QUIT, KEYUP, KEYDOWN
from pygame import quit as py_quit
from misc import Resources as r
from globs import Constants as C, World as W, Tiempo as T, QuestManager
from intro import introduccion

configs = r.abrir_json('config.json')

tamanio = C.ALTO, C.ANCHO
font.init()
pantalla.set_icon(image.load('D:/python/gift/favicon.png'))
pantalla.set_caption('Proyecto Mano-Gift')
fondo = pantalla.set_mode(tamanio) # surface

init = introduccion(C.ANCHO-20,C.ALTO-20)
init.ejecutar(fondo)

W.cargar_hero()
W.setear_mapa(configs['mapa_inicial'], 'inicial')
inAction = False

dx,dy = 0,0
while True:
    T.FPS.tick(60)
    T.contar_tiempo()
    QuestManager.update()
    for event in EVENT.get():
        if event.type == QUIT:
            sys.exit()

        elif event.type == KEYUP:
            if event.key == C.TECLAS.ACCION or event.key == C.TECLAS.HABLAR:
                inAction = False
                if W.onDialog and W.onPause and not W.onVSel:
                    W.MAPA_ACTUAL.popMenu(W.menu_actual.current.nombre)
            
            elif event.key == C.TECLAS.IZQUIERDA or event.key == C.TECLAS.DERECHA:
                if not W.onPause and not W.onDialog:
                    dx = 0
            elif event.key == C.TECLAS.ABAJO or event.key == C.TECLAS.ARRIBA:
                if not W.onPause and not W.onDialog:
                    dy = 0

        elif event.type == KEYDOWN:
            if event.key == C.TECLAS.IZQUIERDA:
                if not W.onPause:
                    if not W.onDialog:
                        dx +=1
                else:
                    W.menu_actual.selectOne('izquierda')

            elif event.key == C.TECLAS.DERECHA:
                if not W.onPause:
                    if not W.onDialog:
                        dx -= 1                        
                else:
                    W.menu_actual.selectOne('derecha')
                    
            elif event.key == C.TECLAS.ARRIBA:
                if W.onDialog:
                    if W.onSelect:
                        W.DIALOG.elegir_opcion(-1)
                    elif W.onPause:
                        if not W.onVSel:
                            W.menu_actual.selectOne('arriba')
                        else:
                            W.menu_actual.elegir_fila(-1)
                else:
                    if not W.onPause:
                        dy += 1

            elif event.key == C.TECLAS.ABAJO:
                if W.onDialog:
                    if W.onSelect:
                        W.DIALOG.elegir_opcion(+1)
                    elif W.onPause:
                        if not W.onVSel:
                            W.menu_actual.selectOne('abajo')
                        else:
                            W.menu_actual.elegir_fila(+1)
                else:
                    if not W.onPause:
                        dy -= 1
                      
            elif event.key == C.TECLAS.ACCION:
                if not inAction:
                    W.HERO.accion()
                    inAction = True

            elif event.key == C.TECLAS.HABLAR:
                if W.onDialog and W.onPause:
                    if W.onVSel:
                        W.menu_actual.confirmar_seleccion()
                    else:
                        W.menu_actual.PressOne()
                if not inAction:
                    if W.onSelect:
                        W.HERO.confirmar_seleccion()
                    else:
                        if not W.onPause:
                            W.onDialog = W.HERO.hablar()
                    inAction = True

            elif event.key == C.TECLAS.CANCELAR_DIALOGO:
                if W.onDialog:
                    W.MAPA_ACTUAL.endDialog()
                    W.onPause = False

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
                        W.MAPA_ACTUAL.popMenu('Pausa')
                        inAction = True
                else:
                    inAction = False
                    W.onPause = False
                    W.MAPA_ACTUAL.endDialog()
                
            elif event.key == C.TECLAS.SALIR:
                    py_quit()
                    print('Saliendo...')
                    sys.exit()
            
            elif event.key == C.TECLAS.POSICION_COMBATE:
                W.HERO.cambiar_estado()

    if dx != 0 or dy != 0:
        W.HERO.mover(-dx,-dy)
        W.MAPA_ACTUAL.mover(dx,dy)

    cambios = W.MAPA_ACTUAL.update(fondo)
    pantalla.update(cambios)


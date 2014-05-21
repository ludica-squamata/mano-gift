from pygame import QUIT, KEYUP, KEYDOWN
from globs import Constants as C, World as W
from misc import Util
from UI.menues import *

class modo:
    dx,dy = 0,0
    onSelect = False
    newMenu = False
    onVSel = False
    setKey = False
    def Juego (events):
        for event in events:
            if event.type == QUIT:
                Util.salir()
            
            elif event.type == KEYDOWN:
                if event.key == C.TECLAS.SALIR:
                    Util.salir()
                
                elif event.key == C.TECLAS.DEBUG:
                    print('map: ',(W.HERO.mapX, W.HERO.mapY))
                    print('rect: ',(W.HERO.rect.x,W.HERO.rect.y))
    
    def Aventura(events,fondo):
        dx, dy = modo.dx, modo.dy
        for event in events:
            if event.type == KEYDOWN:
                if event.key == C.TECLAS.IZQUIERDA: dx -= 1
                elif event.key == C.TECLAS.DERECHA: dx += 1
                elif event.key == C.TECLAS.ARRIBA:  dy -= 1
                elif event.key == C.TECLAS.ABAJO:   dy += 1
                    
                elif event.key == C.TECLAS.HABLAR:
                    if W.HERO.hablar():
                        W.MODO = 'Dialogo'
                    else:
                        W.MODO = 'Aventura'                   
                    
                elif event.key == C.TECLAS.INVENTARIO:
                    W.MODO = 'Dialogo'
                    modo.onVSel = True
                    W.HERO.ver_inventario()
                
                elif event.key == C.TECLAS.POSICION_COMBATE:
                    W.HERO.cambiar_estado()
                
                elif event.key == C.TECLAS.ACCION:
                    W.HERO.accion()
                
                elif event.key == C.TECLAS.MENU:
                    W.onPause = True
                    W.MODO = 'Menu'
                    modo._popMenu('Pausa')
                
                elif event.key == C.TECLAS.CANCELAR_DIALOGO:
                    modo.endDialog()
                    
            elif event.type == KEYUP:
                if event.key == C.TECLAS.IZQUIERDA or event.key == C.TECLAS.DERECHA:
                    dx = 0
                elif event.key == C.TECLAS.ABAJO or event.key == C.TECLAS.ARRIBA:
                    dy = 0
        
        if dx != 0 or dy != 0:
            cx,cy = W.HERO.mover(dx,dy)
            if W.RENDERER.camara.isFocus(W.HERO):
                W.RENDERER.camara.panear(-cx,-cy)
        modo.dx, modo.dy = dx, dy
        
        return W.RENDERER.update(fondo)
    
    def Dialogo(events,fondo):
        for event in events:
            if event.type == KEYDOWN:
                if event.key == C.TECLAS.ARRIBA: W.DIALOG.elegir_opcion(-1)
                elif event.key == C.TECLAS.ABAJO: W.DIALOG.elegir_opcion(+1)
                
                elif event.key == C.TECLAS.HABLAR:
                    W.DIALOG.usar_funcion('hablar')
                
                elif event.key == C.TECLAS.INVENTARIO:
                    modo.endDialog()
                    W.MODO = 'Aventura'
                    modo.onVSel = False
                
                elif event.key == C.TECLAS.CANCELAR_DIALOGO:
                    modo.endDialog()
                    pass # cancelaria el dialogo como lo hace ahora.

        return W.RENDERER.update(fondo)
    
    def Menu(events,fondo):
        for event in events:
            if event.type == KEYDOWN:
                if modo.setKey:
                    W.menu_actual.cambiarTecla(event.key)
                    modo.setKey = False
                else:
                    if event.key == C.TECLAS.IZQUIERDA:
                        W.menu_actual.usar_funcion('izquierda')
                    
                    elif event.key == C.TECLAS.DERECHA:
                        W.menu_actual.usar_funcion('derecha')
                    
                    elif event.key == C.TECLAS.ARRIBA:
                        W.menu_actual.usar_funcion('arriba')
                            
                    elif event.key == C.TECLAS.ABAJO:
                        W.menu_actual.usar_funcion('abajo')
                    
                    elif event.key == C.TECLAS.HABLAR:
                        W.menu_actual.usar_funcion('hablar')
                    
                    elif event.key == C.TECLAS.CANCELAR_DIALOGO:
                        if W.menu_actual.cancelar():
                            'Retrocede al menú anterior, o sale del modo'
                            if W.menu_actual.nombre == 'Pausa':
                                modo.endDialog()
                                W.onPause = False
                            else:
                                W.menu_actual.active = False
                                modo._popMenu(W.menu_previo)
            
            elif event.type == KEYUP:
                if event.key == C.TECLAS.HABLAR:
                    if modo.newMenu:
                        modo._popMenu(W.menu_actual.current.nombre)
                        modo.newMenu = False
                    else:
                        W.menu_actual.keyup_function('hablar')
                                        
        return W.RENDERER.update(fondo)
    
    @staticmethod
    def _popMenu (titulo):
        if W.menu_previo == '' and W.menu_previo != titulo:
            W.menu_previo = titulo

        if titulo not in W.MENUS:
            try:
                menu = eval('Menu_'+titulo+'()')
            except Exception as Description:
                print('No se pudo abrir el menu porque:',Description)
                menu = Menu(titulo)
        else:
            menu = W.MENUS[titulo]
            menu.Reset()
        
        W.menu_actual = menu
        W.menu_actual.active = True
        W.RENDERER.overlays.add(menu)
        W.RENDERER.overlays.move_to_front(menu)
    
    @staticmethod
    def endDialog():
        W.RENDERER.overlays.empty()
        W.DIALOG = None
        W.MODO = 'Aventura'
from engine.globs import Constants as C, EngineData as ED
from engine.misc import Util
from .taphold import _filtrar
from pygame import KEYDOWN,QUIT,KEYUP
from engine.UI.menues import *

class modo:
    dx,dy = 0,0
    newMenu = False
    setKey = False
    
    def Juego(events):
        ED.HUD.update()
        for event in events:
            if event.type == QUIT:
                Util.salir()
            
            elif event.type == KEYDOWN:
                if event.key == C.TECLAS.SALIR:
                    Util.salir()
                
                elif event.key == C.TECLAS.DEBUG:
                    print('map: ',(ED.HERO.mapX, ED.HERO.mapY))
                    print('rect: ',(ED.HERO.rect.x,ED.HERO.rect.y))
    
    def Aventura(events,fondo):
        dx, dy = modo.dx, modo.dy
        for event in _filtrar(events):
            #if event.type == KEYDOWN:
            #    print(event)
            if event.type == C.TAP:
                if event.key == C.TECLAS.HABLAR:
                    if ED.HERO.hablar():
                        ED.MODO = 'Dialogo'
                    else:
                        ED.MODO = 'Aventura'
                
                #elif event.key == C.TECLAS.INVENTARIO:
                #    ED.MODO = 'Dialogo'
                #    ED.HERO.ver_inventario()
                
                elif event.key == C.TECLAS.POSICION_COMBATE:
                    ED.HERO.cambiar_estado()
                
                elif event.key == C.TECLAS.ACCION:
                    ED.HERO.accion()
                
                elif event.key == C.TECLAS.MENU:
                    ED.onPause = True
                    ED.MODO = 'Menu'
                    modo._popMenu('Pausa')
                
                elif event.key == C.TECLAS.IZQUIERDA: ED.HERO.cambiar_direccion('izquierda',True)
                elif event.key == C.TECLAS.DERECHA:   ED.HERO.cambiar_direccion('derecha',True)
                elif event.key == C.TECLAS.ARRIBA:    ED.HERO.cambiar_direccion('arriba',True)
                elif event.key == C.TECLAS.ABAJO:     ED.HERO.cambiar_direccion('abajo',True)
            
            elif event.type == C.HOLD:
                if event.key == C.TECLAS.IZQUIERDA: dx = -1
                elif event.key == C.TECLAS.DERECHA: dx = +1
                elif event.key == C.TECLAS.ARRIBA:  dy = -1
                elif event.key == C.TECLAS.ABAJO:   dy = +1
                
            elif event.type == C.RELEASE:
                if event.key == C.TECLAS.IZQUIERDA or event.key == C.TECLAS.DERECHA:
                    dx = 0
                elif event.key == C.TECLAS.ABAJO or event.key == C.TECLAS.ARRIBA:
                    dy = 0
            
        if dx != 0 or dy != 0:
            ED.HERO.mover(dx,dy)
        modo.dx, modo.dy = dx, dy
        
        return ED.RENDERER.update(fondo)
    
    def Dialogo(events,fondo):
        for event in _filtrar(events):
            if event.type == KEYDOWN:
                if event.key == C.TECLAS.ARRIBA:
                    ED.DIALOG.usar_funcion('arriba')
                
                elif event.key == C.TECLAS.ABAJO: 
                    ED.DIALOG.usar_funcion('abajo')
                
                elif event.key == C.TECLAS.IZQUIERDA:
                    ED.DIALOG.usar_funcion('izquierda')
                
                elif event.key == C.TECLAS.DERECHA: 
                    ED.DIALOG.usar_funcion('derecha')
                
                elif event.key == C.TECLAS.HABLAR:
                    ED.DIALOG.usar_funcion('hablar')
                
                elif event.key == C.TECLAS.INVENTARIO:
                    ED.DIALOG.usar_funcion('inventario')
                    
                elif event.key == C.TECLAS.CANCELAR_DIALOGO:
                    ED.DIALOG.usar_funcion('cancelar')
        
        return ED.RENDERER.update(fondo)
    
    def Menu(events,fondo):
        for event in events:
            if event.type == KEYDOWN:
                if modo.setKey:
                    ED.menu_actual.cambiarTecla(event.key)
                    modo.setKey = False
                else:
                    if event.key == C.TECLAS.IZQUIERDA:
                        ED.menu_actual.usar_funcion('izquierda')
                    
                    elif event.key == C.TECLAS.DERECHA:
                        ED.menu_actual.usar_funcion('derecha')
                    
                    elif event.key == C.TECLAS.ARRIBA:
                        ED.menu_actual.usar_funcion('arriba')
                            
                    elif event.key == C.TECLAS.ABAJO:
                        ED.menu_actual.usar_funcion('abajo')
                    
                    elif event.key == C.TECLAS.HABLAR:
                        ED.menu_actual.usar_funcion('hablar')
                    
                    elif event.key == C.TECLAS.CANCELAR_DIALOGO:
                        previo = ED.menu_actual.cancelar()#podría ser usar_funcion
                        if previo:
                            modo._popMenu(ED.menu_previo)
                        elif previo != None:
                            modo.endDialog(C.CAPA_OVERLAYS_MENUS)
            
            elif event.type == KEYUP:
                if event.key == C.TECLAS.HABLAR:
                    if modo.newMenu:
                        modo._popMenu(ED.menu_actual.current.nombre)
                        modo.newMenu = False
                    else:
                        ED.menu_actual.keyup_function('hablar')
                                        
        return ED.RENDERER.update(fondo)
    
    @staticmethod
    def _popMenu (titulo):
        if ED.menu_previo == '' and ED.menu_previo != titulo:
            ED.menu_previo = titulo

        if titulo not in ED.MENUS:
            try:
                menu = eval('Menu_'+titulo+'()')
            except Exception as Description:
                print('No se pudo abrir el menu porque:',Description)
                menu = Menu(titulo)
        else:
            menu = ED.MENUS[titulo]
            menu.Reset()
        
        ED.menu_actual = menu
        ED.RENDERER.addOverlay(menu,C.CAPA_OVERLAYS_MENUS)
        ED.RENDERER.overlays.move_to_front(menu)
    
    @staticmethod
    def endDialog(layer):
        ED.RENDERER.overlays.remove_sprites_of_layer(layer)
        ED.DIALOG = None
        ED.MODO = 'Aventura'
        ED.onPause = False
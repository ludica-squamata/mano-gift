import pygame,sys
from globs import World as W, Constants as C

class ModoDeJuego:
    modo = ''
    inAction = False
    def __init__(self, modo):
        self.modo = modo
    
    def mainloop(self):
        if self.modo == 'aventura':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                
                elif event.type == pygame.KEYUP:
                    if event.key == C.TECLAS.ACCION:
                        self.inAction = False
                        
                elif event.type == pygame.KEYDOWN:
                    dx,dy = 0,0
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
                        if not self.inAction:
                            onDialog = W.HERO.accion()
                            self.inAction = True
                            if onDialog:
                                self.modo = 'dialogo'
                    
                    elif event.key == C.TECLAS.INVENTARIO:
                        if not self.inAction:
                            W.HERO.ver_inventario()
                            self.inAction = True
                            
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
        
        elif self.modo == 'dialogo':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                        
                elif event.type == pygame.KEYDOWN:
                    if event.key == C.TECLAS.CONTROL:
                        self.modo = 'aventura'
                        W.MAPA_ACTUAL.dialogs.empty()
    

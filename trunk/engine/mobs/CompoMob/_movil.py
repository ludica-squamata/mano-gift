from engine.globs import Constants as C

class Movil:
    direcciones = {'abajo':[0,1],'izquierda':[1,0],'arriba':[0,-1],'derecha':[-1,0],'ninguna':[0,0]}
    direccion = 'abajo'
    modo_colision = None# determina qué direccion tomará el mob al chocar con algo
    
    def cambiar_direccion(self,arg):
        direccion = 'ninguna'
    
        if arg == 'contraria':
            if self.direccion == 'arriba': direccion = 'abajo'
            elif self.direccion == 'abajo': direccion = 'arriba'
            elif self.direccion == 'izquierda': direccion = 'derecha'
            elif self.direccion == 'derecha': direccion = 'izquierda'
    
        elif arg in self.direcciones:
            direccion = arg
            
        self.direccion = direccion
        return direccion
    
    def mover(self):
        direccion = self.AI(self)
        self.cambiar_direccion(direccion)
        x,y = self.direcciones[self.direccion]
        dx,dy = x*self.velocidad,y*self.velocidad

        if self.detectar_colisiones(dx,dy):
            self.cambiar_direccion(self.modo_colision)
            x,y = self.direcciones[self.direccion]
            dx,dy = x*self.velocidad,y*self.velocidad
        
        self.animar_caminar()        
        self.reubicar(dx, dy)
        
        return dx,dy
                
    def detectar_colisiones(self,dx,dy):
        col_bordes = False #colision contra los bordes de la pantalla
        col_mobs = False #colision contra otros mobs
        col_heroe = False #colision contra el héroe
        col_props = False # colision contra los props
        col_mapa = False # colision contra las cajas de colision del propio mapa

        if self.solido:
            if self.stage.mapa.mask.overlap(self.mask,(self.mapX + dx, self.mapY)) is not None:
                col_mapa = True

            if self.stage.mapa.mask.overlap(self.mask,(self.mapX, self.mapY + dy)) is not None:
                col_mapa = True

            for spr in self.stage.properties.get_sprites_from_layer(C.CAPA_GROUND_ITEMS):
                if self.colisiona(spr,dx,dy):
                    if spr.solido:
                        if spr.accion == 'mover': spr.reubicar(dx,dy)
                        else: col_props = True
                        
            for spr in self.stage.properties.get_sprites_from_layer(C.CAPA_GROUND_MOBS):
                if spr.solido:
                    if self.colisiona(spr,dx,dy):
                        col_mobs = True
        
        newPos = self.mapX + dx
        if newPos < 0 or newPos > self.stage.mapa.rect.w-32:
            if C.ANCHO > self.rect.x - dx  >=0:
                col_bordes = True

        newPos = self.mapY + dy
        if newPos < 0 or newPos > self.stage.mapa.rect.h-32:
            if C.ALTO > self.rect.y - dy  >=0:
                col_bordes = True

        return any([col_bordes,col_mobs,col_props,col_mapa])
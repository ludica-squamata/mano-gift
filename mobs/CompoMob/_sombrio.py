class _shadowSprite:
    _sombras = [] #list
    _sprSombra = None #sprite
    proyectaSombra = True
    _luces = [0,0,0,0,0,0,0,0]

    def recibir_luz(self, source):
        if self.proyectaSombra:
            #calcular direccion de origen
            #marcar direccion como iluminada
            dx = self.centerX - source.centerX
            dy = self.centerY - source.centerY
            l = self._luces
            margen = 10 #para que las sombras no sean mayormente diagonales
                        #como alternativa podriamos calcular el angulo
            if dx > margen: #source esta a la izq
                if dy > margen: #arriba
                            l[7] = 1
                elif dy < -margen:
                        l[5] = 1
                else:
                        l[6] = 1
            elif dx < -margen:
                if dy > margen:
                        l[1] = 1
                elif dy < -margen:
                        l[3] = 1
                else:
                        l[2] = 1
            else:
                if dy > margen:
                        l[0] = 1
                else:
                        l[4] = 1
    
    def updateSombra(self):
             #
     
            #generar sombra en direccion contraria a los slots iluminados
            #si cambio la lista,
            #actualizar imagen de sombra y centrar
            
            #para el calculo de sombras ha de usarse la imagen que veria la fuente de luz.
            #ej: si el personaje estuviera en posicion D, la sombra O se hace en base a la imagen R
            # si estuviera en posicion U, se usaria L
            #esto es importante para que queden bien cosas como los brazos u adornos
            
            #a resolver: que imagen usar para las diagonales
            
            s = []
            l = self._luces
            
            for i in range(0,7):
                if s[i] = (l[(i+4) mod 7] - l[i]) == 1:
                    pass
            #s[0] = l[4] and not l[0]
            
            if s != self._sombras:
                pass
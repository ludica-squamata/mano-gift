import _giftSprite
    
class _shadowSprite(_giftSprite):
    _sombras = None #list
    proyectaSombra = True
    
    def recibir_luz(self, source):
        if self.proyectaSombra:
            #calcular direccion de origen
            #marcar direccion como iluminada
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
            pass
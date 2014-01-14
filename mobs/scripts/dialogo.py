
class _dialogo:
    textos = []
    pos = -1
    def __init__(self,textos):
        self.textos = textos
        # se tiene que registrar en el renderer.
     
    def avanzar (self):
        #return texto
        pass
    
    def opcion (self):
        pass
    
    def cerrar(self):
        pass
    
    
    def usar_funcion(self):
        if type(self.textos[self.pos]) != dict:
            texto = self.avanzar()
        else:
            pass
        
        # Dialog.setText(texto)
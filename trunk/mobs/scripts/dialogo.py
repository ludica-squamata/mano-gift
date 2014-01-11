
class _dialogo:
    textos = []
    pos = -1
    def __init__(self,textos):
        self.textos = textos        
     
    def avanzar (self):
        #return texto
        pass
    
    def opcion (self):
        pass
    
    def usar_funcion(self):
        if type(self.textos[self.pos]) != dict:
            texto = self.avanzar()
        else:
            pass
        
        # Dialog.setText(texto)
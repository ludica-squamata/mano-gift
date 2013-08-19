from collections import Counter
from globs import World as W

class Inventory(Counter):
    tamanio_max = 0
    
    def __init__(self,maximo):
        super().__init__()
        self.tamanio_max = maximo
    
    def ver (self):
        if len(self) < 1:
            texto = 'El inventario está vacío'
        else:
            texto = ', '.join(sorted([item.capitalize()+' x'+str(self[item]) for item in self]))
        
        return texto
        
    def agregar(self,nombre_item):
        if sum(self.values())+1 <= self.tamanio_max:
            if nombre_item in self:
                self[nombre_item] += 1
            else:
                self[nombre_item] = 1
            return True
        else:
            W.MAPA_ACTUAL.setDialog('Cantidad máxima de items alcanzada')
            return False
    
    def quitar (self,nombre_item):
        if self[nombre_item]-1 <= 0:
            del self[nombre_item]
            return 0
        else:
            self[nombre_item] -= 1
            return self[nombre_item]
    


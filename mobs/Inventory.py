from collections import UserDict
from .Item import Item

class Inventory(UserDict):
    tamanio_max = 0
    
    def __init__(self,maximo):
        super().__init__()
        self.tamanio_max = maximo
    
    def ver (self):
        if len(self) < 1:
            texto = 'El inventario está vacío'
        else:
            toJoin = []
            for key in self:
                if len(self[key]) > 0:
                    toJoin.append(key.capitalize()+' x'+str(len(self[key])))
            texto = ', '.join(toJoin)
        return texto

    def contar_items(self):
        cantidad = 0
        for key in self:
            cantidad += len(self[key])
        return cantidad
    
    def agregar(self,cosa):
        if self.contar_items()+1 <= self.tamanio_max:
            if cosa in self:
                self[cosa].append(Item(cosa))
            else:
                self[cosa] = [Item(cosa)]
            return True
        else:
            print('Cantidad máxima de items alcanzada')
            return False


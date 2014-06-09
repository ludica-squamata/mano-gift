from collections import UserList
from engine.globs import EngineData as ED
from .Item import Item

class Inventory(UserList):
    volumen_max = 0
    peso_max = 0

    def __init__(self,maxvol):
        super().__init__()
        self.volumen_max = maxvol
        self.peso_max = 1
    
    def _calcular_limites(self,elemento):
        volumen = 0
        peso = 0
        for item in self:
            volumen += item.volumen*item.cantidad
            peso += item.peso*item.cantidad
        
        if elemento.peso+peso > self.peso_max*ED.HERO.fuerza:
            #MAPA_ACTUAL.setDialog('No puedes cargar más peso del que llevas.')
            return False
        
        if elemento.volumen+volumen > self.volumen_max:
            #MAPA_ACTUAL.setDialog('El item no entra en la mochila.')
            return False
        
        return True    

    def agregar(self,item):
        if self._calcular_limites (item):
            if item in self:
                if item.esStackable:
                    self[self.index(item)].cantidad += 1
                else:
                    self.append(item)
            else:
                self.append(item)
            return True
        else:
            return False
    
    def quitar (self,item_id):
        for item in self:
            if item.ID == item_id:
                index = self.index(item)
                break
        
        if self[index].cantidad -1 <= 0:
            del self[index]
            return 0
        else:
            self[index].cantidad -= 1
            return self[index].cantidad
    
    def __contains__(self,item):
        if type(item) == str:
            #item es el nombre de un item
            for _item in self:
                if _item.nombre == item:
                    return True
            return False
        
        elif type(item) == int:
            #item es el ID de un item
            for _item in self:
                if _item.ID == item:
                    return True
            return False
        
        elif item.__class__ == Item:
            for _item in self:
                if _item.ID == item.ID:
                    return True
            return False
            
    



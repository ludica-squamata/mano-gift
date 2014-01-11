from collections import UserDict

class _giftGroup(UserDict):
    
    def add(self,spr):
        nombre = spr.nombre
        self[nombre]= spr
    
    def remove(self,spr):
        nombre = spr.nombre
        if nombre in self:
            del self[nombre]

MobGroup = _giftGroup()
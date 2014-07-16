class _giftGroup:
    _group = {}
    _indexes = []
    def __init__(self):
        self._group = {}
        self._indexes = []
        
    def __setitem__(self,key,value):
        if key not in self._group:
            self._group[key] = value
            self._indexes.append(key)
            
    def __getitem__(self,key):
        if key in self._group:
            return self._group[key]
        elif type(key) == int:
            if 0 <= key <= len(self._indexes)-1:
                return self._indexes[key]
            else:
                raise IndexError
        else:
            raise KeyError(key)
        
    def __delitem__(self,key):
        if key in self._group:
            del self._group[key]
        elif type(key) == int:
            if 0 <= key <= len(self._indexes)-1:
                del self._group[self._indexes[key]]
                del self._indexes[key]
            else:
                raise IndexError
        else:
            raise KeyError
    
    def __contains__(self,item):
        if type(item) == str:
            if item in self._group:
                return True
        elif type(item) == int:
            if 0 <= item <= len(self._indexes)-1:
                if self._indexes[item] in self._group:
                    return True
                else:
                    raise IndexError
        elif hasattr(item,'nombre'):
            if item.nombre in self._group:
                return True
        return False
    
    def __str__(self): 
        return 'MobGroup keys ('+','.join([self._group[i].nombre for i in self._indexes])+')'
    
    def add(self,mob):
        key = mob.nombre
        self.__setitem__(key,mob)
    
    def remove(self,mob):
        nombre = mob.nombre
        self.__delitem__(nombre)
    
    def get (self,mob):
        self.__getitem__(mob.nombre)

MobGroup = _giftGroup()
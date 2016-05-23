from .eventDispatcher import EventDispatcher


class MobGroup:
    """this is a dict that can be accessed by index"""

    _group = {}
    _indexes = []

    def __init__(self):
        self._group = {}
        self._indexes = []

        EventDispatcher.register(self.delete_mob, 'MobMuerto')

    def __setitem__(self, key, value):
        if key not in self._group:
            self._group[key] = value
            self._indexes.append(key)
        else:
            raise KeyError('Key "' + key + '" is already set. Replacing is not allowed.')

    def __getitem__(self, key):
        if key in self._group:
            return self._group[key]
        elif type(key) is int:
            if 0 <= key <= len(self._indexes) - 1:
                return self._group[self._indexes[key]]
            else:
                raise IndexError
        else:
            raise KeyError(key)

    def __delitem__(self, key):
        if key in self._group:
            self._indexes.remove(key)
            del self._group[key]

        elif type(key) is int:
            if 0 <= key <= len(self._indexes) - 1:
                del self._group[self._indexes[key]]
                del self._indexes[key]
            else:
                raise IndexError
        else:
            raise KeyError

    def __contains__(self, item):
        if type(item) is str:
            if item in self._group:
                return True
        elif type(item) is int:
            if 0 <= item <= len(self._indexes) - 1:
                if self._indexes[item] in self._group:
                    return True
                else:
                    raise IndexError
        elif hasattr(item, 'nombre'):
            if item.nombre in self._group:
                return True
        return False

    def delete_mob(self, event):
        nombre = event.data['obj'].nombre
        del self[nombre]

    def __str__(self):
        return 'MobGroup keys (' + ','.join([self._group[i].nombre for i in self._indexes]) + ')'

    def contents(self):
        return [self._group[key] for key in self._group]

class ItemGroup:

    _group = {}
    _indexes = []
    _lenght = 0

    def __init__(self):
        self._group = {}
        self._indexes = []
        self._lenght = 0

        EventDispatcher.register(self.delete_item, 'DelItem')

    def __setitem__(self, key, value):
        if key not in self._group:
            self._group[key] = [value]
        else:
            self._group[key].append(value)

        self._indexes.append(key)
        self._lenght += 1

    def __getitem__(self, key):
        if hasattr(key, "nombre"):
            if key.nombre in self._group:
                return self._group[key.nombre][self._group[key.nombre].index(key)]

        elif type(key) is int:
            if 0 <= key <= self._lenght:
                name = self._indexes[key]
                idx = key - self._indexes.index(name)
                return self._group[name][idx]
            else:
                raise IndexError
        else:
            raise KeyError

    def __delitem__(self, key):
        
        if type(key) is int:
            if 0 <= key <= self._lenght:
                del self._indexes[key]
                del self[key]

        elif hasattr(key, "nombre"):
            if key.nombre in self._group:
                if len(self._group[key.nombre]) > 1:
                    del self._group[key.nombre][self._group[key.nombre].index(key)]
                else:
                    del self._group[key.nombre]
            self._indexes.remove(key.nombre)

        else:
            raise KeyError

    def __contains__(self, item):
        if type(item) is str:
            if item in self._group:
                return True
        elif hasattr(item, 'nombre'):
            if item.nombre in self._group:
                return True
        else:
            return False

    def __len__(self):
        return self._lenght

    def delete_item(self, event):
        obj = event.data['obj']
        del self[obj]

    def contents(self):
        return [self._group[key][0] for key in self._group]

MobGroup = MobGroup()
ItemGroup = ItemGroup()

__all__ = ["MobGroup", "ItemGroup"]

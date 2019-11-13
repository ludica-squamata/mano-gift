from .event_dispatcher import EventDispatcher


class MobGroup:
    """this is a dict that can be accessed by index"""

    _group = {}
    _indexes = []

    def __init__(self):
        self._group = {}
        self._indexes = []

        EventDispatcher.register(self.delete_mob, 'MobDeath')

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

    def clear(self):
        self._group.clear()
        self._indexes.clear()

    def get_controlled_mob(self):
        # creo que esto se podría hacer con un oneliner
        for mob_name in self._group:
            mob = self._group[mob_name]
            if mob.AI_type == 'Controllable':
                return mob


class ItemGroup:
    _group = {}
    _indexes = []
    _lenght = 0

    def __init__(self):
        self._group = {}
        self._indexes = []
        self._layers = {}
        self._lenght = 0

        EventDispatcher.register(self.delete_item, 'DeleteItem')

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
                raise IndexError()

        elif type(key) == str:
            if key in self._group:
                return self._group[key][0]

        else:
            raise TypeError()

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
            raise TypeError()

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

    def __add__(self, other):
        new = ItemGroup()
        for item in self:
            new[item.nombre] = item
        for item in other:
            new[item.nombre] = item

        return new

    def add(self, key, value, layer=0):
        if layer in self._layers:
            self._layers[layer].append(value)
        else:
            self._layers[layer] = [value]
        self.__setitem__(key, value)

    def get_from_layer(self, layer):
        if layer in self._layers:
            return self._layers[layer]
        else:
            return []

    def clear_layer(self, layer):
        self._layers[layer].clear()

    def delete_item(self, event):
        obj = event.data['obj']
        del self[obj]

    def contents(self):
        return [self._group[key][0] for key in self._group]


class DeletedItems(ItemGroup):
    def delete_item(self, event):
        obj = event.data['obj']
        self[obj.nombre] = obj


Mob_Group = MobGroup()
Item_Group = ItemGroup()
Deleted_Items = DeletedItems()

__all__ = ["Mob_Group", "Item_Group", "Deleted_Items"]

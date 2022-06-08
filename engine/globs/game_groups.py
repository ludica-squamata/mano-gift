from .event_dispatcher import EventDispatcher


class MobGroup:
    """this is a dict that can be accessed by index"""

    _group = {}
    _indexes = []
    _name = ''

    def __init__(self):
        self._group = {}
        self._indexes = []

        EventDispatcher.register_many(
            (self.delete_mob, 'MobDeath'),
            (self.register_name, "CharacterCreation", 'LoadGame')
        )

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
            return self.__missing__(key)

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
        elif hasattr(item, 'id'):
            if item.id in self._group:
                return True
        return False

    def __missing__(self, key):
        return key

    def get_existing(self, mobs):
        flagged = []
        for mob in mobs:
            if mob in self:
                flagged.append(mob)
        return flagged

    def delete_mob(self, event):
        del self[event.data['obj'].id]

    def __str__(self):
        return 'MobGroup keys (' + ','.join([self._group[i].nombre for i in self._indexes]) + ')'

    def contents(self):
        return [self._group[key] for key in self._group]

    def clear(self):
        self._group.clear()
        self._indexes.clear()

    def get_controlled_mob(self):
        # creo que esto se podría hacer con un oneliner
        for mob_id in self._group:
            mob = self._group[mob_id]
            if mob.AI_type == 'Controllable':
                return mob

    # Aunque estos tres métodos singularizan al héroe
    # no se me ocurre otra forma de arrastrar su nombre.
    def register_name(self, event):
        # posiblemente esto se puede hacer en menos líneas.
        if 'nombre' in event.data:
            self._name = event.data['nombre']
        elif 'focus' in event.data:
            self._name = event.data['focus']

    @property
    def character_name(self):
        return self._name

    @character_name.deleter
    def character_name(self):
        self._name = ''


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


class LightGroup:
    _lights = None
    """A group for lights that belong to a certain map"""

    def __init__(self):
        self._lights = {}

    def add(self, map_id, light):
        if map_id not in self._lights:
            self._lights[map_id] = []
        if light not in self._lights[map_id]:
            self._lights[map_id].append(light)

    def remove(self, light):
        for map_id in self._lights:
            if light in self._lights[map_id]:
                self._lights[map_id].remove(light)

    def list(self, map_id):
        if map_id in self._lights:
            return self._lights[map_id]
        else:
            return []


Mob_Group = MobGroup()
Item_Group = ItemGroup()
Deleted_Items = DeletedItems()
Light_Group = LightGroup()

__all__ = ["Mob_Group", "Item_Group", "Deleted_Items", "Light_Group"]

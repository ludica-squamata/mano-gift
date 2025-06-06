from .event_dispatcher import EventDispatcher


class MobGroup:
    """this is a dict that can be accessed by index"""

    _group = {}
    _indexes = []
    _name = ''

    def __init__(self):
        self._group = {}
        self._indexes = []

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
            return None

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
        for key in self._indexes:
            mob = self[key]
            mob.unload()
            mob.AI.unload()
            mob.parent.del_property(mob)
            mob.parent.parent.del_property(mob)
        self._group.clear()
        self._indexes.clear()

    def get_controlled_mob(self):
        # now it is just a shortcut.
        return self.get_by_trait('AI', 'controllable')

    def get_by_trait(self, key, value):
        """Return a sorted (by name) list of mobs that have the desired trait for the purposes of iteration."""

        listed = [mob for mob in self.contents() if mob[key] == value]
        listed.sort(key=lambda o: o['nombre'])
        if len(listed) == 1:
            return listed[0]
        elif len(listed):
            return listed


class ItemGroup:
    _group = {}
    _indexes = []
    _lenght = 0

    def __init__(self, name):
        self._group = {}
        self._indexes = []
        self._layers = {}
        self._lenght = 0
        self.name = name

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

        elif type(key) is str:
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
                    item = [i for i in self._group[key.nombre] if i.id == key.id]
                    if len(item):
                        item = item[0]
                        idx = self._group[key.nombre].index(item)
                        del self._group[key.nombre][idx]
                        self._indexes.remove(key.nombre)
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
        new = ItemGroup('combined')
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
        if event.origin == self.name:
            obj = event.data['obj']
            del self[obj]

    def contents(self):
        return [self._group[key][0] for key in self._group]

    def __repr__(self):
        return f'ItemGroup {self.name}'

    def clear(self):
        for key in self._indexes:
            items = self._group[key]
            for item in items:
                item.parent.del_property(item)
                item.parent.parent.del_property(item)
        self._indexes.clear()
        self._group.clear()
        self._lenght = 0


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


class TaggedGroup:
    """Es un diccionario cuyas keys son características de los props/mobs que lo componen. Un prop o mob puede
    pertenecer a más de una key, pero no pueden aparecer más de una vez bajo una key dada.

    Esto permite obtener props o mobs por caracterísicas como "solido" o "agresivo" sin tener que generar nuevas listas
    en el mapa o entradas en Constantes.
    """

    def __init__(self):
        self._inner_dict = {}

    def add(self, key: str, item):
        """Añade un item a la key provista. Si la key no existiere, se crea una nueva con ese item."""

        if key in self._inner_dict:
            self._inner_dict[key].append(item)
        elif key not in self._inner_dict:
            self._inner_dict[key] = [item]

    def add_item(self, item, *keys):
        """Añade un item a todas las keys provistas."""

        for key in keys:
            self.add(key, item)

    def get(self, key: str):
        """Devuelve los items de una key o un error si la key no existe."""

        if key in self._inner_dict:
            return self._inner_dict[key]
        else:
            raise KeyError(f"key '{key}' is invalid")

    def intersect(self, key1, key2):
        """Devuelve los items que pertenezcan simultáneamente a key1 y key2"""

        items = set(self._inner_dict.get(key1, []) + self._inner_dict.get(key2, []))
        return list(items)

    def create_key(self, key):
        """Crea una lista nueva bajo key si la key no está ya presente"""

        if key not in self._inner_dict:
            self._inner_dict[key] = []

    def remove_item(self, item):
        """Remueve el item de todas las keys del grupo"""

        for key in self._inner_dict:
            if item in self._inner_dict[key]:
                idx = self._inner_dict[key].index(item)
                del self._inner_dict[key][idx]

    def remove_key(self, key: str):
        """Remueve keys. Items pertenecientes a otras keys no se ven afectados."""

        if key in self._inner_dict:
            del self._inner_dict[key]
        else:
            raise KeyError(f"key '{key}' is invalid")


class ParentedTaggedGroup(TaggedGroup):
    """Funciona igual que TaggedGroup, pero tinene una referencia a su parent."""

    def __init__(self, parent):
        self.parent = parent
        super().__init__()


Mob_Group = MobGroup()
Item_Group = ItemGroup('Item')
Prop_Group = ItemGroup('Prop')
Deleted_Items = DeletedItems('Deleted')
Light_Group = LightGroup()
Tagged_Items = TaggedGroup()

__all__ = ["Mob_Group", "Item_Group", "Prop_Group", "Deleted_Items", "Light_Group", "Tagged_Items"]

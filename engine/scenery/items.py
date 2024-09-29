from engine.globs.event_dispatcher import EventDispatcher
from .bases import Item


class Equipable(Item):
    def __init__(self, parent, nombre, data):
        super().__init__(parent, nombre, data)
        self.tipo = 'equipable'
        self.subtipo = data['subtipo']
        self.espacio = data['efecto']['equipo']


class Consumible(Item):
    def __init__(self, parent, nombre, data):
        super().__init__(parent, nombre, data)
        self.tipo = 'consumible'
        self.data = data

    def usar(self, mob):
        stat = self.data.get('efecto', {}).get('stat', '')
        mod = self.data.get('efecto', {}).get('mod', '')
        method = self.data.get('efecto', {}).get('method', '')
        valor = 0

        if method == 'percentage':
            valmaximo = mob[stat + 'Max']
            valactual = mob[stat]
            valor = int((mod * valmaximo) / 100)
            if valor + valactual > valmaximo:
                valor = valmaximo
            else:
                valor += valactual

            mob[stat] = valor

        elif method == 'incremental':
            actual = mob[stat]
            valor = actual + mod
            mob[stat] = valor

        m, s, v, f, h = 'mob', 'stat', 'value', 'factor', 'method'
        EventDispatcher.trigger('UsedItem', self.nombre, {m: mob, s: stat, v: valor, f: mod, h: method})
        return mob.inventario.remover(self)


class Colocable(Item):
    def __init__(self, parent, entity, nombre, data, item):
        super().__init__(parent, nombre, data)
        self.tipo = 'colocable'
        self.entity = entity
        self.item = item

    def action(self):
        from .new_prop import new_prop
        x, y, z = self._get_placement_position()
        prop = new_prop(self.parent, x, y, z, self.nombre, self.data)
        self.entity.inventario.remover(self.item)
        self.entity.parent.parent.place_placeable_props(prop)
        return prop

    def _get_placement_position(self):
        """Establece las coordinadas donde aparecerá el prop relativas al mob que lo colocó.

        Aún no funciona completamente bien."""

        x, y, z = 0, 0, 0
        w, h = self.rect.size
        if self.entity.body_direction == 'abajo':
            x = self.entity.rel_x
            y = self.entity.rel_y + h // 2
            z = self.entity.rect.bottom + h // 2
        elif self.entity.body_direction == 'arriba':
            x = self.entity.rel_x
            y = self.entity.rel_y - h // 2
            z = self.entity.rect.top + h // 2
        elif self.entity.body_direction == 'izquierda':
            x = self.entity.rect.left + w // 2
            y = self.entity.rel_y
            z = self.entity.rect.centery
        elif self.entity.body_direction == 'derecha':
            x = self.entity.rel_x + w // 2
            y = self.entity.rel_y
            z = self.entity.rect.centery

        return x, y, z


class Armadura(Equipable):
    def __init__(self, parent, nombre, data):
        super().__init__(parent, nombre, data)
        self.proteccion = data['efecto']['proteccion']


class Arma(Equipable):
    def __init__(self, parent, nombre, data):
        super().__init__(parent, nombre, data)


class Accesorio(Equipable):
    def __init__(self, parent, nombre, data):
        super().__init__(parent, nombre, data)


class Pocion(Consumible):
    def __init__(self, parent, nombre, data):
        super().__init__(parent, nombre, data)

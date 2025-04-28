from engine.globs.event_dispatcher import EventDispatcher
from engine.globs import Item_Group
from .bases import Item


class Tradeable(Item):
    price_sell = 0
    price_buy = 0
    coin = None

    def __init__(self, parent, data):
        super().__init__(parent, data)
        if "trading" in data:
            self.price_sell = data['trading']['sell_price']
            self.price_buy = data['trading']['buy_price']
            self.coin = data['trading']['coin_symbol']


class Equipable(Tradeable):
    def __init__(self, parent, data):
        super().__init__(parent, data)
        self.tipo = 'equipable'
        self.subtipo = data['subtipo']
        self.espacio = data['efecto']['equipo']
        Item_Group.add(self.nombre, self, self.tipo)


class Consumible(Tradeable):
    def __init__(self, parent, data):
        super().__init__(parent, data)
        self.tipo = 'consumible'
        self.data = data
        Item_Group.add(self.nombre, self, self.tipo)

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
        EventDispatcher.trigger('PlaySound', self, {'sound': 'powerup'})
        return mob.inventario.remover(self)


class Utilizable(Tradeable):
    def __init__(self, parent, data):
        super().__init__(parent, data)
        self.tipo = "utilizable"
        self.subtipo = "libro"
        Item_Group.add(self.nombre, self, self.tipo)


class Colocable(Item):
    def __init__(self, parent, entity, data, item):
        super().__init__(parent, data)
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
    def __init__(self, parent, data):
        super().__init__(parent, data)
        self.proteccion = data['efecto']['proteccion']


class Arma(Equipable):
    def __init__(self, parent, data):
        super().__init__(parent, data)


class Accesorio(Equipable):
    def __init__(self, parent, data):
        super().__init__(parent, data)


class Pocion(Consumible):
    def __init__(self, parent, data):
        super().__init__(parent, data)

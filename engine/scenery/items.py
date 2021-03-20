from engine.globs.event_dispatcher import EventDispatcher
from .bases import Item


class Equipable(Item):
    def __init__(self, nombre, imagen, data):
        super().__init__(nombre, imagen, data)
        self.tipo = 'equipable'
        self.subtipo = data['subtipo']
        self.espacio = data['efecto']['equipo']


class Consumible(Item):
    def __init__(self, nombre, imagen, data):
        super().__init__(nombre, imagen, data)
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

        if method == 'incremental':
            actual = mob[stat]
            valor = actual + mod
            mob[stat] = valor

        m, s, v, f, h = 'mob', 'stat', 'value', 'factor', 'method'
        EventDispatcher.trigger('UsedItem', self.nombre, {m: mob, s: stat, v: valor, f: mod, h: method})
        return mob.inventario.remover(self)


class Colocable(Item):
    def __init__(self, nombre, imagen, data):
        super().__init__(nombre, imagen, data)
        self.subtipo = 'colocable'


class Armadura(Equipable):
    def __init__(self, nombre, imagen, data):
        super().__init__(nombre, imagen, data)
        self.proteccion = data['efecto']['proteccion']


class Arma(Equipable):
    def __init__(self, nombre, imagen, data):
        super().__init__(nombre, imagen, data)


class Accesorio(Equipable):
    def __init__(self, nombre, imagen, data):
        super().__init__(nombre, imagen, data)


class Pocion(Consumible):
    def __init__(self, nombre, imagen, data):
        super().__init__(nombre, imagen, data)

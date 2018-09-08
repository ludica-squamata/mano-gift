from .bases import Item


class Equipable(Item):
    def __init__(self, nombre, imagen, data):
        super().__init__(nombre, imagen, data)
        self.tipo = 'equipable'
        self.espacio = data['efecto']['equipo']


class Consumible(Item):
    def __init__(self, nombre, imagen, data):
        super().__init__(nombre, imagen, data)
        self.tipo = 'consumible'
        self.data = data

    def usar(self, mob):
        stat = self.data.get('efecto', {}).get('stat', '')
        mod = self.data.get('efecto', {}).get('mod', '')

        if stat == 'salud':
            actual = stat + '_act'
            maximo = stat + '_max'
            valactual = getattr(mob, actual)
            valmaximo = getattr(mob, maximo)

            valor = int((mod * valmaximo) / 100)
            if valor + valactual > valmaximo:
                valor = valmaximo
            else:
                valor += valactual

            setattr(mob, actual, valor)

        elif hasattr(mob, stat):
            actual = getattr(mob, stat)
            valor = actual + mod
            setattr(mob, stat, valor)

        return mob.inventario.remover(self)


class Colocable(Item):
    def __init__(self, nombre, imagen, data):
        super().__init__(nombre, imagen, data)
        self.subtipo = 'colocable'


class Armadura(Equipable):
    def __init__(self, nombre, imagen, data):
        super().__init__(nombre, imagen, data)
        self.subtipo = 'armadura'


class Arma(Equipable):
    def __init__(self, nombre, imagen, data):
        super().__init__(nombre, imagen, data)
        self.subtipo = 'arma'


class Accesorio(Equipable):
    def __init__(self, nombre, imagen, data):
        super().__init__(nombre, imagen, data)
        self.subtipo = 'accesorio'


class Pocion(Consumible):
    def __init__(self, nombre, imagen, data):
        super().__init__(nombre, imagen, data)
        self.subtipo = 'pocion'

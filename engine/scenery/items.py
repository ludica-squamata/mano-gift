class Item:
    stackable = False
    tipo = ''

    def __init__(self, nombre, imagen, data):
        self.nombre = nombre
        self.image = imagen
        self.ID = data['ID']
        self.peso = data['peso']
        self.volumen = data['volumen']
        self.efecto_des = data['efecto']['des']
        if 'stackable' in data['propiedades']:
            self.stackable = True

    def __eq__(self, other):
        if other.__class__ == self.__class__ and self.ID == other.ID:
            return True
        else:
            return False

    def __ne__(self, other):
        if other.__class__ != self.__class__:
            return True
        elif self.ID != other.ID:
            return True
        else:
            return False

    def __repr__(self):
        return self.nombre + ' (' + self.tipo + ')'


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
            valor_actual = getattr(mob, actual)
            valor_maximo = getattr(mob, maximo)

            valor = int((mod * valor_maximo) / 100)
            if valor + valor_actual > valor_maximo:
                valor = valor_maximo
            else:
                valor += valor_actual

            setattr(mob, actual, valor)

        else:
            actual = getattr(mob, stat)
            valor = actual + mod
            setattr(mob, stat, valor)

        return True


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

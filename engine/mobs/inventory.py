class Inventory:
    def __init__(self, maxvol, maxpeso):
        self._volumen_max = maxvol
        self._peso_max = maxpeso
        self._volumen_actual = 0
        self._peso_actual = 0
        self._contenido = []
        self._by_type = {'consumible': [], 'equipable': []}

    def __contains__(self, item):
        if type(item) == str:
            # item es el nombre de un item
            for _item in self._contenido:
                if _item.nombre == item:
                    return True
            return False

        elif type(item) == int:
            # item es el ID de un item
            for _item in self._contenido:
                if _item.ID == item:
                    return True
            return False

        else:
            return item in self._contenido

    def __getitem__(self, item):
        # no entiendo porqué escribí así este método.
        if type(item) is str:
            for _item in self._contenido:
                if _item.nombre == item:
                    item = self._contenido.index(_item)
                    break

        elif type(item) is not int:
            raise TypeError()

        if 0 <= item <= len(self._contenido):
            return self._contenido[item]
        else:
            raise IndexError()

    def get_equipables(self, espacio):
        # estos "vistos", creo, se podrían suprimir con sets.
        subtotales, visto = [], []
        for item in self._by_type['equipable']:
            if item.espacio == espacio:
                if item.nombre not in visto:
                    visto.append(item.nombre)
                    subtotales.append(item)
        return subtotales

    def get_by_type(self, tipo):
        subtotales, visto = [], []
        for item in self._by_type[tipo]:
            if item.nombre not in visto:
                visto.append(item.nombre)
                subtotales.append(item)
        return subtotales

    def __len__(self):
        return len(self._contenido)

    def cantidad(self, item):
        return self._contenido.count(item)

    def actualizar_maximos(self, nuevopesomax, nuevovolmax):
        self._volumen_max = nuevovolmax
        self._peso_max = nuevopesomax

    def agregar(self, item):
        assert self._volumen_actual + item.volumen <= self._volumen_max, 'El item es demasiado grande'
        assert self._peso_actual + item.peso <= self._peso_max, 'No puedes cargar más peso del que llevas.'
        self._peso_actual += item.peso
        self._volumen_actual += item.volumen
        self._contenido.append(item)
        self._by_type[item.tipo].append(item)

    def remover(self, item):
        if item in self._contenido:
            self._peso_actual -= item.peso
            self._volumen_actual -= item.volumen
            self._contenido.remove(item)
            self._by_type[item.tipo].remove(item)
            return self._contenido.count(item)
        else:
            return 0

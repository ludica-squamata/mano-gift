class InventoryError(Exception):
    def __init__(self, message = None):
        self.message = message

    def __str__(self):
        return self.message


class Inventory:
    __slots__ = ['_volumen_max', '_volumen_actual',
                 '_peso_max', '_peso_actual', '_contenido']

    def __init__(self, maxvol, maxpeso):
        self._volumen_max = maxvol
        self._peso_max = maxpeso
        self._volumen_actual = 0
        self._peso_actual = 0
        self._contenido = []

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

    def __getitem__(self, item):
        if type(item) != int:
            raise TypeError()
        elif item < 0:
            item += len(self._contenido)

        if item > len(self._contenido) - 1:
            raise IndexError()
        else:
            return self._contenido[item]

    def __call__(self, tipo = None, espacio = None):
        subtotales, visto = [], []
        if tipo is None:
            for item in self._contenido:
                if item.nombre not in visto:
                    visto.append(item.nombre)
                    subtotales.append(item)

        elif espacio is None:
            for item in self._contenido:
                if item.tipo == tipo:
                    if item.nombre not in visto:
                        visto.append(item.nombre)
                        subtotales.append(item)

        else:
            for item in self._contenido:
                if item.tipo == tipo:
                    if item.espacio == espacio:
                        if item.nombre not in visto:
                            visto.append(item.nombre)
                            subtotales.append(item)

        return subtotales

    def __len__(self):
        return len(self._contenido)

    def peso_actual(self):
        return self._peso_actual

    def volumen_actual(self):
        return self._volumen_actual

    def cantidad(self, item):
        return self._contenido.count(item)

    def actualizar_maximos(self, nuevoPesoMax, nuevoVolMax):
        self._volumen_max = nuevoVolMax
        self._peso_max = nuevoPesoMax

    def agregar(self, item):
        if self._volumen_actual + item.volumen <= self._volumen_max:
            if self._peso_actual + item.peso <= self._peso_max:
                self._peso_actual += item.peso
                self._volumen_actual += item.volumen
                self._contenido.append(item)
            else:
                raise InventoryError('No puedes cargar más peso del que llevas.')
        else:
            raise InventoryError('El item es demasiado grande')

    def remover(self, item):
        if item in self._contenido:
            self._peso_actual -= item.peso
            self._volumen_actual -= item.volumen
            self._contenido.remove(item)
            return self._contenido.count(item)
        else:
            raise InventoryError('El item no existe')

from engine.globs.eventDispatcher import EventDispatcher
from re import compile


class Elemento:
    """Class for the dialog tree elements."""

    nombre = ''
    hasLeads = False
    tipo = ''
    indice = None
    locutor = None  # el que habla
    inter = None  # a quien le habla
    leads = None
    reqs = None
    event_data = None
    tags = None
    texto = ''

    def __init__(self, indice, data):
        self.leads = None
        self.indice = indice

        self.tipo = data['type']
        self.nombre = self.tipo.capitalize() + ' #' + str(self.indice)
        self.texto = data['txt']
        self.locutor = data['from']
        self.inter = data['to']
        self.leads = data.get('leads', None)
        self.reqs = data.get('reqs', None)
        self.event_data = data.get('event_data', None)

        if type(self.leads) is list:
            self.hasLeads = True

        self.tags = []
        self.expressions = []
        tags = compile(r'<([a-z]*?)>([^<]*)</\1>').findall(self.texto)
        if self.texto.count('<') == len(tags) * 2:
            for tag in tags:
                self.tags.append(tag[0])
                self.expressions.append(tag[1])
        else:
            # si es que son ilógicos...
            raise TypeError('Verificar las tags. No se permiten tags anidadas y los grupos deben estar cerrados')

        del data

    def post_event(self):
        EventDispatcher.trigger('DialogEvent', self, self.event_data)

    def __repr__(self):
        return self.nombre

    def __int__(self):
        return int(self.indice)

    def __str__(self):
        return self.nombre

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        elif self.indice != other.indice:
            return False
        else:
            return True

    def __ne__(self, other):
        if type(self) == type(other):
            return False
        elif self.indice == other.indice:
            return False
        else:
            return True


class BranchArray:
    _lenght = 0
    is_exclusive = False
    locutor = None
    array = []
    flaged = []

    def __init__(self, node, elementos):
        self.array = []
        for idx in node.leads:
            self.array.append(elementos[idx])
        if node.tipo == 'exclusive':
            self.is_exclusive = True

        self.locutor = self.array[0].locutor

    def __getitem__(self, item):
        if type(item) != int:
            raise TypeError('expected int, got' + str(type(item)))
        else:
            return self.array[item]

    def __len__(self):
        return self._lenght

    def __repr__(self):
        ex = 'Exclusive '
        if not self.is_exclusive:
            ex.lower()
            ex = 'Non ' + ex

        return ex + 'BranchArray (' + ', '.join(['#' + str(i.indice) for i in self.array]) + ')'

    def add(self, x):
        self.array.append(x)
        self._lenght += 1

    def supress(self, nodo):
        if nodo in self.array:
            self.flaged.append(self.array.index(nodo))

    def show(self):
        to_show = []
        for i in range(len(self.array)):
            if i not in self.flaged:
                to_show.append(self.array[i])
        self.flaged.clear()
        return to_show


class ArboldeDialogo:
    __slots__ = ['_elementos', '_future']

    def __init__(self, datos):
        self._elementos = []
        self._future = 0

        self._elementos.extend(self._crear_lista(datos))

        for obj in self._elementos:
            if obj.tipo != 'leaf':
                if not obj.hasLeads:
                    obj.leads = self._elementos[obj.leads]
                else:
                    obj.leads = BranchArray(obj, self._elementos)

    @staticmethod
    def _crear_lista(datos):
        _elem = []
        for i in range(len(datos)):
            idx = str(i)
            data = datos[idx]

            _elem.append(Elemento(idx, data))
        return _elem

    def __len__(self):
        return len(self._elementos)

    def __repr__(self):
        return '_Arbol de Dialogo (' + str(len(self._elementos)) + ' elementos)'

    def __getitem__(self, item):
        if type(item) != int:
            raise TypeError('expected int, got' + str(type(item)))
        elif not 0 <= item <= len(self._elementos) - 1:
            raise IndexError
        else:
            return self._elementos[item]

    def __contains__(self, item):
        if item in self._elementos:
            return True
        return False

    def get_lead_of(self, parent_i, lead_i=0):
        if type(parent_i) is Elemento:
            parent_i = self._elementos.index(parent_i)
        item = self._elementos[parent_i]
        if item.tipo != 'leaf':
            if item.hasLeads:
                return item.leads[lead_i]
            else:
                return item.leads
        else:
            raise TypeError('Leaf element has no lead')

    def set_actual(self, idx):
        if isinstance(idx, Elemento):
            idx = self._elementos.index(idx)
        if 0 <= idx <= len(self._elementos) - 1:
            self._future = idx
        else:
            raise IndexError

    def get_actual(self):
        if type(self._future) is BranchArray:
            return self._future
        else:
            return self._elementos[self._future]

    @staticmethod
    def next(nodo):
        return nodo.leads

    def set_chosen(self, choice):
        self.set_actual(int(choice))

    def update(self):
        """Devuelve el nodo actual, salvo que sea un leaf o branch,
        en cuyo caso devuelve False y None (respectivamente), y
        prepara se prepara para devolver el siguiente nodo"""

        if self._future is not False:  # last was leaf; close
            if not type(self._future) is BranchArray:
                actual = self.get_actual()  # node or leaf
                if actual.tipo != 'leaf':
                    if not type(actual.leads) is BranchArray:
                        self._future = int(actual.leads.indice)
                    else:
                        self._future = actual.leads
                else:
                    self._future = False

                return actual

            else:  # branch
                return self._future

        else:  # last was leaf; close
            return self._future

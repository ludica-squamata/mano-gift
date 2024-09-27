from engine.globs.event_dispatcher import EventDispatcher
from re import compile


class Elemento:
    """Class for the dialog tree elements."""

    nombre = ''
    hasLeads = False
    tipo = ''
    indice = None
    emisor = None  # el que habla
    receptor = None  # a quien le habla
    leads = None
    reqs = None
    event = None
    tags = None
    texto = ''

    item = None

    def __init__(self, parent, indice, data):
        self.parent = parent
        self.leads = None
        self.indice = indice

        self.tipo = data['type']
        self.nombre = self.tipo.capitalize() + ' #' + str(self.indice)
        self.texto = data['txt']
        self.emisor = data['from']
        self.receptor = data['to']
        self.leads = data.get('leads', None)
        self.reqs = data.get('reqs', None)
        self.event = data.get('event', None)
        self.pre = data.get('pre', 0)
        self.item = data.get('item', None)  # the filename.

        if type(self.leads) is list:
            self.hasLeads = True

        self.tags = []
        self.expressions = []
        self.tagged_expressions = {}
        tags = compile(r'<([a-z]*?)>([^<]*)</\1>').findall(self.texto)
        if self.texto.count('<') == len(tags) * 2:
            for tag in tags:
                self.tags.append(tag[0])
                self.expressions.append(tag[1])
                self.tagged_expressions[tag[0]] = tag[1]
        else:
            # si es que son ilógicos...
            raise TypeError('Verificar las tags. No se permiten tags anidadas y los grupos deben estar cerrados')

        del data

    def create_event(self, name, data):
        self.event = name, self, data

    def post_event(self):
        EventDispatcher.trigger(*self.event)

    def remove_tagged_expression(self, tag_name):
        expression = self.tagged_expressions[tag_name]
        if expression in self.expressions:
            self.expressions.remove(expression)

    def restore_tagged_expression(self, tag_name):
        expression = self.tagged_expressions[tag_name]
        if expression not in self.expressions:
            self.expressions.append(expression)

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

    def __next__(self):
        return self.leads


class BranchArray:
    _lenght = 0
    is_exclusive = False
    emisor = None
    array = []
    flaged = []
    item = None

    def __init__(self, parent, node, elementos):
        self.parent = parent
        self.array = []
        for idx in node.leads:
            self.array.append(elementos[idx])
        if node.tipo == 'exclusive':
            self.is_exclusive = True

        self.emisor = self.array[0].emisor
        self.item = self.array[0].item

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
    _future = 0

    def __init__(self, parent, datos):
        self.parent = parent
        self._elementos = [Elemento(self, idx, data) for idx, data in datos.items()]

        for obj in self._elementos:
            if obj.tipo != 'leaf':
                if not obj.hasLeads:
                    obj.leads = self._elementos[obj.leads]
                else:
                    obj.leads = BranchArray(self, obj, self._elementos)

    def __getitem__(self, item):
        if type(item) is Elemento:
            if item in self._elementos:
                return item
        elif type(item) is int:
            if 0 <= item <= len(self._elementos):
                return self._elementos[item]
        else:
            raise TypeError("type(item) must be Elemento or int")

    def __setitem__(self, key, value):
        element = None
        if type(key) is int:
            if 0 <= key <= len(self._elementos):
                element = self._elementos[key]
        elif type(key) is Elemento:
            element = key
        else:
            raise TypeError("type(item) must be Elemento or int")

        element.texto = value

    def process_events(self, events):
        for elemento in self._elementos:
            if elemento.event is not None:
                name = elemento.event
                if "mob" in events[name]:
                    # acá procesamos la keyword.
                    if events[name]['mob'] == '<locutor>':
                        # Locutor es el que habla
                        mob = elemento.emisor
                    elif events[name]['mob'] == '<interlocutor>':
                        # Interlocutor es el que escucha.
                        mob = elemento.receptor
                    else:
                        # Si la key no es una keyword asumimos que es el nombre.
                        mob = events[name]['mob']
                    # y reasignamos ese nombre.
                    events[name]['mob'] = mob
                elemento.create_event(name, events[name])

    def __repr__(self):
        return '_Arbol de Dialogo (' + str(len(self._elementos)) + ' elementos)'

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

    def set_chosen(self, choice):
        if choice is None:
            # choice is a leaf
            self._future = False
        else:
            self.set_actual(int(choice))

    def update(self):
        """Devuelve el nodo actual, y se prepara para devolver el siguiente nodo."""

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

        return self._future  # branch or close.

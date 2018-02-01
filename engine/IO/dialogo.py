from engine.globs import EngineData, CAPA_OVERLAYS_DIALOGOS, ModState
from engine.globs.eventDispatcher import EventDispatcher
from engine.globs.event_aware import EventAware
from engine.UI import DialogInterface
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


class Dialogo(EventAware):
    SelMode = False
    sel = 0
    next = 0

    def __init__(self, arbol, *locutores):
        super().__init__()
        self.tags_condicionales = arbol['head']['conditional_tags']
        self.name = arbol['head']['name']

        self.dialogo = ArboldeDialogo(arbol['body'])
        self.locutores = {}
        for loc in locutores:
            self.locutores[loc.nombre] = loc

        self.frontend = DialogInterface(self, arbol['head']['style'])
        self.functions['tap'].update({
            'accion': self.hablar,
            'contextual': self.cerrar,
            'arriba': lambda: self.direccionar_texto('arriba'),
            'abajo': lambda: self.direccionar_texto('abajo'),
            'izquierda': self.frontend.detener_menu,
            'derecha': self.frontend.detener_menu,
        })
        self.functions['hold'].update({
            'arriba': lambda: self.direccionar_texto('arriba'),
            'abajo': lambda: self.direccionar_texto('abajo'),
            'izquierda': lambda: self.direccionar_texto('izquierda'),
            'derecha': lambda: self.direccionar_texto('derecha'),
        })
        self.functions['release'].update({
            'izquierda': self.frontend.detener_menu,
            'derecha': self.frontend.detener_menu,
        })

        self.hablar()

    @classmethod
    def pre_init(cls, meta, *locutores):
        for loc in locutores:
            if loc.nombre not in meta['locutors']:
                return False
        return True

    @staticmethod
    def supress_element(condiciones, locutor):
        supress = False

        if "attrs" in condiciones:
            for attr in condiciones['attrs']:
                loc_attr = getattr(locutor, attr)
                operador, target = condiciones['attrs'][attr]
                if operador == "<":
                    supress = not loc_attr < target
                elif operador == ">":
                    supress = not loc_attr > target
                elif operador == "=":
                    supress = not loc_attr == target
                elif operador == "<=":
                    supress = not loc_attr <= target
                elif operador == ">=":
                    supress = not loc_attr >= target
                elif operador == '!=':
                    supress = not loc_attr != target
                else:
                    raise ValueError("El operador '"+operador+"' es inválido")

        if "objects" in condiciones:
            for obj in condiciones['objects']:
                supress = supress or obj not in locutor.inventario

        return supress

    def hablar(self):

        actual = self.dialogo.update()
        if self.SelMode:
            if self.sel.event_data is not None:
                self.sel.post_event()
            self.dialogo.set_chosen(self.next)
            self.SelMode = False
            self.frontend.exit_sel_mode()
            self.hablar()

        elif type(actual) is BranchArray:
            if actual.is_exclusive:
                choices = actual.array.copy()
                default = None
                for i, choice in enumerate(choices):
                    if choice.reqs is None:
                        # nos quedamos con el que no tenga requisitos, por las dudas
                        default = choices.pop(i)

                filtered = []
                # es mejor así porque del modo anterior no se eliminan todos los nodos con rquisitos incumplidos.
                # podría hacerse con list comprehension, pero queda demasiado larga la linea.
                for choice in choices:
                    reqs = choice.reqs
                    sujeto = self.locutores[reqs['loc']]
                    # vamos eliminando todos los que tengan requisitos incumplidos
                    if not self.supress_element(reqs, sujeto):
                        filtered.append(choice)

                if len(filtered):
                    # si queda alguno con requisitos, elegir el primero.
                    # en realidad debería haber algun tipo de precedencia, pero así esta bien
                    # porque solo queda 1 elemento con requisitos.
                    choice = filtered[0]
                else:
                    # si nos quedamos sin elementos con requisitos, caemos al default.
                    choice = default

                self.dialogo.set_chosen(choice)
                self.hablar()

            else:
                loc = self.locutores[actual.locutor]

                for nodo in actual:
                    if nodo.reqs is not None:
                        if self.supress_element(nodo.reqs, loc):
                            actual.supress(nodo)

                to_show = actual.show()
                self.SelMode = True
                self.frontend.borrar_todo()
                self.frontend.set_loc_img(loc)
                self.frontend.set_sel_mode(to_show)

        elif type(actual) is Elemento:
            if actual.indice in self.tags_condicionales:
                loc = self.locutores[actual.locutor]
                supress = []
                for tag_name in self.tags_condicionales[actual.indice]:
                    condiciones = self.tags_condicionales[actual.indice][tag_name]
                    if self.supress_element(condiciones, loc):
                        supress.append(tag_name)

                self.mostrar_nodo(actual, omitir_tags=supress)
            else:
                self.mostrar_nodo(actual)

        else:
            self.cerrar()

    def mostrar_nodo(self, nodo, omitir_tags=False):
        """
        :type nodo: Elemento
        :type omitir_tags: bool
        """
        self.frontend.borrar_todo()
        loc = self.locutores[nodo.locutor]
        self.frontend.set_loc_img(loc)
        if not omitir_tags:
            self.frontend.set_text(nodo.texto)
        else:
            self.frontend.set_text(nodo.texto, omitir_tags=omitir_tags)

    def direccionar_texto(self, direccion):
        if direccion == 'arriba':
            self.frontend.scroll(+1)
        elif direccion == 'abajo':
            self.frontend.scroll(-1)
        elif self.SelMode:
            if direccion == 'izquierda':
                self.frontend.rotar_menu(-1)
            elif direccion == 'derecha':
                self.frontend.rotar_menu(+1)

    def cerrar(self):
        self.deregister()
        for loc in self.locutores:
            mob = self.locutores[loc]
            mob.hablando = False
        EngineData.end_dialog(CAPA_OVERLAYS_DIALOGOS)
        if self.SelMode:
            self.frontend.exit_sel_mode()
        del self.dialogo
        ModState.set('dialog.'+self.name,1)

    def update(self, sel):
        self.sel = sel
        if hasattr(self.sel, 'leads'):
            self.next = self.sel.leads

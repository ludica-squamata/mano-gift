from engine.UI import DialogInterface
from engine.globs.eventDispatcher import EventDispatcher
from engine.globs.event_dialogue import EventDialogue
from engine.globs import EngineData as Ed, CAPA_OVERLAYS_DIALOGOS


class Elemento:
    """Class for the dialog tree elements."""

    nombre = ''
    hasLeads = False
    tipo = ''
    indice = None
    locutor = None
    leads = None
    reqs = None
    event_data = None
    texto = ''

    def __init__(self, indice, data):
        self.leads = None
        self.indice = indice

        self.tipo = data['type']
        self.nombre = self.tipo.capitalize() + ' #' + str(self.indice)
        self.texto = data['txt']
        self.locutor = data['loc']
        self.leads = data.get('leads', None)
        self.reqs = data.get('reqs', None)
        self.event_data = data.get('event_data', None)

        if type(self.leads) is list:
            self.hasLeads = True

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


class _ArboldeDialogo:
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


class Dialogo (EventDialogue):
    SelMode = False
    sel = 0
    next = 0

    def __init__(self, arbol, *locutores):
        self.dialogo = _ArboldeDialogo(arbol)
        self.locutores = {}
        for loc in locutores:
            self.locutores[loc.nombre] = loc

        self.frontend = DialogInterface(self)

        self.func_lin = {
            'tap': {
                'accion': self.hablar,
                'contextual': self.cerrar
            },
            'hold': {
                'arriba': lambda: self.desplazar_texto('arriba'),
                'abajo': lambda: self.desplazar_texto('abajo'),
            },
        }

        self.func_sel = {
            'tap': {
                'accion': self.confirmar_seleccion,
                'contextual': self.cerrar,
                'arriba': lambda: self.desplazar_texto('arriba'),
                'abajo': lambda: self.desplazar_texto('abajo'),
                'izquierda': self.frontend.detener_menu,
                'derecha': self.frontend.detener_menu,
            },
            'hold': {
                'arriba': lambda: self.desplazar_texto('arriba'),
                'abajo': lambda: self.desplazar_texto('abajo'),
                'izquierda': lambda: self.frontend.rotar_menu(-1),
                'derecha': lambda: self.frontend.rotar_menu(+1),
            },
            'release': {
                'izquierda': self.frontend.detener_menu,
                'derecha': self.frontend.detener_menu,
            }
        }

        super().__init__()

    @classmethod
    def pre_init(cls, meta, *locutores):        
        for loc in locutores:
            if loc.nombre not in meta['locutors']:
                return False
        return True

    def use_function(self, mode, key):
        if self.SelMode:
            functions = self.func_sel
        else:
            functions = self.func_lin

        if mode in functions:
            if key in functions[mode]:
                functions[mode][key]()

    def hablar(self):

        actual = self.dialogo.update()
        if type(actual) is BranchArray:
            if actual.is_exclusive:
                choices = actual.array.copy()
                choice = -1
                for i in range(len(choices)):
                    if choices[i].reqs is not None:  # tiene precedencia
                        choice = i

                reqs = choices[choice].reqs
                sujeto = self.locutores[reqs['loc']]
                for attr in reqs['attrs']:
                    if getattr(sujeto, attr) < reqs['attrs'][attr]:
                        del choices[choice]

                choice = choices[0]
                self.dialogo.set_chosen(choice)
                self.hablar()

            else:
                loc = self.locutores[actual.locutor]

                for nodo in actual:
                    if nodo.reqs is not None:
                        if "attrs" in nodo.reqs:
                            for attr in nodo.reqs['attrs']:
                                if getattr(loc, attr) < nodo.reqs['attrs'][attr]:
                                    actual.supress(nodo)
                        elif "objects" in nodo.reqs:
                            for obj in nodo.reqs['objects']:
                                if obj not in loc.inventario:
                                    actual.supress(nodo)

                to_show = actual.show()
                self.SelMode = True
                self.frontend.borrar_todo()
                self.frontend.set_loc_img(loc)
                self.frontend.set_sel_mode(to_show)

        elif type(actual) is Elemento:
            self.mostrar_nodo(actual)

        else:
            self.cerrar()

    def confirmar_seleccion(self):
        if self.sel.event_data is not None:
            self.sel.post_event()
        self.dialogo.set_chosen(self.next)
        self.SelMode = False
        self.frontend.exit_sel_mode()
        self.hablar()

    def mostrar_nodo(self, nodo):
        """
        :type nodo: Elemento
        """
        self.frontend.borrar_todo()
        loc = self.locutores[nodo.locutor]
        self.frontend.set_loc_img(loc)
        self.frontend.set_text(nodo.texto)
        self.frontend.menu.deregister()

    def desplazar_texto(self, direccion):
        if direccion == 'arriba':
            self.frontend.scroll(+1)
        elif direccion == 'abajo':
            self.frontend.scroll(-1)

    def cerrar(self):
        self.deregister()
        for loc in self.locutores:
            mob = self.locutores[loc]
            mob.hablando = False
        Ed.end_dialog(CAPA_OVERLAYS_DIALOGOS)
        if self.SelMode:
            self.frontend.exit_sel_mode()
        del self.dialogo

    def update(self):
        self.sel = self.frontend.sel
        if hasattr(self.sel, 'leads'):
            self.next = self.sel.leads

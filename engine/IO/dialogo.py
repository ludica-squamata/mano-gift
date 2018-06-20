from engine.IO.arbol_de_dialogo import Elemento, BranchArray, ArboldeDialogo
from engine.globs import EngineData, CAPA_OVERLAYS_DIALOGOS, ModState
from engine.globs.eventDispatcher import EventDispatcher
from engine.globs.event_aware import EventAware
from engine.UI import DialogInterface


class Discurso(EventAware):
    def __init__(self):
        super().__init__()

    @classmethod
    def pre_init(cls, meta, *locutores):
        allow = True
        for loc in locutores:
            if loc.nombre not in meta['locutors']:
                allow = not allow
                break

        if ModState.get('dialog.' + meta['name']):
            allow = False

        if meta['class'] != 'chosen':
            allow = False

        return allow

    def direccionar_texto(self, direccion):
        raise NotImplementedError

    def cerrar(self):
        self.deregister()
        EngineData.end_dialog(CAPA_OVERLAYS_DIALOGOS)


class Dialogo(Discurso):
    SelMode = False
    sel = 0
    next = 0
    write_flag = True  # flags the conversation so it wouldn't be repeated

    def __init__(self, arbol, *locutores):
        super().__init__()
        EventDispatcher.register(self.set_flag, 'Flag')
        self.tags_condicionales = arbol['head']['conditional_tags']
        self.name = arbol['head']['name']

        self.dialogo = ArboldeDialogo(arbol['body'])
        self.dialogo.process_events(arbol['head']['events'])

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
        if self.SelMode and self.frontend.has_stopped():
            if self.sel.event is not None:
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

            elif self.SelMode is False:
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
            if actual.event is not None:
                actual.post_event()
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

    def cerrar(self, write_flag=True):
        for loc in self.locutores:
            mob = self.locutores[loc]
            mob.hablando = False
        if self.SelMode:
            self.frontend.exit_sel_mode()
        self.dialogo = None

        if self.write_flag:
            ModState.set('dialog.'+self.name, 1)

        super().cerrar()

    def set_flag(self, event):
        self.write_flag = event.data['value']

    def update(self, sel):
        self.sel = sel
        if hasattr(self.sel, 'leads'):
            self.next = self.sel.leads


class Monologo(Discurso):
    def __init__(self, locutor, *otros_participantes):
        super().__init__()
        self.locutor = locutor
        self.participantes = [locutor] + list(otros_participantes)
        self.frontend = DialogInterface(self)

        self.functions['tap'].update({
            'accion': self.cerrar,
            'contextual': self.cerrar,
            'arriba': lambda: self.direccionar_texto('arriba'),
            'abajo': lambda: self.direccionar_texto('abajo')})

        self.functions['hold'].update({
            'arriba': lambda: self.direccionar_texto('arriba'),
            'abajo': lambda: self.direccionar_texto('abajo')})

        self.frontend.set_loc_img(self.locutor)
        self.frontend.set_text('No tengo nada más que hablar contigo')  # hardcoded for test

    def direccionar_texto(self, direccion):
        if direccion == 'arriba':
            self.frontend.scroll(+1)
        elif direccion == 'abajo':
            self.frontend.scroll(-1)

    def cerrar(self):
        for mob in self.participantes:
            mob.hablando = False
        super().cerrar()

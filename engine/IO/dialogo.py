from engine.globs import CAPA_OVERLAYS_DIALOGOS, Game_State, ModData, Mob_Group
from engine.UI import DialogInterface, DialogObjectsPanel, DialogThemesPanel
from engine.IO.arbol_de_dialogo import Elemento, BranchArray, ArboldeDialogo
from engine.globs.event_dispatcher import EventDispatcher
from engine.globs.event_aware import EventAware
from engine.misc.resources import abrir_json


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

        if not Game_State.get2(f"dialog.{meta['about']}.disabled"):
            allow = False

        if meta['class'] != 'scripted':
            allow = False

        return allow

    @classmethod
    def is_possible(cls, *locutores):
        for about in ModData.dialogs_by_topic:
            ruta = ModData.dialogs_by_topic[about]
            file = cls.preprocess_locutor(abrir_json(ruta))
            file = cls.process_items(file)
            if Discurso.pre_init(file['head'], *locutores):
                return file

    @staticmethod
    def preprocess_locutor(file):
        hero_name = Mob_Group.character_name
        if 'heroe' in file['head']['locutors']:
            idx = file['head']['locutors'].index('heroe')
            file['head']['locutors'][idx] = hero_name

            for s_idx in file['body']:
                node = file['body'][s_idx]
                if node['from'] == 'heroe':
                    node['from'] = hero_name
                # elif, because the hero wouldn't be talking to himself.
                elif node['to'] == 'heroe':
                    node['to'] = hero_name

                if 'reqs' in node and 'loc' in node['reqs'] and node['reqs']['loc'] == 'heroe':
                    node['reqs']['loc'] = hero_name
        return file

    @staticmethod
    def process_items(file):
        for s_idx in file['body']:
            node = file['body'][s_idx]
            if "item" in node:
                item_name = node['item']
                node['item'] = ModData.items + item_name + '.json'

        return file

    @staticmethod
    def emit_sound_event(locutor):
        """Este método es un shortcut para el post del SoundEvent.
        Pertence a Discurso, y no a Dialogo, porque el héroe también
        escucha el Monólogo del npc."""

        EventDispatcher.trigger('SoundEvent', locutor, {'type': 'dialog', 'intensity': 60})
        # 60dB es la intensidad sonora de una conversacion normal.

        # aunque habría que ver qué pasa si el emisor susurra (20dB) y el receptor no lo puede escuchar

    def direccionar_texto(self, direccion):
        raise NotImplementedError

    def cerrar(self):
        self.deregister()
        EventDispatcher.trigger('EndDialog', self, {'layer': CAPA_OVERLAYS_DIALOGOS})


class Dialogo(Discurso):
    SelMode = False
    sel = 0
    next = 0
    write_flag = True  # flags the conversation so it wouldn't be repeated

    def __init__(self, arbol, *locutores):
        super().__init__()
        EventDispatcher.register(self.set_flag, 'Flag')
        head = arbol['head']
        self.tags_condicionales = head['conditional_tags']
        self.about = head['about']

        self.dialogo = ArboldeDialogo(arbol['body'])
        self.objects = head.get('panels', {}).get('objects', {})
        self.themes = head.get('panels', {}).get('themes', {})

        self.dialogo.process_events(head['events'])

        self.locutores = {}
        for loc in locutores:
            self.locutores[loc.nombre] = loc

        self.objects_panel = DialogObjectsPanel(self)
        self.themes_panel = DialogThemesPanel(self)
        self.frontend = DialogInterface(self, head['style'])
        self.panels = [self.frontend, self.objects_panel, self.themes_panel]
        self.panel_idx = 0

        self.functions['tap'].update({
            'accion': self.hablar_en_panel,
            'contextual': self.cerrar,
            'arriba': lambda: self.direccionar_texto('arriba'),
            'abajo': lambda: self.direccionar_texto('abajo'),
            'izquierda': lambda: self.switch_panel(-1),
            'derecha': lambda: self.switch_panel(+1),
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

    def hablar_en_panel(self):
        panel = self.panels[self.panel_idx]
        if panel is not self.frontend:
            # No hace falta crear un elif entero para discriminar entre los grupos.
            # Es cuestión de relacionar un grupo con su panel correspondiente.
            if panel is self.objects_panel:
                action = self.objects
                # "action" es un nombre provisorio, no sé realmente que nombre ponerle.
            else:
                action = self.themes

            if len(action):
                if panel.menu.actual.nombre in action:
                    # aunque aquí se está comparando por nombre, podría hacerse de manera que compare por identidad,
                    # de manera que realmente se verifique que se está mostrando ESE item en particular.

                    idx = action[panel.menu.actual.nombre]
                    # si el elemento seleccionado coincide con el nombre indicado en head,
                    # entonces el dialogo salta a ese numero de índice.
                else:
                    # de otro modo se cae al nodo indicado por default.
                    idx = action['default']

                self.dialogo.set_chosen(idx)
                # cambiamos la vista al panel de dialogo automáticamente luego de la selección,
                # porque nuestra acción fue mostrar el ítem.
                self.switch_panel(panel=self.frontend)
                # hablar() no se ejecuta si el item mostrado o tema mencionado no tienen efecto.
                # aunque todos los diálogos tendrían que tener algún nodo por default si se muestra un objeto o
                # se menciona un tema que no tiene sentido para el NPC.
                self.hablar()
        else:
            self.hablar()

    @staticmethod
    def supress_element(condiciones, locutor):
        supress = False

        if "attrs" in condiciones:
            for attr in condiciones['attrs']:
                loc_attr = locutor[attr]
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
                    raise ValueError("El operador '" + operador + "' es inválido")

        if "objects" in condiciones:
            for obj in condiciones['objects']:
                supress = supress or obj not in locutor.inventario

        if "flags" in condiciones:
            for flag in condiciones['flags']:
                supress = supress or flag not in Game_State

        return supress

    def hablar(self):
        actual = self.dialogo.update()
        if self.SelMode and self.frontend.has_stopped():
            if self.sel.event is not None:
                self.sel.post_event()
            if self.sel.item is not None:
                loc = self.locutores[self.sel.emisor]
                rec = self.locutores[self.sel.receptor]
                loc.enviar_item(self.sel.item, rec)
            self.dialogo.set_chosen(self.next)
            self.SelMode = False
            self.frontend.exit_sel_mode()
            self.emit_sound_event(self.locutores[actual.emisor])
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
                    # si queda alguno con requisitos, elegir el de mayor precedencia.
                    filtered.sort(key=lambda ch: ch.pre, reverse=True)
                    choice = filtered[0]
                else:
                    # si nos quedamos sin elementos con requisitos, caemos al default.
                    choice = default

                self.dialogo.set_chosen(choice)
                if choice.event is not None:
                    choice.post_event()

                if choice.item is not None:
                    loc = self.locutores[choice.emisor]
                    rec = self.locutores[choice.receptor]
                    loc.enviar_item(choice.item, rec)

                self.hablar()
                self.emit_sound_event(self.locutores[actual.emisor])

            elif self.SelMode is False:
                loc = self.locutores[actual.emisor]

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
                loc = self.locutores[actual.emisor]
                supress = []
                for tag_name in self.tags_condicionales[actual.indice]:
                    condiciones = self.tags_condicionales[actual.indice][tag_name]
                    if self.supress_element(condiciones, loc):
                        supress.append(tag_name)
                        actual.remove_tagged_expression(tag_name)

                self.mostrar_nodo(actual, omitir_tags=supress)

            elif actual.reqs is not None:
                if "loc" in actual.reqs:
                    # si el requisito especifica un locutor, hay que tenerlo en cuenta.
                    loc = self.locutores[actual.reqs['loc']]
                else:
                    loc = self.locutores[actual.emisor]

                if self.supress_element(actual.reqs, loc):
                    self.hablar()
                else:
                    self.mostrar_nodo(actual)

            elif actual.item is not None:
                loc = self.locutores[actual.emisor]
                rec = self.locutores[actual.receptor]
                loc.enviar_item(actual.item, rec)
                self.mostrar_nodo(actual)

            else:
                self.mostrar_nodo(actual)

            self.emit_sound_event(self.locutores[actual.emisor])

        else:
            self.cerrar()

    def mostrar_nodo(self, nodo, omitir_tags: list = False):
        """
        :type nodo: Elemento
        :type omitir_tags: bool
        """
        self.frontend.borrar_todo()
        loc = self.locutores[nodo.emisor]
        self.frontend.set_loc_img(loc)
        if not omitir_tags:
            self.frontend.set_text(nodo.texto)
        else:
            self.frontend.set_text(nodo.texto, omitir_tags=omitir_tags)

        for exp in nodo.expressions:
            Game_State.set2('tema.' + exp + '.enabled')

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
        for panel in [self.objects_panel, self.themes_panel]:
            if panel.menu is not None:
                panel.menu.salir()

        if self.write_flag:
            Game_State.set2(f'dialog.{self.about}.disabled')

        super().cerrar()

    def switch_panel(self, i=0, panel=None):
        if i != 0 and panel is None:
            self.panel_idx += i
            if self.panel_idx < -len(self.panels) + 1 or self.panel_idx > len(self.panels) - 1:
                self.panel_idx = 0

        elif panel is not None:
            self.panel_idx = self.panels.index(panel)

        for panel in self.panels:
            panel.hide()
        self.panels[self.panel_idx].show()

    def set_flag(self, event):
        self.write_flag = event.data['value']

    def update(self, sel):
        self.sel = sel
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
        self.frontend.set_text(str(self.locutor.id))  # hardcoded for test
        self.emit_sound_event(self.locutor)

    def direccionar_texto(self, direccion):
        if direccion == 'arriba':
            self.frontend.scroll(+1)
        elif direccion == 'abajo':
            self.frontend.scroll(-1)

    def cerrar(self):
        for mob in self.participantes:
            mob.hablando = False
        super().cerrar()

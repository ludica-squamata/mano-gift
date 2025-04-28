from engine.globs import CANVAS_BG, TEXT_FG, Mob_Group, ModData, EngineData
from engine.globs.event_dispatcher import EventDispatcher
from engine.libs.textrect import render_textrect
from engine.misc.resources import cargar_imagen
from engine.UI.widgets import EspacioEquipable
from engine.globs.azoe_group import AzoeGroup
from engine.IO import SoundManager
from pygame import Rect, font
from .menu import Menu


class MenuEquipo(Menu):
    espacios = None
    cur_esp = 0
    cur_itm = 0
    foco = None
    cambio = False
    draw_space_rect = None
    draw_space = None

    def __init__(self, parent, select=None):
        """Crea e inicaliza las varibales del menú Equipo."""

        super().__init__(parent, 'Equipo')
        self.entity = Mob_Group.get_controlled_mob()
        self.espacios = AzoeGroup('Espacios')  # grupo de espacios equipables.
        self.filas = AzoeGroup('Filas')  # grupo de items del espacio de selección.
        self.foco = 'espacios'  # setea el foco por default
        # Crear los espacios equipables.
        # "e_pos" es la posicion del espacio. "t_pos" es la posicion de su titulo.
        # "direcciones" indica a qué espacio se salta cuando se presiona qué tecla de dirección.
        n, e, t, k = 'nom', 'e_pos', 't_pos', 'direcciones'
        a, b, i, d = 'arriba', 'abajo', 'izquierda', 'derecha'

        # abreviaturas para legibilidad
        ye, a1, a2, cu, pe, gu, br = 'yelmo', 'aro 1', 'aro 2', 'cuello', 'peto', 'guardabrazos', 'brazales'
        fa, qu, gr, mb, mm, bo, ca = 'faldar', 'quijotes', 'grebas', 'mano buena', 'mano mala', 'botas', 'capa'
        ci, ga, r1, r2 = 'cinto', 'guantes', 'anillo 1', 'anillo 2'

        # nueva propiedad que determina qué tipo de objeto puede llenar el espacio.
        # Por ejemplo, objetos con espacio "anillo", pueden llenar tanto anillo 1 como anillo 2.
        acc = 'accepts'

        esp = [
            {n: ye, e: [96, 64], t: [93, 48], k: {i: a1, d: cu}, acc: 'yelmo'},
            {n: a1, e: [32, 64], t: [32, 48], k: {b: pe, d: ye}, acc: 'aro'},
            {n: a2, e: [224, 64], t: [224, 48], k: {b: fa, i: cu}, acc: 'aro'},
            {n: cu, e: [160, 64], t: [157, 48], k: {i: ye, d: a2}, acc: 'cuello'},
            {n: pe, e: [32, 128], t: [34, 112], k: {a: a1, b: gu, d: fa}, acc: 'peto'},
            {n: gu, e: [32, 192], t: [7, 176], k: {a: pe, b: br, d: qu}, acc: 'guardabrazos'},
            {n: br, e: [32, 256], t: [23, 240], k: {a: gu, b: ca, d: gr}, acc: 'brazales'},
            {n: fa, e: [224, 128], t: [222, 112], k: {a: a2, b: qu, i: pe}, acc: 'faldar'},
            {n: qu, e: [224, 192], t: [213, 176], k: {a: fa, b: gr, i: gu}, acc: 'quijotes'},
            {n: gr, e: [224, 256], t: [217, 240], k: {a: qu, b: ci, i: br}, acc: 'grebas'},
            {n: mb, e: [96, 352], t: [50, 320], k: {a: ca, b: r1, i: ca, d: mm}, acc: 'arma'},
            {n: mm, e: [160, 352], t: [165, 320], k: {a: ci, b: r2, i: mb, d: ci}, acc: 'escudo'},
            {n: bo, e: [224, 384], t: [223, 368], k: {a: ci, b: r2, i: r2}, acc: 'botas'},
            {n: ca, e: [32, 320], t: [32, 304], k: {a: br, b: ga, d: mb}, acc: 'capa'},
            {n: ci, e: [224, 320], t: [224, 304], k: {a: gr, b: bo, i: mm}, acc: 'cinto'},
            {n: ga, e: [32, 384], t: [22, 368], k: {a: ca, b: r1, d: r1}, acc: 'guantes'},
            {n: r1, e: [96, 416], t: [90, 400], k: {a: mb, i: ga, d: r2}, acc: 'anillo'},
            {n: r2, e: [160, 416], t: [154, 400], k: {a: mm, i: r1, d: bo}, acc: 'anillo'},
        ]

        for e in esp:
            item = self.entity.equipo[e['nom']]
            cuadro = EspacioEquipable(self, e['nom'], item, e['direcciones'], e['accepts'], *e['e_pos'])
            titulo = self.titular(e['nom'])
            self.canvas.blit(titulo, e['t_pos'])
            self.espacios.add(cuadro)

        # seleccionar un espacio por default
        if select is not None:
            espacios = [esp.index(e) for e in esp if e[acc] == select]
            self.cur_esp = espacios[0]
        else:
            self.cur_esp = 1
        selected = self.espacios.get_spr(self.cur_esp)
        selected.ser_elegido()
        self.current = selected

        # dibujar
        self.espacios.draw(self.canvas)
        self.hombre = cargar_imagen(ModData.graphs + 'hombre_mimbre.png')
        self.canvas.blit(self.hombre, (96, 96))
        w = self.canvas.get_width() - 256
        h = self.canvas.get_height() // 2
        self.create_draw_space('Inventario', 270, 40, w, h)
        self.llenar_espacio_selectivo()

        # determinar qué tecla activa qué función.
        self.functions = {
            'espacios': {
                'tap': {
                    'accion': self.cambiar_foco,
                    'contextual': self.cancelar,
                    'arriba': lambda: self.select_one('arriba'),
                    'abajo': lambda: self.select_one('abajo'),
                    'izquierda': lambda: self.select_one('izquierda'),
                    'derecha': lambda: self.select_one('derecha')
                },
                'hold': {
                    'arriba': lambda: self.select_one('arriba'),
                    'abajo': lambda: self.select_one('abajo'),
                    'izquierda': lambda: self.select_one('izquierda'),
                    'derecha': lambda: self.select_one('derecha')
                },
                'release': {
                    'accion': self.cambiar_foco,
                    'contextual': self.cancelar
                }
            },
            'items': {
                'tap': {
                    'accion': self.equipar_item,
                    'contextual': self.cancelar,
                    'arriba': lambda: self.elegir_fila('arriba'),
                    'abajo': lambda: self.elegir_fila('abajo')
                },
                'hold': {
                    'arriba': lambda: self.elegir_fila('arriba'),
                    'abajo': lambda: self.elegir_fila('abajo')
                },
                'release': {
                    'accion': self.equipar_item,
                    'contextual': self.cancelar
                }
            }
        }

    @staticmethod
    def titular(titulo):
        """Agrega un titulo descriptivo a cada espacio equipable.

        Si el nombre tiene dos partes de texto (por ejemplo 'mano buena'),
        se separa en dos lineas mediante un \\n. Si, en cambio, tras el espacio
        hay un numero (como en 'aro 1') se deja como está.

        :param titulo: string"""

        fuente = font.Font('engine/libs/Verdana.ttf', 12)
        w, h = fuente.size(titulo)
        just = 0
        if ' ' in titulo:
            titulo = titulo.split(' ')
            if not titulo[1].isnumeric():
                titulo = '\n'.join(titulo)
                h *= 2
                just = 1
            else:
                titulo = ' '.join(titulo)

        rect = Rect(-1, -1, w + 5, h + 1)
        render = render_textrect(titulo.title(), fuente, rect, TEXT_FG, CANVAS_BG, just)

        return render

    def select_one(self, direccion):
        self.canvas.fill(CANVAS_BG, [270, 290, 345, 166])
        """Desplaza la selección al espacio equipable actual, y lo resalta.
        :param direccion: string
        """

        self.deselect_all(self.espacios)
        self.draw_space.fill(CANVAS_BG)
        self.current = self.espacios.get_sprite(self.cur_esp)
        if direccion in self.current.direcciones:
            selected = self.current.direcciones[direccion]
            self.cambio = True
        else:
            selected = self.current.nombre

        for i in range(len(self.espacios)):
            espacio = self.espacios.get_sprite(i)
            if espacio.nombre == selected:
                espacio.ser_elegido()
                SoundManager.play_direct_sound('select')
                self.current = espacio
                self.cur_esp = i
                break

        self.espacios.draw(self.canvas)
        if self.current.item is not None:
            self.mostrar_caracteristicas(self.current.item)

    def elegir_fila(self, direccion=None):
        if direccion == 'arriba':
            j = -1
        elif direccion == 'abajo':
            j = +1
        else:
            j = 0

        if self.opciones > 0:
            for fila in self.filas.sprs():
                fila.ser_deselegido()
            self.posicionar_cursor(j)
            self.mover_cursor(self.filas.get_sprite(self.sel))
            self.current.ser_elegido()
            self.mostrar_caracteristicas(self.current.item)

    def llenar_espacio_selectivo(self):
        """Llena el espacio selectivo con los items que se correspondan con el espacio
        actualmente seleccionado. Esta función se llama cuando se cambia el espacio."""

        h, w = 32, self.draw_space_rect.w

        self.filas.empty()
        espacio = self.espacios.get_spr(self.cur_esp)  # por ejemplo: peto
        items = self.entity.inventario.get_equipables(espacio.accepts)
        self.fill_draw_space(items, w, h)

    def mostrar_caracteristicas(self, item):
        fuentea = font.Font('engine/libs/Verdana.ttf', 14)
        fuenteb = font.Font('engine/libs/Verdanab.ttf', 14)

        d = [
            {'nombre': 'Nombre', 'data': item.nombre, "column": 1, "row": 0},
            {'nombre': 'Peso', 'data': item.peso, "column": 1, "row": 1},
            {'nombre': 'Volumen', 'data': item.volumen, "column": 2, "row": 1},
            {'nombre': 'Descripción', 'data': item.efecto_des, "column": 1, "row": 2}
        ]
        self.canvas.fill(CANVAS_BG, [270, 290, 342, 165])  # clears the descriptive area
        for p in d:
            key = fuenteb.render(str(p['nombre']), True, TEXT_FG, CANVAS_BG)
            x = 270 if p['column'] == 1 else 370
            y = 290 + p['row'] * 22

            rect_key = key.get_rect(topleft=(x, y))

            data = fuentea.render(': ' + str(p['data']), True, TEXT_FG, CANVAS_BG)
            rect_data = data.get_rect(x=rect_key.right, y=y)
            self.canvas.blit(key, rect_key)
            self.canvas.blit(data, rect_data)

    def cambiar_foco(self):
        """Cambia el foco (las funciones que se utilizarán segun el imput)
        variando entre los espacios equipables y la lista de selección."""

        if self.current.item is None:
            if self.opciones > 0:
                self.foco = 'items'
                self.opciones = len(self.filas)
                self.elegir_fila()
        else:
            self.desequipar_espacio()

    def equipar_item(self):
        """Cuando un espacio esta seleccionado, y el foco está en la lista de items
        usar esta función traslada el item de la lista al espacio seleccionado."""

        espacio = self.espacios.get_spr(self.cur_esp)
        item = self.current.item
        if espacio.accepts == item.espacio:
            espacio.ocupar(item)
            self.entity.equipar_item(item, espacio.nombre)
            self.draw_space.fill(CANVAS_BG)
            self.espacios.draw(self.canvas)
            self.foco = 'espacios'
            self.current = espacio
            self.cambio = True

    def desequipar_espacio(self):
        espacio = self.espacios.get_spr(self.cur_esp)
        item = self.current.item
        espacio.desocupar()
        self.entity.desequipar_item(item)
        self.espacios.draw(self.canvas)
        self.cambio = True

    def cancelar(self):
        if self.foco == 'espacios':
            self.deregister()
            if len(EngineData.acceso_menues) == 1:
                EngineData.acceso_menues.clear()
                EventDispatcher.trigger('EndDialog', self, {'layer': self.layer})
            else:
                return super().cancelar()
        else:
            for fila in self.filas.sprs():
                fila.ser_deselegido()
            self.foco = 'espacios'
            self.canvas.fill(CANVAS_BG, [270, 290, 345, 166])

    def reset(self, **kwargs):
        self.deselect_all(self.espacios)
        self.cur_esp = 1
        if kwargs:
            esp = self.espacios.sprs()
            slot = kwargs['select']
            espacios = [esp.index(e) for e in esp if e.accepts == slot]
            self.cur_esp = espacios[0]

        selected = self.espacios.get_spr(self.cur_esp)
        selected.ser_elegido()
        self.current = selected
        self.llenar_espacio_selectivo()

    def use_function(self, mode, key):
        """Determina qué grupo de funciones se van a usar según el foco actual.
        :param mode: string,
        :param key: string
        """
        if mode in self.functions[self.foco]:
            if key in self.functions[self.foco][mode]:
                self.functions[self.foco][mode][key]()

    def update(self):
        if self.cambio:
            self.llenar_espacio_selectivo()
            self.cambio = False

        self.filas.update()
        self.filas.draw(self.draw_space)
        self.espacios.draw(self.canvas)
        self.canvas.blit(self.draw_space, self.draw_space_rect)

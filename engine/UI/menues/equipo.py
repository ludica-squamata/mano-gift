from engine.globs import CANVAS_BG, TEXT_FG, Mob_Group
from engine.libs.textrect import render_textrect
from engine.misc.resources import cargar_imagen
from engine.UI.widgets import EspacioEquipable
from engine.globs.azoe_group import AzoeGroup
from pygame import Rect, font
from .menu import Menu

_boton_equipo = 'Equipo'


class MenuEquipo(Menu):
    espacios = None
    cur_esp = 0
    cur_itm = 0
    foco = None
    cambio = False
    draw_space_rect = None
    draw_space = None

    def __init__(self):
        """Crea e inicaliza las varibales del menú Equipo."""

        super().__init__('Equipo')
        self.entity = Mob_Group.get_controlled_mob()
        self.espacios = AzoeGroup('Espacios')  # grupo de espacios equipables.
        self.filas = AzoeGroup('Filas')  # grupo de items del espacio de selección.
        self.foco = 'espacios'  # setea el foco por default
        # Crear los espacios equipables.
        # "e_pos" es la posicion del espacio. "t_pos" es la posicion de su titulo.
        # "direcciones" indica a qué espacio se salta cuando se presiona qué tecla de dirección.
        n, e, t, k = 'nom', 'e_pos', 't_pos', 'direcciones'
        a, b, i, d = 'arriba', 'abajo', 'izquierda', 'derecha'
        esp = [
            {n: 'yelmo', e: [96, 64], t: [93, 48], k: {i: 'aro 1', d: 'cuello'}},
            {n: 'aro 1', e: [32, 64], t: [32, 48], k: {b: 'peto', d: 'yelmo'}},
            {n: 'aro 2', e: [224, 64], t: [224, 48], k: {b: 'faldar', i: 'cuello'}},
            {n: 'cuello', e: [160, 64], t: [157, 48], k: {i: 'yelmo', d: 'aro 2'}},
            {n: 'peto', e: [32, 128], t: [34, 112], k: {a: 'aro 1', b: 'guardabrazos', d: 'faldar'}},
            {n: 'guardabrazos', e: [32, 192], t: [7, 176], k: {a: 'peto', b: 'brazales', d: 'quijotes'}},
            {n: 'brazales', e: [32, 256], t: [23, 240], k: {a: 'guardabrazos', b: 'capa', d: 'grebas'}},
            {n: 'faldar', e: [224, 128], t: [222, 112], k: {a: 'aro 2', b: 'quijotes', i: 'peto'}},
            {n: 'quijotes', e: [224, 192], t: [213, 176], k: {a: 'faldar', b: 'grebas', i: 'guardabrazos'}},
            {n: 'grebas', e: [224, 256], t: [217, 240], k: {a: 'quijotes', b: 'cinto', i: 'brazales'}},
            {n: 'mano buena', e: [96, 352], t: [50, 320], k: {a: 'capa', b: 'anillo 1', i: 'capa', d: 'mano mala'}},
            {n: 'mano mala', e: [160, 352], t: [165, 320], k: {a: 'cinto', b: 'anillo 2', i: 'mano buena', d: 'cinto'}},
            {n: 'botas', e: [224, 384], t: [223, 368], k: {a: 'cinto', b: 'anillo 2', i: 'anillo 2'}},
            {n: 'capa', e: [32, 320], t: [32, 304], k: {a: 'brazales', b: 'guantes', d: 'mano buena'}},
            {n: 'cinto', e: [224, 320], t: [224, 304], k: {a: 'grebas', b: 'botas', i: 'mano mala'}},
            {n: 'guantes', e: [32, 384], t: [22, 368], k: {a: 'capa', b: 'anillo 1', d: 'anillo 1'}},
            {n: 'anillo 1', e: [96, 416], t: [90, 400], k: {a: 'mano buena', i: 'guantes', d: 'anillo 2'}},
            {n: 'anillo 2', e: [160, 416], t: [154, 400], k: {a: 'mano mala', i: 'anillo 1', d: 'botas'}},
        ]

        for e in esp:
            item = self.entity.equipo[e['nom']]
            cuadro = EspacioEquipable(e['nom'], item, e['direcciones'], *e['e_pos'])
            titulo = self.titular(e['nom'])
            self.canvas.blit(titulo, e['t_pos'])
            self.espacios.add(cuadro)

        # seleccionar un espacio por default
        self.cur_esp = 1
        selected = self.espacios.get_sprite(self.cur_esp)
        selected.ser_elegido()
        self.current = selected

        # dibujar
        self.espacios.draw(self.canvas)
        self.hombre = cargar_imagen('hombre_mimbre.png')
        self.canvas.blit(self.hombre, (96, 96))
        w = self.canvas.get_width() - 256
        h = self.canvas.get_height() - 62
        self.create_draw_space('Inventario', w, h, 270, 40)

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
                self.current = espacio
                self.cur_esp = i
                break

        self.espacios.draw(self.canvas)

    def elegir_fila(self, direccion=None):
        if direccion == 'arriba':
            j = -1
        elif direccion == 'abajo':
            j = +1
        else:
            j = 0

        if self.opciones > 0:
            for fila in self.filas:
                fila.ser_deselegido()
            self.posicionar_cursor(j)
            self.mover_cursor(self.filas.get_sprite(self.sel))
            self.current.ser_elegido()

    def llenar_espacio_selectivo(self):
        """Llena el espacio selectivo con los items que se correspondan con el espacio
        actualmente seleccionado. Esta función se llama cuando se cambia el espacio."""

        h, w = 32, self.draw_space_rect.w

        self.filas.empty()
        espacio = self.espacios.get_sprite(self.cur_esp)  # por ejemplo: peto
        items = self.entity.inventario('equipable', espacio.nombre)
        self.fill_draw_space(items, w, h)

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

        espacio = self.espacios.get_sprite(self.cur_esp)
        item = self.current.item
        if espacio.nombre == item.espacio:
            espacio.ocupar(item)
            self.entity.equipar_item(item)
            self.draw_space.fill(CANVAS_BG)
            self.espacios.draw(self.canvas)
            self.foco = 'espacios'
            self.current = espacio
            self.cambio = True

    def desequipar_espacio(self):
        espacio = self.espacios.get_sprite(self.cur_esp)
        item = self.current.item
        espacio.desocupar()
        self.entity.desequipar_item(item)
        self.espacios.draw(self.canvas)
        self.cambio = True

    def cancelar(self):
        if self.foco == 'espacios':
            self.deregister()
            return super().cancelar()
        else:
            for fila in self.filas:
                fila.ser_deselegido()
            self.foco = 'espacios'

    def use_function(self, mode, key):
        """Determina qué grupo de funciones se van a usar según el foco actual.
        :param mode: string,
        :param key: string
        """
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

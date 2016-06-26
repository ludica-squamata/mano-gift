from pygame.sprite import LayeredUpdates, Sprite
from pygame.key import name as key_name
from pygame import Rect, font, joystick, Surface
from engine.UI.widgets import Fila
from engine.globs.constantes import TECLAS
from engine.globs.eventDispatcher import EventDispatcher
from engine.misc.config import Config as Cfg
from engine.libs.textrect import render_textrect
from .menu import Menu


class MenuOpciones(Menu):
    curr_input = ''
    input_device = 'teclado'

    def __init__(self):
        super().__init__('Opciones')
        self.data = Cfg.cargar()

        if self.data['metodo_de_entrada'] == 'teclado':
            self.curr_input = 'teclas'
        elif self.data['metodo_de_entrada'] == 'gamepad':
            self.curr_input = 'botones'

        self.botones = LayeredUpdates()
        self.espacios = LayeredUpdates()
        self.establecer_botones(self.create_config_btns(), 6)
        self.establecer_botones(self.crear_restore_btn(), 6)
        self.establecer_botones(self.create_key_btns(), 4)
        self.crear_espacios_config()
        self.notice, self.notice_area = self.create_notice()

        self.functions.update({
            'tap': {
                'accion': self.press_button,
                'arriba': lambda: self.select_one('arriba'),
                'abajo': lambda: self.select_one('abajo'),
                'izquierda': lambda: self.select_one('izquierda'),
                'derecha': lambda: self.select_one('derecha')
            },
            'hold': {
                'accion': self.mantener_presion,
                'arriba': lambda: self.select_one('arriba'),
                'abajo': lambda: self.select_one('abajo'),
                'izquierda': lambda: self.select_one('izquierda'),
                'derecha': lambda: self.select_one('derecha')
            },
            'release': {
                'accion': self.liberar_presion,
            }
        })

    def create_config_btns(self):
        m, k, p, c = 'nombre', 'direcciones', 'pos', 'comando'
        a, b, i, d = 'arriba', 'abajo', 'izquierda', 'derecha'
        cmd1 = self.cambiar_booleano
        cmd2 = self.set_input_device
        if joystick.get_count():
            botones = [
                {m: "Mostrar Intro", c: cmd1, k: {d: "Arriba", b: "Recordar Menus", a: "Defaults"}},
                {m: "Recordar Menus", c: cmd1, k: {b: "Metodo de Entrada", a: "Mostrar Intro", d: "Abajo"}},
                {m: "Metodo de Entrada", c: cmd2, k: {b: "Arriba", a: "Recordar Menus", d: "Derecha"}}
            ]
        else:
            botones = [
                {m: "Mostrar Intro", c: cmd1, k: {b: "Recordar Menus", a: "Salir", d: "Arriba"}},
                {m: "Recordar Menus", c: cmd1, k: {d: "Abajo", a: "Mostrar Intro", b: "Arriba"}}
            ]

        for i in range(len(botones)):
            botones[i][p] = [6, 38 * i + 64]

        return botones

    def create_key_btns(self):
        # abreviaturas para hacer más legible el código
        m, k = 'nombre', 'direcciones'
        a, b, i, d = 'arriba', 'abajo', 'izquierda', 'derecha'
        if joystick.get_count():
            special = "Metodo de Entrada"
        else:
            special = "Recordar Menus"
        botones = [
            {m: "Arriba", k: {b: "Abajo", a: special, i: "Mostrar Intro"}},
            {m: "Abajo", k: {b: "Derecha", a: "Arriba", i: "Recordar Menus"}},
            {m: "Derecha", k: {b: "Izquierda", a: "Abajo", i: special}},
            {m: "Izquierda", k: {b: "Menu", a: "Derecha"}},
            {m: "Menu", k: {b: "Accion", a: "Izquierda"}},
            {m: "Accion", k: {b: "Contextual", a: "Menu"}},
            {m: "Contextual", k: {b: "Defaults", a: "Accion", i: "Defaults"}}]

        for i in range(len(botones)):
            botones[i]['pos'] = [326 + 75 + 3, 38 * i + 64]
            botones[i]['comando'] = self.set_tecla

        return botones

    def crear_restore_btn(self):
        n, k, p, c = 'nombre', 'direcciones', 'pos', 'comando'
        a, b, d = 'arriba', 'abajo', 'derecha'
        dirs = {b: "Mostrar Intro", d: "Contextual"}
        if joystick.get_count():
            dirs.update({a: "Metodo de Entrada"})
        else:
            dirs.update({a: "Recordar Menus"})
        y = self.canvas.get_height() - 32 - 15
        btn = {n: 'Defaults', c: self.restore_defaults, p: [6, y], k: dirs}
        return [btn]

    def crear_espacios_config(self):
        esp = None
        for boton in self.botones:
            nom = boton.nombre.lower()
            x, y = boton.rect.topright
            if nom == "mostrar intro" or nom == "recordar menus":
                nom = nom.replace(' ', '_')
                if self.data[nom]:
                    opt = 'Sí'
                else:
                    opt = 'No'
                esp = Fila(opt, 88, x, y + 9, justification=1)
                self.espacios.add(esp)

            elif nom == 'metodo de entrada':
                nom = nom.replace(' ', '_')
                txt = self.data[nom].title()
                esp = Fila(txt, 88, x, y + 9, justification=1)

            elif nom in self.data[self.curr_input]:
                x, y = boton.rect.topleft
                texto = self.data[self.curr_input][nom]
                nom = key_name(texto)
                esp = Fila(nom, 75, x - 75 - 3, y + 9, justification=1)

            elif nom == 'defaults':
                spr = Sprite()
                spr.nombre = 'dummy space'
                spr.image = Surface((0, 0))
                spr.rect = spr.image.get_rect()

                esp = spr

            self.espacios.add(esp)

    def elegir_boton_espacio(self, n=None):
        if n is None:
            n = self.cur_btn
        tecla = self.espacios.get_sprite(n)
        boton = self.botones.get_sprite(n)
        return boton, tecla

    def cambiar_booleano(self):
        boton, opcion = self.elegir_boton_espacio()

        if opcion.nombre == 'Sí':
            opcion.reset_text('No')
        else:
            opcion.reset_text('Sí')

        if boton.nombre == 'Mostrar Intro':
            Cfg.asignar('mostrar_intro', not Cfg.dato('mostrar_intro'))
        elif boton.nombre == 'Recordar Menus':
            Cfg.asignar('recordar_menus', not Cfg.dato('recordar_menus'))

        self.mostrar_aviso()

    def set_input_device(self):
        boton, opcion = self.elegir_boton_espacio()

        if self.input_device == 'teclado':
            self.input_device = 'gamepad'
            self.curr_input = 'botones'

        elif self.input_device == 'gamepad':
            self.input_device = 'teclado'
            self.curr_input = 'teclas'

        # este bloque cambia todos los espacios por los nombres de las teclas del nuevo input.
        # key names para las teclas del teclado, números para los botones del gamepad.
        opcion.reset_text(self.input_device.title())
        for idx in range(len(self.botones)):
            boton, espacio = self.elegir_boton_espacio(idx)
            nom = boton.nombre.lower()
            if nom in self.data[self.curr_input]:
                txt = self.data[self.curr_input][nom]
                if self.curr_input == 'teclas':
                    espacio.reset_text(key_name(txt))
                else:
                    espacio.reset_text(str(txt))

        self.mostrar_aviso()

    def set_tecla(self):
        """Prepara la tecla elegida para ser cambiada"""

        boton, tecla = self.elegir_boton_espacio()
        boton.ser_presionado()
        tecla.ser_elegido()

        EventDispatcher.trigger('SetMode', self.nombre, {'mode': 'SetKey', 'value': True})

    def cambiar_tecla(self, tcl):
        """Cambia la tecla elgida por el nuevo input
        :param tcl: int
        """

        i_boton, i_tecla = None, None
        # elige segun la posición del cursor.
        boton, tecla = self.elegir_boton_espacio()

        i = -1
        # si la tecla elegida ya está asignada a un comando...
        for fila in self.espacios:
            i += 1
            if key_name(tcl) == fila.nombre:
                # i_x son el boton y la tecla que ya existen
                i_boton, i_tecla = self.elegir_boton_espacio(i)

                break

        tecla.ser_deselegido()
        if i_tecla is not None:
            # acá, si tcl ya está asignada a otro comando, se intercambian las teclas entre esos comandos.
            i_tecla.reset_text(tecla.nombre)
            idx = Cfg.dato(self.curr_input + '/' + i_boton.nombre.lower())
            Cfg.asignar(self.curr_input + '/' + i_boton.nombre.lower(), idx)

        if tecla.nombre != key_name(tcl):
            # acá comprobamos que la tecla elegida sea de hecho distinta a la que ya está
            tecla.reset_text(key_name(tcl))
            Cfg.asignar(self.curr_input + '/' + boton.nombre.lower(), tcl)

            # porque si no lo es, no hay que mostrar el aviso de los cambios.
            self.mostrar_aviso()

    def restore_defaults(self):
        data = Cfg.defaults()
        for idx in range(len(self.botones)):
            boton, espacio = self.elegir_boton_espacio(idx)
            nom = boton.nombre.lower()
            if nom in data['teclas']:
                txt = data['teclas'][nom]
                espacio.reset_text(key_name(txt))
                Cfg.asignar('teclas/'+nom, txt)
            else:
                nom = nom.replace(' ', '_')
                if nom in data:
                    if type(data[nom]) is str:
                        txt = data[nom].title()
                    elif data[nom]:
                        txt = 'Sí'
                    else:
                        txt = 'No'
                    espacio.reset_text(txt)
                    Cfg.asignar(nom, data[nom])

        self.canvas.fill(self.bg_cnvs, self.notice_area)

    def create_notice(self):
        """Crea el aviso de que la configuración cambiará al salir del menú"""
        texto = 'Los cambios tendrán efecto al salir de este menú'
        fuente = font.SysFont('verdana', 14)
        w, h = fuente.size(texto)
        x, y = self.canvas.get_width() - w - 15, self.canvas.get_height() - h - 15
        rect = Rect(x, y, w, h + 1)
        render = render_textrect(texto, fuente, rect, self.font_low_color, self.bg_cnvs)

        return render, rect

    def mostrar_aviso(self):
        """Muestra el aviso del cambio en la configuración"""
        self.canvas.blit(self.notice, self.notice_area)

    def cancelar(self):
        TECLAS.asignar(Cfg.dato(self.curr_input))
        Cfg.asignar('metodo_de_entrada', self.input_device)
        Cfg.guardar()

        self.canvas.fill(self.bg_cnvs, self.notice_area)
        return True

    def update(self):
        self.botones.update()
        self.botones.draw(self.canvas)
        self.espacios.draw(self.canvas)

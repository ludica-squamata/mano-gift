from engine.globs.eventDispatcher import EventDispatcher
from engine.globs import TECLAS, TEXT_DIS, CANVAS_BG, TEXT_SEL
from pygame.sprite import LayeredUpdates, Sprite
from pygame import Rect, font, joystick, Surface
from engine.libs.textrect import render_textrect
from engine.misc.config import Config as Cfg
from pygame.key import name as key_name
from engine.UI.widgets import Fila
from .menu import Menu


class MenuOpciones(Menu):
    input_device = 'teclado'
    espacios = None
    notice = None
    notice_area = None

    def __init__(self):
        super().__init__('Opciones')
        self.data = Cfg.cargar()

        self.botones = LayeredUpdates()
        self.espacios = LayeredUpdates()
        self.establecer_botones(self.create_buttons(), 6)
        self.crear_espacios_config()
        self.notice, self.notice_area = self.create_notice()
        exp, rect = self.create_explanation()
        self.canvas.blit(exp, rect)

        self.functions['tap'].update({
            'accion': self.press_button,
            'arriba': lambda: self.select_one('arriba'),
            'abajo': lambda: self.select_one('abajo'),
            'izquierda': lambda: self.select_one('izquierda'),
            'derecha': lambda: self.select_one('derecha')})

        self.functions['hold'].update({
            'accion': self.mantener_presion,
            'arriba': lambda: self.select_one('arriba'),
            'abajo': lambda: self.select_one('abajo'),
            'izquierda': lambda: self.select_one('izquierda'),
            'derecha': lambda: self.select_one('derecha')})

        self.functions['release'].update({
            'accion': self.liberar_presion})

    def listener(self, event):
        if 'nom' not in event.data:
            self.new_key_event(event)
        else:
            super().listener(event)

    def create_buttons(self):
        n, d, p, c = 'nombre', 'direcciones', 'pos', 'comando'
        a, b = 'arriba', 'abajo'
        factor_y = 2
        
        nombres = "Mostrar Intro,Recordar Menus,Arriba,Abajo,Derecha,Izquierda,Menu,Accion,Contextual,Defaults".split(",")
        botones = []
        for j, nombre in enumerate(nombres):
            if j == 0 or j == 1:
                cmd = self.cambiar_booleano
            elif j == 9:
                cmd = self.restore_defaults
            else:
                cmd = self.set_tecla
            botones.append({n: nombre, c: cmd, d: {a: nombres[j-1], b: nombres[j-(len(nombres)-1)]}})

        if joystick.get_count():
            factor_y = 1
            botones[1][d][b] = botones[2][d][a] = "Metodo de Entrada"
            botones.insert(2, {n: "Metodo de Entrada", c: self.set_input_device, d: {b: "Arriba", a: "Recordar Menus"}})

        for i in range(len(botones)):
            botones[i][p] = [6, 38 * i + (32*factor_y)]

        return botones

    def crear_espacios_config(self):
        margen_derecho = 3
        margen_inferior = 9
        ancho = 88
        for boton in self.botones:
            nom = boton.nombre.lower()
            x, y = boton.rect.topright
            x += margen_derecho
            y += margen_inferior
            if nom == "mostrar intro" or nom == "recordar menus":
                nom = nom.replace(' ', '_')
                if self.data[nom]:
                    opt = 'Sí'
                else:
                    opt = 'No'
                esp = Fila(opt, ancho, x, y, justification=1)

            elif nom == 'metodo de entrada':
                nom = nom.replace(' ', '_')
                txt = self.data[nom].title()
                esp = Fila(txt, ancho, x, y, justification=1)

            elif nom in self.data['comandos']:
                texto = self.data['comandos'][nom]
                nom = key_name(texto)
                esp = Fila(nom, ancho, x, y, justification=1)

            else:
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

        elif self.input_device == 'gamepad':
            self.input_device = 'teclado'

        # este bloque cambia todos los espacios por los nombres de las teclas del nuevo input.
        # key names para las teclas del teclado, números para los botones del gamepad.
        opcion.reset_text(self.input_device.title())
        for idx in range(len(self.botones)):
            boton, espacio = self.elegir_boton_espacio(idx)
            nom = boton.nombre.lower()
            if nom in self.data['comandos']:
                txt = self.data['comandos'][nom]
                if self.input_device == 'teclado':
                    espacio.reset_text(key_name(txt))
                elif self.input_device == 'gamepad':
                    espacio.reset_text("None")

        self.mostrar_aviso()

    def set_tecla(self):
        """Prepara la tecla elegida para ser cambiada"""

        boton, tecla = self.elegir_boton_espacio()
        boton.ser_presionado()
        tecla.ser_elegido()

        EventDispatcher.trigger('ToggleSetKey', 'MenuOpciones', {'value': True})

    def new_key_event(self, event):
        if self.input_device == event.data['device']:
            self.cambiar_tecla(event.data['key'])
            EventDispatcher.trigger('ToggleSetKey', 'Modo.Menu', {'value': False})

    def cambiar_tecla(self, tcl):
        """Cambia la tecla elgida por el nuevo input
        :param tcl: int
        """

        i_boton, i_tecla = None, None
        # elige segun la posición del cursor.
        boton, tecla = self.elegir_boton_espacio()

        # si la tecla elegida ya está asignada a un comando...
        for i, fila in enumerate(self.espacios):
            if key_name(tcl) == fila.nombre:
                # i_x son el boton y la tecla que ya existen
                i_boton, i_tecla = self.elegir_boton_espacio(i)

                break

        tecla.ser_deselegido()
        if i_tecla is not None:
            # acá, si tcl ya está asignada a otro comando, se intercambian las teclas entre esos comandos.
            i_tecla.reset_text(tecla.nombre)
            idx = Cfg.dato('comandos/' + i_boton.nombre.lower())
            Cfg.asignar('comandos/' + i_boton.nombre.lower(), idx)

        if tecla.nombre != key_name(tcl):
            # acá comprobamos que la tecla elegida sea de hecho distinta a la que ya está
            tecla.reset_text(key_name(tcl))
            Cfg.asignar('comandos/' + boton.nombre.lower(), tcl)

            # porque si no lo es, no hay que mostrar el aviso de los cambios.
            self.mostrar_aviso()

    def restore_defaults(self):
        data = Cfg.defaults()
        for idx in range(len(self.botones)):
            boton, espacio = self.elegir_boton_espacio(idx)
            nom = boton.nombre.lower()
            if nom in data['comandos']:
                txt = data['comandos'][nom]
                espacio.reset_text(key_name(txt))
                Cfg.asignar('comandos/'+nom, txt)
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

        self.canvas.fill(CANVAS_BG, self.notice_area)

    def create_notice(self):
        """Crea el aviso de que la configuración cambiará al salir del menú"""
        texto = 'Los cambios tendrán efecto al salir de este menú'
        fuente = font.SysFont('verdana', 14)
        w, h = fuente.size(texto)
        x, y = self.canvas.get_width() - w - 15, self.canvas.get_height() - h - 27
        rect = Rect(x, y, w, h + 1)
        render = render_textrect(texto, fuente, rect, TEXT_DIS, CANVAS_BG)

        return render, rect

    def mostrar_aviso(self):
        """Muestra el aviso del cambio en la configuración"""
        self.canvas.blit(self.notice, self.notice_area)

    @staticmethod
    def create_explanation():
        texto = 'Usa las teclas de movimiento (Arriba, Abajo, Izquierda y Derecha) para que tu personaje se desplace ' \
                'por el mapa.\n\nLa tecla Menú abre el menú Pausa.\n\nLa tecla de Acción te permite interactuar con ' \
                'el ambiente, hablar con otros personajes y también atacar.\n\nUsa la tecla Contextual para cambiar ' \
                'entre las opciones de Acción y muchas cosas más! '
        fuente = font.SysFont('verdana', 15)
        w = 300
        h = 270
        x, y = 300, 128
        rect = Rect(x, y, w, h)
        render = render_textrect(texto, fuente, rect, TEXT_SEL, CANVAS_BG, justification=1)
        return render, rect

    def cancelar(self):
        TECLAS.asignar(Cfg.dato('comandos'))
        Cfg.asignar('metodo_de_entrada', self.input_device)
        Cfg.guardar()

        self.canvas.fill(CANVAS_BG, self.notice_area)
        super().cancelar()

    def update(self):
        self.botones.update()
        self.botones.draw(self.canvas)
        self.espacios.draw(self.canvas)

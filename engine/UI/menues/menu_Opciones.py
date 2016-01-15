from pygame.sprite import LayeredUpdates
from pygame.key import name as key_name
from pygame import Rect, font, joystick
from engine.UI.widgets import Fila
from engine.globs.constantes import Constants as Cs
from engine.globs.eventDispatcher import EventDispatcher
from engine.misc.config import Config as Cfg
from engine.libs.textrect import render_textrect
from .menu_Pausa import MenuPausa
from .menu import Menu


class MenuOpciones(MenuPausa, Menu):
    def __init__(self):
        Menu.__init__(self, 'Opciones')
        self.data = Cfg.cargar()

        self.botones = LayeredUpdates()
        self.espacios = LayeredUpdates()
        self.establecer_botones(self.crear_botones_config(), 6)
        self.establecer_botones(self.crear_botones_teclas(), 4)
        self.crear_espacios_config()
        
        self.functions.update({
            'tap':{
                'hablar':self.press_button,
                'arriba': lambda: self.select_one('arriba'),
                'abajo': lambda: self.select_one('abajo'),
                'izquierda': lambda: self.select_one('izquierda'),
                'derecha': lambda: self.select_one('derecha')
            },
            'hold':{
                'hablar': self.mantener_presion,
                'arriba': lambda: self.select_one('arriba'),
                'abajo': lambda: self.select_one('abajo'),
                'izquierda': lambda: self.select_one('izquierda'),
                'derecha': lambda: self.select_one('derecha')
            },
            'release':{
                'hablar': self.liberar_presion,
            }
        })

    def crear_botones_config(self):
        m, k, p, c = 'nombre', 'direcciones', 'pos', 'comando'
        a, b, i, d = 'arriba', 'abajo', 'izquierda', 'derecha'
        dy, f = 64, 38  # constantes numéricas de posicion # f = fila
        cmd1 = self.cambiar_booleano
        cmd2 = self.set_input_device
        if joystick.get_count():
            botones = [
                {m: "Mostrar Intro", c: cmd1, p: [6, f * 0 + dy], k: {b: "Recordar Menus", a: "Salir"}},
                {m: "Recordar Menus", c: cmd1, p: [6, f * 1 + dy], k: {b: "Metodo de Entrada", a: "Mostrar Intro"}},
                {m: "Metodo de Entrada", c: cmd2, p: [6, f * 2 + dy], k: {b: "Arriba", a: "Recordar Menus"}}
            ]
        else:
            botones = [
                {m: "Mostrar Intro", c: cmd1, p: [6, f * 0 + dy], k: {b: "Recordar Menus", a: "Salir"}},
                {m: "Recordar Menus", c: cmd1, p: [6, f * 1 + dy], k: {b: "Arriba", a: "Mostrar Intro"}}
            ]
            

        return botones

    def crear_botones_teclas(self):
        # abreviaturas para hacer más legible el código
        m, k, p, c = 'nombre', 'direcciones', 'pos', 'comando'
        a, b, i, d = 'arriba', 'abajo', 'izquierda', 'derecha'
        x1, x2 = 6, 226
        dy, f = 185, 38  # constantes numéricas de posicion # f = fila
        cmd = self.set_tecla
        if joystick.get_count():
            special = "Metodo de Entrada"
        else:
            special = "Recordar Menus"
        botones = [
            # primera columna
            {m: "Arriba", c: cmd, p: [x1, f * 0 + dy], k: {b: "Abajo", a: special, d: "Accion"}},
            {m: "Abajo", c: cmd, p: [x1, f * 1 + dy], k: {b: "Derecha", a: "Arriba", d: "Hablar"}},
            {m: "Derecha", c: cmd, p: [x1, f * 2 + dy], k: {b: "Izquierda", a: "Abajo", d: "Inventario"}},
            {m: "Izquierda", c: cmd, p: [x1, f * 3 + dy], k: {b: "Menu", a: "Derecha", d: "Cancelar"}},
            {m: "Menu", c: cmd, p: [x1, f * 4 + dy], k: {b: "Debug", a: "Izquierda", d: "Posicion"}},
            {m: "Debug", c: cmd, p: [x1, f * 5 + dy], k: {b: "Accion", a: "Menu", d: "Salir"}},
            # segunda columna
            {m: "Accion", c: cmd, p: [x2, f * 0 + dy], k: {b: "Hablar", a: "Debug", i: "Arriba"}},
            {m: "Hablar", c: cmd, p: [x2, f * 1 + dy], k: {b: "Inventario", a: "Accion", i: "Abajo"}},
            {m: "Inventario", c: cmd, p: [x2, f * 2 + dy], k: {b: "Cancelar", a: "Hablar", i: "Derecha"}},
            {m: "Cancelar", c: cmd, p: [x2, f * 3 + dy], k: {b: "Posicion", a: "Inventario", i: "Izquierda"}},
            {m: "Posicion", c: cmd, p: [x2, f * 4 + dy], k: {b: "Salir", a: "Cancelar", i: "Menu"}},
            {m: "Salir", c: cmd, p: [x2, f * 5 + dy], k: {b: "Mostrar Intro", a: "Posicion", i: "Debug"}}]

        return botones

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
                esp = Fila(opt, 88, x, y + 9, justification = 1)
                self.espacios.add(esp)

            elif nom == 'metodo de entrada':
                nom = nom.replace(' ', '_')
                txt = self.data[nom].title()
                esp = Fila(txt, 88, x, y + 9, justification = 1)

            elif nom in self.data['teclas']:
                texto = self.data['teclas'][nom]
                nom = key_name(texto)
                esp = Fila(nom, 75, x + 3, y + 9, justification = 1)

            self.espacios.add(esp)

    def elegir_boton_espacio(self):
        n = self.cur_btn
        tecla = self.espacios.get_sprite(n)
        boton = self.botones.get_sprite(n)
        return boton, tecla

    def cambiar_booleano(self):
        boton, opcion = self.elegir_boton_espacio()

        if opcion.nombre == 'Sí':
            opcion.set_text('No', 88, 1)
        else:
            opcion.set_text('Sí', 88, 1)

        if boton.nombre == 'Mostrar Intro':
            Cfg.asignar('mostrar_intro', not Cfg.dato('mostrar_intro'))
        elif boton.nombre == 'Recordar Menus':
            Cfg.asignar('recordar_menus', not Cfg.dato('recordar_menus'))

    def set_input_device(self):
        boton, opcion = self.elegir_boton_espacio()

        nombre = ''
        if opcion.nombre == 'Teclado':
            nombre = 'Gamepad'
            Cs.TECLAS.asignar(Cfg.dato('botones'))
        elif opcion.nombre == 'Gamepad':
            nombre = 'Teclado'
            Cs.TECLAS.asignar(Cfg.dato('teclas'))

        opcion.set_text(nombre, 88, 1)
        Cfg.asignar('metodo_de_entrada', nombre.lower())

    def set_tecla(self):
        '''Prepara la tecla elegida para ser cambiada'''

        boton, tecla = self.elegir_boton_espacio()
        boton.ser_presionado()
        tecla.ser_elegido()

        EventDispatcher.trigger('SetMode',self.nombre,{'mode': 'SetKey','value':True})

    def cambiar_tecla(self, tcl):
        """Cambia la tecla elgida por el nuevo input
        :param tcl: int
        """

        boton, tecla = self.elegir_boton_espacio()
        tecla.ser_deselegido()
        tecla.set_text(key_name(tcl), 75, 1)
        Cfg.asignar('teclas/' + boton.nombre.lower(), tcl)
        self.mostrar_aviso()

    def mostrar_aviso(self):
        """Muestra el aviso de que la configuración cambiará al reiniciar"""

        texto = 'Los cambios tendrán efecto al salir de este menú'
        fuente = font.SysFont('verdana', 14)
        w, h = fuente.size(texto)
        x, y = self.canvas.get_width() - w - 15, self.canvas.get_height() - h - 15
        rect = Rect(x, y, w, h + 1)
        render = render_textrect(texto, fuente, rect, self.font_low_color, self.bg_cnvs)
        self.canvas.blit(render, rect)

    def cancelar(self):
        return True

    def update(self):
        self.botones.update()
        self.botones.draw(self.canvas)
        self.espacios.draw(self.canvas)

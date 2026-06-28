from engine.globs.azoe_group import AzoeGroup, AzoeBaseSprite
from engine.globs.event_dispatcher import EventDispatcher
from pygame import Rect, font, joystick, Surface, draw
from engine.libs.textrect import render_textrect
from engine.misc.config import Config as Cfg
from engine.UI.widgets import Fila, Boton
from engine.globs.colores import Colores as Col
from pygame.key import name as key_name
from engine.IO.teclas import Teclas
from itertools import cycle
from pygame import Color
from .menu import Menu


class MenuOpciones(Menu):
    input_device = 'teclado'
    espacios = None
    notice = None
    notice_area = None

    def __init__(self, parent):
        super().__init__(parent, 'Opciones')
        # self.w = 300
        self.crear_titulo('Opciones')
        self.data = Cfg.cargar()

        self.botones = AzoeGroup('Botones')
        self.espacios = AzoeGroup('Espacios')
        self.colores = AzoeGroup('Colores')
        self.muestras = AzoeGroup("Muestras")
        draw.aaline(self.canvas, [0, 0, 0], [277, 30], [277, 450])
        self.crear_color_lables()
        self.establecer_botones(self.create_buttons(), 5.5)
        self.crear_espacios_config()
        self.notice, self.notice_area = self.create_notice()

        self.theme_cycler = cycle(list(Col.themes.keys()) + ['Temas'])
        next(self.theme_cycler)

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

        EventDispatcher.register(self.new_key_event, 'SetNewKey')

    def crear_titulo(self, titulo):
        fuente = font.Font('engine/libs/Verdana.ttf', 16)
        self.titulo = titulo
        fuente.set_underline(True)
        ttl_rect = Rect((8, 3), (self.w - 7, 30))
        ttl_txt = render_textrect(titulo, fuente, ttl_rect, Col.TEXT_SEL, Col.CANVAS_BG, 1)
        self.canvas.blit(ttl_txt, ttl_rect.topleft)

    def crear_color_lables(self):
        colores = ('Canvas,BiselBG,BiselFG,TextFG,TextUns,TextSel,BoxBack,'
                   'BoxText,SlotBG,MenuTxt,ScrollBG,ScrollArr').split(',')
        muestras = Col.CANVAS_BG, Col.BISEL_BG, Col.BISEL_FG, Col.TEXT_FG, Col.TEXT_DIS, Col.TEXT_SEL, Col.BOX_SEL_BACK,
        muestras += Col.BOX_SEL_TEXT, Col.SLOT_BG, Col.MENU_TEXT, Col.SCROLL_BG, Col.SCROLL_ARROW
        botones = []

        for i, color in enumerate(colores):
            esp = Fila(self, color, 80, 280, 32 + (i * 36), justification=2)
            self.colores.add(esp)

            m = EspacioColor(self, color, i, muestras[i], 370, 34 + (i * 36))
            self.muestras.add(m)

            boton_minusR = BotonMod(self, 28, i, '-', 'R', [438, 26 + (i * 36)], texto='-')
            boton_plusR = BotonMod(self, 28, i, '+', 'R', [403, 26 + (i * 36)], texto="+")
            botones.append(boton_plusR)
            botones.append(boton_minusR)

            boton_minusG = BotonMod(self, 28, i, '-', 'G', [507, 26 + (i * 36)], texto='-')
            boton_plusG = BotonMod(self, 28, i, '+', 'G', [474, 26 + (i * 36)], texto="+")
            botones.append(boton_plusG)
            botones.append(boton_minusG)

            boton_minusB = BotonMod(self, 28, i, '-', 'B', [577, 26 + (i * 36)], texto="-")
            boton_plusB = BotonMod(self, 28, i, '+', 'B', [544, 26 + (i * 36)], texto="+")
            botones.append(boton_plusB)
            botones.append(boton_minusB)

            boton_plusR.direcciones['derecha'] = f'minusR-{i}'
            boton_minusR.direcciones['derecha'] = f'plusG-{i}'
            boton_plusG.direcciones['derecha'] = f'minusG-{i}'
            boton_minusG.direcciones['derecha'] = f'plusB-{i}'
            boton_plusB.direcciones['derecha'] = f'minusB-{i}'

            boton_minusB.direcciones['izquierda'] = f'plusB-{i}'
            boton_minusG.direcciones['izquierda'] = f'plusG-{i}'
            boton_minusR.direcciones['izquierda'] = f'plusR-{i}'
            boton_plusB.direcciones['izquierda'] = f'minusG-{i}'
            boton_plusG.direcciones['izquierda'] = f'minusR-{i}'

            boton_plusR.direcciones['abajo'] = f'plusR-{i + 1}'
            boton_plusG.direcciones['abajo'] = f'plusG-{i + 1}'
            boton_plusB.direcciones['abajo'] = f'plusB-{i + 1}'

            boton_minusR.direcciones['abajo'] = f'minusR-{i + 1}'
            boton_minusG.direcciones['abajo'] = f'minusG-{i + 1}'
            boton_minusB.direcciones['abajo'] = f'minusB-{i + 1}'

            boton_plusR.direcciones['arriba'] = f'plusR-{i - 1}'
            boton_plusG.direcciones['arriba'] = f'plusG-{i - 1}'
            boton_plusB.direcciones['arriba'] = f'plusB-{i - 1}'

            boton_minusR.direcciones['arriba'] = f'minusR-{i - 1}'
            boton_minusG.direcciones['arriba'] = f'minusG-{i - 1}'
            boton_minusB.direcciones['arriba'] = f'minusB-{i - 1}'

        self.botones.add(*botones, layer=1)

        for j, k in enumerate(['R', 'G', 'B']):
            esp = Fila(self, k, 20, 430 + j * 70, 6, justification=1)
            self.colores.add(esp)

        botones[0].direcciones['izquierda'] = 'Mostrar Intro'
        botones[6].direcciones['izquierda'] = 'Recordar Menus'
        botones[12].direcciones['izquierda'] = 'Metodo de Entrada'
        botones[18].direcciones['izquierda'] = 'Arriba'
        botones[24].direcciones['izquierda'] = 'Abajo'
        botones[30].direcciones['izquierda'] = 'Derecha'
        botones[42].direcciones['izquierda'] = 'Izquierda'
        botones[48].direcciones['izquierda'] = 'Menu'
        botones[54].direcciones['izquierda'] = 'Accion'
        botones[60].direcciones['izquierda'] = 'Contextual'
        botones[66].direcciones['izquierda'] = 'Defaults'

    def rotate_themes(self):
        theme = next(self.theme_cycler)
        button_themes = self.botones.get_sprite(11)
        button_themes.texto = theme
        button_themes.rewrite()
        if theme != 'Temas':
            Col.set_theme(theme)
        else:
            Col.restore_defaults()

    def create_buttons(self):
        n, d, p, c = 'nombre', 'direcciones', 'pos', 'comando'
        a, b, r = 'arriba', 'abajo', "derecha"
        factor_y = 2

        nom = "Mostrar Intro,Recordar Menus,Arriba,Abajo,Derecha,Izquierda,Menu,Accion,Contextual,Defaults,Temas"
        nom = nom.split(',')
        botones = []
        for j, nombre in enumerate(nom):
            if j == 0 or j == 1:
                cmd = self.cambiar_booleano
            elif j == 9:
                cmd = self.restore_defaults
            elif j == 10:
                cmd = self.rotate_themes
            else:
                cmd = self.set_tecla

            # g = j if j != 2 else j + 2  # éste loop saltea "Metodo de Entrada", por eso esta linea.
            k = self.botones.sprs()[j * 6].nombre

            botones.append({n: nombre, c: cmd, d: {a: nom[j - 1], b: nom[j - (len(nom) - 1)], r: k}})

        if joystick.get_count():
            factor_y = 1
            botones[1][d][b] = botones[2][d][a] = "Metodo de Entrada"
            botones.insert(2, {n: "Metodo de Entrada", c: self.set_input_device,
                               d: {b: "Arriba", a: "Recordar Menus", r: self.botones.sprs()[12].nombre}})

        for i in range(len(botones)):
            botones[i][p] = [6, 38 * i + (3 * factor_y)]

        return botones

    def crear_espacios_config(self):
        margen_derecho = 0
        margen_inferior = 9
        ancho = 88
        for boton in self.botones.sprs():
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
                esp = Fila(self, opt, ancho, x, y, justification=1)

            elif nom == 'metodo de entrada':
                nom = nom.replace(' ', '_')
                txt = self.data[nom].title()
                esp = Fila(self, txt, ancho, x, y, justification=1)

            elif nom in self.data['comandos']:
                texto = self.data['comandos'][nom]
                nom = key_name(texto)
                esp = Fila(self, nom, ancho, x, y, justification=1)

            else:
                nombre = 'dummy space'
                image = Surface((0, 0))
                rect = image.get_rect()
                esp = AzoeBaseSprite(self, nombre, image, rect)

            self.espacios.add(esp)

    def elegir_boton_espacio(self, n=None):
        if n is None:
            n = self.cur_btn
        tecla = self.espacios.get_spr(n)
        boton = self.botones.get_spr(n)
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

        # self.mostrar_aviso()

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

        # self.mostrar_aviso()

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
            # self.mostrar_aviso()

    def restore_defaults(self):
        data = Cfg.defaults()
        for idx in range(len(self.botones.get_sprites_from_layer(0))):
            boton, espacio = self.elegir_boton_espacio(idx)
            nom = boton.nombre.lower()
            if nom in data['comandos']:
                txt = data['comandos'][nom]
                espacio.reset_text(key_name(txt))
                Cfg.asignar('comandos/' + nom, txt)
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

        for esp in self.muestras.sprs():
            esp.restore()

        Col.restore_defaults()

        # self.canvas.fill(Col.CANVAS_BG, self.notice_area)

    def create_notice(self):
        """Crea el aviso de que la configuración cambiará al salir del menú"""
        texto = 'Los cambios tendrán efecto al salir de este menú'
        fuente = font.SysFont('verdana', 14)
        w, h = fuente.size(texto)
        x, y = self.canvas.get_width() - w - 15, self.canvas.get_height() - h - 27
        rect = Rect(x, y, w, h + 1)
        render = render_textrect(texto, fuente, rect, Col.TEXT_DIS, Col.CANVAS_BG)

        return render, rect

    # def mostrar_aviso(self):
    #     """Muestra el aviso del cambio en la configuración"""
    #     self.canvas.blit(self.notice, self.notice_area)

    def cancelar(self):
        Teclas.asignar(data=Cfg.dato('comandos'))
        Cfg.asignar('metodo_de_entrada', self.input_device)
        Cfg.guardar()

        # self.canvas.fill(Col.CANVAS_BG, self.notice_area)
        super().cancelar()

    def update(self):
        super().update()
        draw.aaline(self.canvas, [0, 0, 0], [277, 30], [277, 450])
        self.botones.update()
        self.muestras.update()

        self.botones.draw(self.canvas)
        self.espacios.draw(self.canvas)
        self.muestras.draw(self.canvas)
        self.colores.draw(self.canvas)


class EspacioColor(AzoeBaseSprite):
    has_changed = False
    new_color = None

    def __init__(self, parent, nombre, indice, base_color, x, y):
        image = Surface([20, 20])
        self.w, self.h = image.get_size()
        self.base_color = base_color
        image.fill(base_color, [1, 1, self.w - 2, self.h - 2])
        rect = image.get_rect(topleft=[x, y])
        self.indice = indice
        self.keyname = self.traducir(nombre)
        super().__init__(parent, f'{nombre}-{indice}', image, rect)

        EventDispatcher.register(self.alter_color, 'Operation')
        EventDispatcher.register(self.recolor, 'AlterColor')

    @staticmethod
    def traducir(nombre):
        if nombre == 'Canvas':
            return 'CANVAS_BG'
        elif nombre == 'BiselBG':
            return 'BISEL_BG'
        elif nombre == 'BiselFG':
            return 'BISEL_FG'
        elif nombre == 'TextFG':
            return 'TEXT_FG'
        elif nombre == 'TextUns':
            return 'TEXT_DIS'
        elif nombre == 'TextSel':
            return 'TEXT_SEL'
        elif nombre == 'BoxBack':
            return "BOX_SEL_BACK"
        elif nombre == 'BoxText':
            return "BOX_SEL_TEXT"
        elif nombre == 'MenuBG':
            return "MENU_BG"
        elif nombre == 'MenuTxt':
            return "MENU_TEXT"
        elif nombre == 'ScrollBG':
            return "SCROLL_BG"
        elif nombre == 'ScrollArr':
            return "SCROLL_ARROW"

    def alter_color(self, event):
        operation = event.data['op']
        channel = event.data['cnl']
        if 'held' in event.data:
            delta = event.data['held'] // 2
        else:
            delta = 1

        if self.indice == event.data['idx']:
            r, g, b, a = self.base_color if self.new_color is None else self.new_color
            if operation == '+':
                if channel == 'R':
                    r += delta if r + delta <= 255 else 0
                elif channel == 'G':
                    g += delta if g + delta <= 255 else 0
                elif channel == 'B':
                    b += delta if b + delta <= 255 else 0

            elif operation == '-':
                if channel == 'R':
                    r -= delta if r - delta >= 0 else 0
                elif channel == 'G':
                    g -= delta if g - delta >= 0 else 0
                elif channel == 'B':
                    b -= delta if b - delta >= 0 else 0
            self.new_color = Color(r, g, b)
            Col.set_color(self.keyname, self.new_color)
            EventDispatcher.trigger('AlterColor', self, {'name': self.keyname, 'color': self.new_color})

            self.image.fill(self.new_color, [1, 1, self.w - 2, self.h - 2])

            if self.new_color != self.base_color:
                self.has_changed = True

    def restore(self):
        self.new_color = self.base_color
        self.image.fill(self.base_color, [1, 1, self.w - 2, self.h - 2])

    def __repr__(self):
        return f'Espacio {self.nombre}'

    def recolor(self, event):
        # this is because setting a theme doesn't trigger self.alter_color()
        if event.data['name'] == self.keyname:
            self.new_color = event.data['color']
            self.image.fill(event.data['color'], [1, 1, self.w - 2, self.h - 2])


class BotonMod(Boton):

    def __init__(self, parent, ancho_mod, idx, op, cnl, pos, texto=None):
        self.op = op
        self.cnl = cnl
        self.idx = idx

        if op == '-':
            nombre = f'minus{cnl}-{idx}'
        else:
            nombre = f'plus{cnl}-{idx}'
        super().__init__(parent, nombre, ancho_mod, None, pos, texto=texto)
        self.enable_holding = True

        self.comando_1 = self.operation_1
        self.set_comando2(self.operation_2)

    def operation_1(self):
        EventDispatcher.trigger('Operation', self, {'cnl': self.cnl, 'op': self.op, 'idx': self.idx})

    def operation_2(self):
        EventDispatcher.trigger('Operation', self, {'cnl': self.cnl, 'op': self.op, 'idx': self.idx, 'held': self.held})

    def crear(self, texto, ancho):

        rect = Rect((-1, -1), (ancho - 6, ancho - 6))

        cnvs_pre = Surface((ancho + 6, ancho + 6))
        cnvs_pre.fill(Col.CANVAS_BG)
        cnvs_sel = cnvs_pre.copy()
        cnvs_uns = cnvs_pre.copy()
        cnvs_dis = cnvs_pre.copy()

        fnd_pre = self.create_sunken_canvas(ancho, ancho)
        fnd_uns = self.create_raised_canvas(ancho, ancho)

        for i in range(round((ancho + 6) / 3)):
            # linea punteada horizontal superior
            draw.line(cnvs_sel, Col.BOX_SEL_BACK, (i * 7, 0), ((i * 7) + 5, 0), 2)

            # linea punteada horizontal inferior
            draw.line(cnvs_sel, Col.BOX_SEL_BACK, (i * 7, ancho + 4), ((i * 7) + 5, ancho + 4), 2)

        for i in range(round((ancho + 6) / 3)):
            # linea punteada vertical derecha
            draw.line(cnvs_sel, Col.BOX_SEL_BACK, (0, i * 7), (0, (i * 7) + 5), 2)

            # linea punteada vertical izquierda
            draw.line(cnvs_sel, Col.BOX_SEL_BACK, (ancho + 4, i * 7), (ancho + 4, (i * 7) + 5), 2)

        cnvs_sel.blit(fnd_uns, (3, 3))
        cnvs_uns.blit(fnd_uns, (3, 3))
        cnvs_dis.blit(fnd_uns, (3, 3))
        cnvs_pre.blit(fnd_pre, (3, 3))

        bold = font.Font('engine/libs/Verdanab.ttf', 16)
        fuente = font.Font('engine/libs/Verdana.ttf', 16)

        btn_sel = render_textrect(texto, bold, rect, Col.TEXT_SEL, Col.CANVAS_BG, 1)
        btn_uns = render_textrect(texto, fuente, rect, Col.TEXT_FG, Col.CANVAS_BG, 1)
        btn_dis = render_textrect(texto, fuente, rect, Col.BISEL_BG, Col.CANVAS_BG, 1)

        cnvs_uns.blit(btn_uns, (6, 6))
        cnvs_sel.blit(btn_sel, (6, 6))
        cnvs_pre.blit(btn_sel, (6, 6))
        cnvs_dis.blit(btn_dis, (6, 6))

        return cnvs_sel, cnvs_pre, cnvs_uns, cnvs_dis

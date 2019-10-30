from engine.globs import CANVAS_BG, TEXT_SEL, BISEL_BG
from engine.UI.widgets import BaseWidget
from engine.globs.azoe_group import AzoeBaseSprite, AzoeGroup
from pygame import font, Rect, Surface, draw


class NameScreen(BaseWidget):
    area_teclas = None
    area_rect = None
    area_input = None
    cursor = None
    teclas = None
    lineas = None
    hidden = False

    # noinspection PyMissingConstructor
    def __init__(self, parent):

        self.parent = parent
        self.teclas = AzoeGroup('Teclas')  # teclado en pantalla
        self.area_input = AzoeGroup('Letras')  # letras del nombre
        self.lineas = AzoeGroup('Linea Punteada')  # linea punteada
        self.ins_txt = "Escriba a continuación el nombre del personaje. Puede usar los caracteres provistos abajo"

        # generar teclado y cursor
        self.area_teclas = self.create_sunken_canvas(448 + 12, 224 + 12)  # marco y parte del fondo del teclado
        r = self.parent.rect
        self.area_rect = self.area_teclas.get_rect(center=(r.centerx - 80, r.centery + 90))
        self.crear_teclas(6, 6)  # genera el teclado en pantalla

        # el espacio se añade por separado porque ' ' es el delimitador en self.crear_teclas
        self.teclas.add(Character(' ', CANVAS_BG, 10 + 12 * 32 + 6, 212 + 6 * 32 + 6))

        # Cursor del teclado en pantalla
        self.cursor = Cursor(*self.teclas.get_sprite(0).rect.center)

        # area del nombre del personaje
        y = 165
        self.area_nombre = Rect(13, y, 400, 25)

        # lineas punteadas
        for i in range(20):
            lin = LineaChr(i, 15 + (i * 20), y + 27)
            self.lineas.add(lin)
        self.lineas.get_sprite(0).isSelected = True

        self.ltr_idx = -1  # idx de self.area_input
        self.lin_idx = 0  # idx de self.lineas

        self.functions = {
                'tap': {
                    'accion': self.input_character,
                    'contextual': self.erase_character,
                    'arriba': lambda: self.movercursor(0, -1),
                    'abajo': lambda: self.movercursor(0, 1),
                    'izquierda': lambda: self.movercursor(-1, 0),
                    'derecha': lambda: self.movercursor(1, 0)
                },
                'hold': {
                    'accion': self.input_character,
                    'arriba': lambda: self.movercursor(0, -1),
                    'abajo': lambda: self.movercursor(0, 1),
                    'izquierda': lambda: self.movercursor(-1, 0),
                    'derecha': lambda: self.movercursor(1, 0)
                },
                'release': {
                    'contextual': self.erase_character
                }
            }

    def crear_teclas(self, x, y):
        """Genera el teclado en pantalla, con excepción del espacio, que se genera por separado"""

        t = "ABCDEFGHI  123JKLMNÑOPQ  456RSTUVWXYZ  789           *0#abcdefghi     jklmnñopq  :+-rstuvwxyz  , ."
        i = -1
        mx, my = self.area_rect.topleft
        for dy in range(7):
            for dx in range(14):
                i += 1
                # este bloque determina el color del fondo de la tecla, para un efecto cuadriculado
                if dy % 2 != 0 and i % 2 != 0 or dy % 2 == 0 and i % 2 == 0:
                    bg = CANVAS_BG
                else:
                    bg = BISEL_BG

                if t[i] != ' ':
                    char = Character(t[i], bg, mx + x + dx * 32, my + y + dy * 32)
                    self.teclas.add(char)
                else:
                    # esta parte pinta el resto del fondo, que no tiene teclas activas
                    rect = Rect(x + dx * 32, y + dy * 32, 32, 32)
                    self.area_teclas.fill(bg, rect)

    def input_character(self):
        """Ingresa el caracter seleccionado a la lista de letras del nombre"""

        if self.lin_idx < len(self.lineas):
            key = self.cursor.current.nombre  # string
            espacio = self.lineas.get_sprite(self.lin_idx).rect

            fuente = font.SysFont('Verdana', 20)
            image = fuente.render(key, 1, (0, 0, 0), CANVAS_BG)
            rect = image.get_rect()
            rect.bottom = espacio.top - 2
            rect.centerx = espacio.centerx
            spr = AzoeBaseSprite(self, key, image, rect)
            spr.key = key

            self.area_input.add(spr)
            self.ltr_idx += 1

            self.select_line(+1)

        if self.lin_idx == len(self.lineas):
            self.parent.cambiar_foco('menu')

    def select_line(self, delta):
        for linea in self.lineas:
            linea.isSelected = False
        self.lin_idx += delta
        if 0 <= self.lin_idx < len(self.lineas):
            self.lineas.get_sprite(self.lin_idx).isSelected = True

    def erase_character(self):
        """Borra el caracter del espacio actualmente seleccionado"""

        if self.ltr_idx >= 0:
            self.parent.canvas.fill(CANVAS_BG, self.area_nombre)

            spr = self.area_input.get_sprite(self.ltr_idx)
            self.area_input.remove(spr)
            self.ltr_idx -= 1

            self.select_line(-1)

    def movercursor(self, dx, dy):
        """Desplaza el cursor por el teclado en pantalla y controla los limites."""
        self.cursor.mover(dx * 32, dy * 32)

        # esta sección controla que el cursor no se quede parado en la nada
        collides = False
        for t in self.teclas:
            if t.rect.collidepoint(self.cursor.pos):
                collides = True
                break

        if not collides:
            if self.area_rect.collidepoint(self.cursor.pos):
                self.movercursor(dx, dy)  # repetir el movimiento
            elif self.cursor.x > self.area_rect.right and len(self.area_input):
                self.parent.cambiar_foco('menu')  # el cursor busca el boton "aceptar"
            else:
                self.movercursor(-dx, -dy)  # deshacer el movimiento

    def use_funcion(self, mode, key):
        if key in self.functions[mode]:
            self.functions[mode][key]()

    def update(self):
        for t in self.teclas:
            if t.rect.collidepoint(self.cursor.pos):
                t.ser_elegido()
                self.cursor.set_current(t)
            elif t.isSelected:
                t.ser_deselegido()

        if not self.hidden:
            self.parent.canvas.blit(self.area_teclas, self.area_rect)
            self.teclas.draw(self.parent.canvas)
            self.lineas.draw(self.parent.canvas)
            self.area_input.draw(self.parent.canvas)

    def toggle_hidden(self):
        self.hidden = not self.hidden


class Character(BaseWidget):
    """Caracter individual del teclado en pantalla"""

    def __init__(self, char, bg, x, y):

        self.img_uns = self._crear_img(char, bg)
        self.img_sel = self.dibujar_seleccion(self.img_uns, TEXT_SEL)

        super().__init__(self.img_uns)
        self.nombre = char
        self.rect.topleft = x, y

    @staticmethod
    def _crear_img(char, bg):
        fuente = font.SysFont('Verdana', 20)
        img = Surface((32, 32))
        img.fill(bg)
        render = fuente.render(char, 1, (0, 0, 0), bg)
        rect = render.get_rect(center=img.get_rect().center)
        img.blit(render, rect)
        return img

    @staticmethod
    def dibujar_seleccion(img, color):
        sel = img.copy()
        w, h = sel.get_size()
        for i in range(round(38 / 3)):
            # linea punteada horizontal superior
            draw.line(sel, color, (i * 7, 0), ((i * 7) + 5, 0), 2)

            # linea punteada horizontal inferior
            draw.line(sel, color, (i * 7, h - 2), ((i * 7) + 5, h - 2), 2)

        for i in range(round(38 / 3)):
            # linea punteada vertical derecha
            draw.line(sel, color, (w - 2, i * 7), (w - 2, (i * 7) + 5), 2)

            # linea punteada vertical izquierda
            draw.line(sel, color, (0, i * 7), (0, (i * 7) + 5), 2)
        return sel

    def __repr__(self):
        return self.nombre


class LineaChr(BaseWidget):
    """Estas son las líneas punteadas del nombre del personaje"""
    animado = False
    idx = 0

    def __init__(self, idx, x, y):
        img = Surface((15, 2))
        img.fill((255, 255, 255))
        super().__init__(img)
        self.rect.topleft = x, y
        self.idx = idx

    def animar(self):
        self.image.fill((255, 0, 0))

    def desanimar(self):
        self.image.fill((255, 255, 255))

    def update(self):
        if self.isSelected:
            self.animar()
        else:
            self.desanimar()


class Cursor:
    """Este es el cursor virtual que se desplaza en el teclado en pantalla"""
    x, y = 0, 0
    current = None

    def __init__(self, x, y):
        self.x, self.y = x, y
        self.pos = x, y

    def mover(self, dx, dy):
        self.x += dx
        self.y += dy
        if self.x < 0:
            self.x = 0
        if self.y < 0:
            self.y = 0

        self.pos = self.x, self.y

    def set_current(self, tecla):
        self.current = tecla

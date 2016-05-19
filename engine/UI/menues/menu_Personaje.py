from engine.misc import Resources
from engine.libs import render_textrect
from engine.globs import Tiempo
from pygame import font, Rect, Surface, draw
from pygame.sprite import LayeredUpdates, Sprite
from .menu import Menu
from engine.UI.widgets import BaseWidget, Boton


class MenuPersonaje(Menu):
    _step = 'D'
    timer_animacion = 0

    char_images = None
    char_face = None
    char_img = None

    foco = 'teclas'

    def __init__(self):
        super().__init__('Personaje')
        self.teclas = LayeredUpdates()  # teclado en pantalla
        self.area_input = LayeredUpdates()  # letras del nombre
        self.lineas = LayeredUpdates()  # linea punteada

        # cargar imagenes
        self.char_face = Resources.cargar_imagen('mobs/imagenes/pc_face.png')
        self.char_images = self.cargar_anims('mobs/imagenes/heroe_idle_walk.png')
        self.char_img = self.char_images['Sabajo']
        self.char_img_rect = Rect(107, 130, 32, 32)

        # generar teclado y cursor
        self.area_teclas = self.create_sunken_canvas(448 + 12, 224 + 12)  # marco y parte del fondo del teclado
        self.area_rect = self.area_teclas.get_rect(center=(self.rect.centerx - 80, self.rect.centery + 90))
        self.crear_teclas(6, 6)  # genera el teclado en pantalla

        # el espacio se añade por separado porque ' ' es el delimitador en self.crear_teclas
        self.teclas.add(Character(' ', self.bg_cnvs, 10 + 12 * 32 + 6, 212 + 6 * 32 + 6))

        # Cursor del teclado en pantalla
        self.cursor = Cursor(*self.teclas.get_sprite(0).rect.center)

        # area del nombre del personaje
        self.area_nombre = Rect(143, 140, 400, 25)

        # lineas punteadas
        for i in range(20):
            lin = LineaChr(i, 145 + (i * 20), 140 + 27)
            self.lineas.add(lin)
        self.lineas.get_sprite(0).isSelected = True

        self.ltr_idx = -1  # idx de self.area_input
        self.lin_idx = 0  # idx de self.lineas

        # generar boton 'Aceptar'
        aceptar = Boton('Aceptar', 3, self.aceptar, (self.area_rect.right + 20, self.area_rect.bottom - 35))
        self.botones.add(aceptar)  # self.botones es herencia de Menu

        # dibujos estáticos
        self.canvas.blit(self.char_face, (10, 100))
        self.canvas.blit(self.area_teclas, self.area_rect)
        self.print_instructions()

        # determinar qué tecla activa qué función.
        self.functions.update({  # obsérvese que es dict.update()
            'teclas': {
                'tap': {
                    'accion': self.input_character,
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
                }
            },
            'botones': {
                'tap': {
                    'accion': self.press_button,
                    'izquierda': lambda: self.cambiar_foco('teclas'),
                    'arriba': lambda: self.cambiar_foco('teclas'),
                },
                'hold': {
                    'accion': self.mantener_presion,
                    'izquierda': lambda: self.cambiar_foco('teclas'),
                    'arriba': lambda: self.cambiar_foco('teclas'),
                },
                'release': {
                    'accion': self.liberar_presion
                }
            }})

    def print_instructions(self):
        s = "Escriba a continuación el nombre del personaje. Puede usar los caracteres provistos abajo"
        fuente = font.SysFont('Verdana', 14, italic=True)
        rect = Rect(10, 32, 600, 64)
        render = render_textrect(s, fuente, rect, self.font_none_color, self.bg_cnvs)
        self.canvas.blit(render, rect)

    def use_function(self, mode, key):
        """Determina qué grupo de funciones se van a usar según el foco actual.
        :param mode: string,
        :param key: string
        """
        if mode in self.functions[self.foco]:
            if key in self.functions[self.foco][mode]:
                self.functions[self.foco][mode][key]()

    def cambiar_foco(self, foco):
        """Cambia el foco de selección de un grupo a otro."""

        if foco == 'botones':
            for t in self.teclas:
                t.ser_deselegido()

            self.foco = 'botones'
            self.current = self.botones.get_sprite(0)
            self.current.ser_elegido()

        elif foco == 'teclas':
            self.movercursor(-1, 0)
            self.deselect_all(self.botones)
            self.foco = 'teclas'

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
                    bg = self.bg_cnvs
                else:
                    bg = self.bg_bisel_bg

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

            spr = Sprite()  # no hace falta una clase nueva para esto.
            fuente = font.SysFont('Verdana', 20)
            spr.image = fuente.render(key, 1, (0, 0, 0), self.bg_cnvs)
            spr.rect = spr.image.get_rect()
            spr.rect.bottom = espacio.top - 2
            spr.rect.centerx = espacio.centerx
            spr.key = key

            self.area_input.add(spr)
            self.ltr_idx += 1

            self.select_line(+1)

        if self.lin_idx == len(self.lineas):
            self.cambiar_foco('botones')

    def cancelar(self):
        if self.foco == 'teclas':
            self.erase_character()
        else:
            self.cambiar_foco('teclas')

    def erase_character(self):
        """Borra el caracter del espacio actualmente seleccionado"""

        if self.ltr_idx >= 0:
            self.canvas.fill(self.bg_cnvs, self.area_nombre)

            spr = self.area_input.get_sprite(self.ltr_idx)
            self.area_input.remove(spr)
            self.ltr_idx -= 1

            self.select_line(-1)

    def aceptar(self):
        name = ''.join([spr.key for spr in self.area_input])
        print(name)

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
                self.cambiar_foco('botones')  # el cursor busca el boton "aceptar"
            else:
                self.movercursor(-dx, -dy)  # deshacer el movimiento

    def select_line(self, delta):
        for linea in self.lineas:
            linea.isSelected = False
        self.lin_idx += delta
        if 0 <= self.lin_idx < len(self.lineas):
            self.lineas.get_sprite(self.lin_idx).isSelected = True

    @staticmethod
    def cargar_anims(ruta_imgs):
        dicc = {}
        spritesheet = Resources.split_spritesheet(ruta_imgs)
        idx = -1
        for L in ['S', 'I', 'D']:
            for D in ['abajo', 'arriba', 'izquierda', 'derecha']:
                key = L + D
                idx += 1
                dicc[key] = spritesheet[idx]

        return dicc

    def animar_sprite(self):
        """Cambia la imagen del sprite para mostrarlo animado"""

        self.timer_animacion += Tiempo.FPS.get_time()
        if self.timer_animacion >= 250:
            self.timer_animacion = 0
            if self._step == 'D':
                self._step = 'I'
            else:
                self._step = 'D'

            key = self._step + 'abajo'
            self.char_img = self.char_images[key]

    def update(self):
        self.animar_sprite()
        self.lineas.update()
        self.botones.update()

        if self.foco == 'teclas':
            for t in self.teclas:
                if t.rect.collidepoint(self.cursor.pos):
                    t.ser_elegido()
                    self.cursor.set_current(t)
                elif t.isSelected:
                    t.ser_deselegido()
        self.draw()

    def draw(self):
        self.canvas.fill(self.bg_cnvs, self.char_img_rect)
        self.canvas.blit(self.char_img, self.char_img_rect.topleft)
        self.teclas.draw(self.canvas)
        self.lineas.draw(self.canvas)
        self.botones.draw(self.canvas)
        self.area_input.draw(self.canvas)


class Character(BaseWidget):
    """Caracter individual del teclado en pantalla"""

    def __init__(self, char, bg, x, y):

        self.img_uns = self._crear_img(char, bg)
        self.img_sel = self.dibujar_seleccion(self.img_uns, self.font_high_color)

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
    animado = False
    """Estas son las líneas punteadas del nombre del personaje"""

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
    x, y = 0, 0
    current = None
    """Este es el cursor virtual que se desplaza en el teclado en pantalla"""

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

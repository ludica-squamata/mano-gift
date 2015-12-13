from engine.UI.Ventana import Ventana
from engine.globs import Constants as Cs, EngineData as Ed
from pygame.sprite import LayeredUpdates
from pygame import Surface, Rect
from engine.libs.textrect import render_textrect


class Menu(Ventana):
    botones = None
    keyup = {}
    cur_btn = 0
    current = ''
    canvas = None
    newMenu = False
    active = True
    ticks = 0

    def __init__(self, titulo):
        self.nombre = titulo
        # self.current = self
        self.canvas = self.create_raised_canvas(Cs.ANCHO - 20, Cs.ALTO - 20)
        self.crear_titulo(titulo, self.font_high_color, self.bg_cnvs, Cs.ANCHO - 20)
        self.funciones = {
            "arriba": lambda dummy: None,
            "abajo": lambda dummy: None,
            "izquierda": lambda dummy: None,
            "derecha": lambda dummy: None,
            "hablar": lambda: None}
        self.botones = LayeredUpdates()
        super().__init__(self.canvas)
        self.ubicar(10, 10)

        Ed.MENUS[titulo] = self

    def crear_titulo(self, titulo, fg_color, bg_color, ancho):
        ttl_rect = Rect((3, 3), (ancho - 7, 30))
        ttl_txt = render_textrect(titulo, self.fuente_Mu, ttl_rect, fg_color, bg_color, 1)
        self.canvas.blit(ttl_txt, ttl_rect.topleft)

    @staticmethod
    def deselect_all(lista):
        if len(lista) > 0:
            for item in lista:
                item.ser_deselegido()
                item.dirty = 1

    def mover_cursor(self, item):
        if item.tipo == 'boton':
            for i in range(len(self.botones)):
                spr = self.botones.get_sprite(i)
                if spr.nombre == item.nombre:
                    self.cur_btn = i
                    self.current = spr
                    break

        elif item.tipo == 'fila':
            for i in range(len(self.filas)):
                spr = self.filas.get_sprite(i)
                if item.nombre == spr.nombre:
                    self.cur_opt = i
                    self.current = spr
                    break

    def cancelar(self):
        """Esta funcion es un hook para otras funciones del mismo nombre."""
        self.active = False
        return True

    def usar_funcion(self, tecla):
        if tecla in ('arriba', 'abajo', 'izquierda', 'derecha'):
            self.funciones[tecla](tecla)
        else:
            self.funciones[tecla]()

    def keyup_function(self, tecla):
        if tecla in self.keyup:
            self.keyup[tecla]()

    def press_button(self):
        if len(self.botones) > 0:
            self.current.ser_presionado()

    def reset(self):
        """Resetea el estado de la ventana. Esta función es solo un hook."""
        self.active = True

    def __repr__(self):
        return 'Menu_' + self.nombre + ' (en ' + str(len(self.groups())) + ' grupos)'

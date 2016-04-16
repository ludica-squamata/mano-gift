from engine.UI.widgets import Ventana
from engine.globs import EngineData as Ed, ANCHO, ALTO
from pygame.sprite import LayeredUpdates
from pygame import Rect
from engine.libs.textrect import render_textrect


class Menu(Ventana):
    botones = None
    filas = None
    keyup = {}
    cur_btn = 0
    cur_opt = 0
    current = ''
    canvas = None
    newMenu = False
    active = True

    def __init__(self, titulo):
        self.nombre = titulo
        self.canvas = self.create_raised_canvas(ANCHO - 20, ALTO - 20)
        self.crear_titulo(titulo, self.font_high_color, self.bg_cnvs, ANCHO - 20)
        self.functions = {
            'tap': {
                'hablar': lambda: None,
                'cancelar': lambda: None,
                'arriba': lambda: None,
                'abajo': lambda: None,
                'izquierda': lambda: None,
                'derecha': lambda: None,
            },
            'hold': {
                'hablar': lambda: None,
                'cancelar': lambda: None,
                'arriba': lambda: None,
                'abajo': lambda: None,
                'izquierda': lambda: None,
                'derecha': lambda: None,
            },
            'release': {
                'hablar': lambda: None,
                'cancelar': lambda: None,
                'arriba': lambda: None,
                'abajo': lambda: None,
                'izquierda': lambda: None,
                'derecha': lambda: None,
            }
        }
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

    def use_function(self, mode, key):
        if key in self.functions[mode]:
            self.functions[mode][key]()

    def press_button(self):
        if len(self.botones) > 0:
            self.current.ser_presionado()
    
    def mantener_presion(self):
        self.current.mantener_presion()

    def liberar_presion(self):
        self.current.liberar_presion()

    def reset(self):
        """Resetea el estado de la ventana. Esta función es solo un hook."""
        self.active = True

    def __repr__(self):
        return 'Menu_' + self.nombre + ' (en ' + str(len(self.groups())) + ' grupos)'

from .menu import Menu
from engine.UI.widgets import Fila
from engine.globs import EngineData as Ed
from engine.libs import render_tagged_text
from pygame import sprite, Rect, Surface


class MenuItems(Menu):
    cur_opt = 0
    slots = [0 for i in range(10)]
    filas = sprite.LayeredUpdates()
    description_area = None
    altura_del_texto = 0  # altura de los glifos
    draw_space = None
    draw_space_rect = None

    def __init__(self):
        self.altura_del_texto = self.fuente_M.get_height() + 1
        super().__init__('Items')
        self.draw_space_rect = Rect((10, 44), (self.canvas.get_width() - 19, 270))
        self.draw_space = Surface(self.draw_space_rect.size)
        self.crear_contenido()
        self.crear_espacio_descriptivo((self.canvas.get_width() - 15), 93)
        self.functions.update({
            'tap':{
                'arriba': lambda: self.elegir_fila('arriba'),
                'abajo': lambda: self.elegir_fila('abajo')
            },
            'hold':{
                'arriba': lambda: self.elegir_fila('arriba'),
                'abajo': lambda: self.elegir_fila('abajo')
            }
        })

    def crear_contenido(self):
        self.actualizar_filas()

        if self.opciones > 0:
            self.elegir_fila()

    def actualizar_filas(self):
        h = self.altura_del_texto
        self.filas.empty()

        items = Ed.HERO.inventario()

        for i in range(len(items)):
            fila = Fila(items[i], self.draw_space_rect.w, 3, i * h + i)
            self.filas.add(fila)

        self.opciones = len(self.filas)
        self.filas.update()

    def crear_espacio_descriptivo(self, ancho, alto):
        marco = self.create_titled_canvas(ancho, alto, 'Efecto')
        rect = self.canvas.blit(marco, (7, 340))
        self.description_area = Rect((12, 363), (rect.w - 20, rect.h - 42))

    def elegir_fila(self, direccion = None):
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

    def update(self):
        self.draw_space.fill(self.bg_cnvs)
        self.crear_contenido()
        self.filas.draw(self.draw_space)
        self.canvas.blit(self.draw_space, self.draw_space_rect)
        if self.opciones > 0:
            desc = render_tagged_text(self.current.item.efecto_des,
                                      self.current.tags,
                                      self.description_area.w,
                                      bgcolor=self.bg_cnvs)
        else:
            desc = Surface(self.description_area.size)
            desc.fill(self.bg_cnvs)

        self.canvas.blit(desc, self.description_area.topleft)

from engine.globs import EngineData as Ed, ModData as Md, ANCHO, ALTO
from pygame.sprite import LayeredUpdates
from engine.UI.widgets import Fila
from .menu import Menu
import os


class MenuDebug(Menu):
    escenas = []
    draw_space = None
    draw_space_rect = None

    def __init__(self):
        super().__init__("Mano-Gift: Selector de Escenas")

        self.functions.update({
            'tap': {
                'hablar': self.cargar_escena,
                'arriba': lambda: self.elegir_opcion('arriba'),
                'abajo': lambda: self.elegir_opcion('abajo'),
            },
            'hold': {
                'arriba': lambda: self.elegir_opcion('arriba'),
                'abajo': lambda: self.elegir_opcion('abajo'),
            },
            'release': {
                'hablar': self.cargar_escena
            }
        })

        self.filas = LayeredUpdates()
        self.crear_espacio_de_escenas(ANCHO - 37, ALTO / 2.4)
        self.elegir_opcion(0)

    @staticmethod
    def cargar_escenas():
        ok = []
        for scn in os.listdir(Md.scenes):
            scn = scn.split('.')
            ok.append(scn[0])

        return ok

    def crear_espacio_de_escenas(self, ancho, alto):
        escenas = self.create_titled_canvas(ancho, alto, 'Elija una escena')
        rect = self.canvas.blit(escenas, (7, 40))
        self.draw_space = escenas.subsurface(((0, 0), (rect.w - 8, rect.h - 30)))
        self.draw_space.fill(self.bg_cnvs)
        self.draw_space_rect = escenas.get_rect(topleft=(11, 65))

        h = self.fuente_M.get_height() + 1
        self.escenas = self.cargar_escenas()  # lista
        self.opciones = len(self.escenas)
        for i in range(len(self.escenas)):
            opcion = Fila(self.escenas[i], self.draw_space_rect.w - 10, 0, i * h + i + 2)
            self.filas.add(opcion)

    def elegir_opcion(self, direccion):
        i = 0
        if direccion == 'arriba':
            i = -1
        elif direccion == 'abajo':
            i = +1
        self.deselect_all(self.filas)
        self.posicionar_cursor(i)
        elegido = self.filas.get_sprite(self.sel)
        elegido.ser_elegido()

    def cargar_escena(self):
        Ed.setear_escena(self.escenas[self.sel])
        Ed.onPause = False
        Ed.menu_previo = ''

    def update(self):
        self.filas.draw(self.draw_space)
        self.canvas.blit(self.draw_space, self.draw_space_rect)

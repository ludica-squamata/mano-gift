from engine.globs import EngineData, ANCHO, ALTO, SAVEFD
from pygame.sprite import LayeredUpdates
from engine.UI.widgets import Fila
from .menu import Menu
import os


class MenuCargar(Menu):
    archivos = []
    draw_space = None
    draw_space_rect = None

    def __init__(self):
        super().__init__("Cargar Partida")
        self.functions['tap'].update({
            'accion': self.cargar,
            'contextual': self.cancelar,
            'arriba': lambda: self.elegir_opcion('arriba'),
            'abajo': lambda: self.elegir_opcion('abajo')
        })
        self.functions['hold'].update({
            'arriba': lambda: self.elegir_opcion('arriba'),
            'abajo': lambda: self.elegir_opcion('abajo'),
        })
        self.functions['release'].update({
            'accion': self.cargar,
        })

        self.filas = LayeredUpdates()
        self.create_draw_space(ANCHO - 37, ALTO / 2.4)
        if len(self.filas):
            self.elegir_opcion(0)

    def use_function(self, mode, key):
        if len(self.filas):
            super().use_function(mode, key)

    @staticmethod
    def load_save_files():
        ok = []
        for file in os.listdir(SAVEFD):
            if file.endswith('.json') and file != 'config.json':
                ok.append(file.split('.')[0])

        return ok

    def create_draw_space(self, ancho, alto):
        archivos = self.create_titled_canvas(ancho, alto, 'Elija un archivo')
        rect = self.canvas.blit(archivos, (7, 40))
        self.draw_space = archivos.subsurface(((0, 0), (rect.w - 8, rect.h - 30)))
        self.draw_space.fill(self.bg_cnvs)
        self.draw_space_rect = archivos.get_rect(topleft=(11, 65))

        h = self.fuente_M.get_height() + 1
        self.archivos = self.load_save_files()  # lista
        self.opciones = len(self.archivos)
        for i in range(len(self.archivos)):
            opcion = Fila(self.archivos[i], self.draw_space_rect.w - 10, 0, i * h + i + 2)
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

    def cargar(self):
        EngineData.load_savefile(self.archivos[self.sel] + '.json')
        self.deregister()
        EngineData.end_dialog(self.layer)

    def update(self):
        self.filas.draw(self.draw_space)
        self.canvas.blit(self.draw_space, self.draw_space_rect)

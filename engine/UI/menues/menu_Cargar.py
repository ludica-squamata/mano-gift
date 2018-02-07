from engine.globs import EngineData, ANCHO, ALTO, SAVEFD
from pygame.sprite import LayeredUpdates
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
        self.create_draw_space('Elija un archivo', ANCHO - 16, ALTO / 2.4, 11, 65)
        self.llenar_espacio_selectivo()
        if len(self.filas):
            self.elegir_opcion(0)

    def use_function(self, mode, key):
        if len(self.filas):
            super().use_function(mode, key)

    def llenar_espacio_selectivo(self):
        self.archivos = [f.split('.')[0] for f in os.listdir(SAVEFD) if f.endswith('.json') and f != 'config.json']
        self.fill_draw_space(self.archivos, self.draw_space_rect.w, 21)

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

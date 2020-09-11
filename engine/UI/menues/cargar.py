from engine.globs.event_dispatcher import EventDispatcher
from engine.globs import EngineData, ANCHO, ALTO
from engine.globs.azoe_group import AzoeGroup
from engine.misc import Config
from .menu import Menu
import os

_boton_cargar = 'Cargar'


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
            'abajo': lambda: self.elegir_opcion('abajo'),
            'menu': self.cargar
        })
        self.functions['hold'].update({
            'arriba': lambda: self.elegir_opcion('arriba'),
            'abajo': lambda: self.elegir_opcion('abajo'),
        })
        self.functions['release'].update({
            'accion': self.cargar,
        })

        self.filas = AzoeGroup('Filas')
        self.create_draw_space('Elija un archivo', ANCHO - 16, ALTO / 2-6, 11, 65)
        self.llenar_espacio_selectivo()
        if len(self.filas):
            self.elegir_opcion(0)

    def llenar_espacio_selectivo(self):
        list_dir = os.listdir(Config.savedir)
        self.archivos = [f.split('.')[0] for f in list_dir if f.endswith('.json') and f != 'config.json']
        self.fill_draw_space(self.archivos, self.draw_space_rect.w, 21)

    def elegir_opcion(self, direccion):
        i = 0
        if direccion == 'arriba':
            i = -1
        elif direccion == 'abajo':
            i = +1
        self.deselect_all(self.filas)
        self.posicionar_cursor(i)
        if self.opciones > 0:
            elegido = self.filas.get_spr(self.sel)
            elegido.ser_elegido()
            if elegido.rect.y > self.draw_space_rect.h:
                for fila in self.filas:
                    fila.rect.y -= fila.rect.h
            elif elegido.rect.y < 0:
                for fila in self.filas:
                    fila.rect.y += fila.rect.h

    def cargar(self):
        if self.opciones > 0:
            EngineData.load_savefile(self.archivos[self.sel] + '.json')
            self.deregister()
            EventDispatcher.trigger('EndDialog', self, {'layer': self.layer})

    def update(self):
        self.filas.draw(self.draw_space)
        self.canvas.blit(self.draw_space, self.draw_space_rect)

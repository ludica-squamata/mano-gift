from engine.globs import ANCHO, ALTO, ModData, EngineData
from engine.globs.event_dispatcher import EventDispatcher
from engine.libs.mersenne_twister import choice
from engine.globs.azoe_group import AzoeGroup
from engine.misc import Config, abrir_json
from engine.UI.widgets import Fila
from .menu import Menu
import os


class MenuDebug(Menu):
    draw_space = None
    draw_space_rect = None

    def __init__(self, parent):
        self.mapas = []
        super().__init__(parent, 'debug', titulo="Mano-Gift: Selector de Escenas")

        self.functions.update({
            'tap': {
                'accion': self.elegir_mapa,
                'arriba': lambda: self.elegir_opcion('arriba'),
                'abajo': lambda: self.elegir_opcion('abajo'),
            },
            'hold': {
                'arriba': lambda: self.elegir_opcion('arriba'),
                'abajo': lambda: self.elegir_opcion('abajo'),
            }
        })

        self.filas = AzoeGroup('mapas')
        self.crear_espacio_de_mapas(ANCHO - 37, ALTO / 2.4)
        self.elegir_opcion(0)

    def elegir_mapa(self):
        player_name = [name.rstrip('.json') for name in os.listdir(ModData.fd_player)][0]
        selected = [fila for fila in self.filas.sprs() if fila.isSelected][0]
        ruta = os.path.join(Config.savedir, player_name + '.json')
        if os.path.exists(ruta):
            data = abrir_json(ruta)
            data['mapa'] = selected.item
            mapa = self.mapas[selected.item]
            data['entrada'] = choice(mapa['entradas'])
            data['use_csv'] = 'chunks_csv' in mapa or 'mobs_csv' in mapa

            EngineData.load_savefile(data)
            self.deregister()
            EventDispatcher.trigger('EndDialog', self, {'layer': self.layer})
        else:
            EventDispatcher.trigger('QUIT', self, {'status': "There's not such player in savedir"})

    def crear_espacio_de_mapas(self, ancho, alto):
        mapas = self.create_titled_canvas(ancho, alto, 'Elija un mapa')
        self.draw_space = mapas
        self.draw_space_rect = mapas.get_rect(topleft=(11, 65))

        h = 20
        self.mapas = self.filtrar_mapas()
        self.opciones = len(self.mapas)
        for i, mapa in enumerate(self.mapas):
            opcion = Fila(self, mapa.split('.')[0], self.draw_space_rect.w - 10, 3, i * h + i + 24)
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

    @staticmethod
    def filtrar_mapas():
        all_maps = [mapa for mapa in os.listdir(ModData.mapas) if '.stage' in mapa]
        mapas = {mapa.split('.')[0]: abrir_json(os.path.join(ModData.mapas, mapa)) for mapa in all_maps}
        return mapas

    def update(self):
        self.filas.draw(self.draw_space)
        self.canvas.blit(self.draw_space, self.draw_space_rect)

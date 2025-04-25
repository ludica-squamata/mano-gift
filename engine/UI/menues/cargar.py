from engine.globs import EngineData, ANCHO, ALTO, CANVAS_BG
from engine.globs.event_dispatcher import EventDispatcher
from engine.globs.azoe_group import AzoeGroup
from engine.misc import Config
from .menu import Menu
import os


class MenuCargar(Menu):
    archivos = []
    draw_space = None
    draw_space_rect = None

    def __init__(self, parent):
        super().__init__(parent, "Cargar Partida")
        self.functions['tap'].update({
            'accion': self.press_button,
            'contextual': self.cancelar,
            'arriba': lambda: self.direccionar('arriba'),
            'abajo': lambda: self.direccionar('abajo'),
            'izquierda': lambda: self.direccionar('izquierda'),
            'derecha': lambda: self.direccionar('derecha'),
            'menu': self.cargar
        })
        self.functions['hold'].update({
            'arriba': lambda: self.direccionar('arriba'),
            'abajo': lambda: self.direccionar('abajo'),
            'izquierda': lambda: self.direccionar('izquierda'),
            'derecha': lambda: self.direccionar('derecha'),
        })

        self.filas = AzoeGroup('Filas')
        self.create_draw_space('Elija un archivo', 11, 65, ANCHO - 16, ALTO / 2 - 6)
        self.llenar_espacio_selectivo()
        if len(self.filas):
            self.elegir_opcion(0)

        n, d, c, e = 'nombre', 'direcciones', 'comando', self.draw_space_rect
        botones = [
            {n: 'Cargar', d: {'derecha': 'Borrar'}, c: self.cargar, 'pos': [e.centerx - 180, e.bottom + 20]},
            {n: 'Borrar', d: {'izquierda': 'Cargar'}, c: self.eliminar, 'pos': [e.centerx + 20, e.bottom + 20]}
        ]
        self.establecer_botones(botones, 5)

    def llenar_espacio_selectivo(self):
        list_dir = os.listdir(Config.savedir)
        self.archivos = [f.split('.')[0] for f in list_dir if f.endswith('.json') and f != 'config.json']
        self.fill_draw_space(self.archivos, self.draw_space_rect.w, 21)

    def direccionar(self, direccion):
        if direccion in ('arriba', 'abajo'):
            self.elegir_opcion(direccion)
        elif direccion in ('derecha', 'izquierda'):
            self.select_one(direccion)

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
            EventDispatcher.trigger('OpenMenu', self.nombre, {'value': 'Loading'})

    def eliminar(self):
        current = self.archivos[self.sel] + '.json'
        ruta = os.path.join(os.getcwd(), 'save', current)
        os.remove(ruta)
        spr = self.filas.get_sprite(self.sel)
        spr.kill()
        self.opciones -= 1
        if len(self.filas):
            self.elegir_opcion(0)

    def update(self):
        self.draw_space.fill(CANVAS_BG)
        self.filas.draw(self.draw_space)
        self.botones.update()
        self.botones.draw(self.canvas)
        self.canvas.blit(self.draw_space, self.draw_space_rect)

from .RenderedCircularMenu import RenderedCircularMenu
from .RenderedCircularMenu import RenderedCircularMenu, LetterElement, Title
from engine.IO.menucircular import CircularMenu
from engine.globs import EngineData as Ed, CAPA_OVERLAYS_INVENTARIO
from engine.globs.eventDispatcher import EventDispatcher
from .elements import CommandElement, InventoryElement


class QuickCircularMenu(RenderedCircularMenu):
    radius = 15
    layer = CAPA_OVERLAYS_INVENTARIO

    def __init__(self, first, opciones=None):
        n, c, i, cmd, j = 'name', 'csc', 'icon', 'cmd', 'idx'

        if opciones is None:
            opciones = [
                {j: 0, n: 'Estado', cmd: Ed.HERO.cambiar_estado, i: 'S'},
                {j: 1, n: 'Guardar', i: 'G', cmd: lambda: EventDispatcher.trigger('Save', 'Menu Rápido', {})},
                {j: 2, n: 'Consumibles', c: Ed.HERO.inventario('consumible'), i: 'C'},
                {j: 3, n: 'Equipables', c: Ed.HERO.inventario('equipable'), i: 'E'}
            ]

        cascadas = {'inicial': []}
        for opt in [opciones[first]] + opciones[first + 1:] + opciones[:first]:
            if 'cmd' in opt:
                obj = CommandElement(self, opt)
            else:
                obj = InventoryElement(self, opt)
            obj.idx = opt['idx']
            cascadas['inicial'].append(obj)
            cascadas[obj.nombre] = obj.cascada

        super().__init__(cascadas)
        self.functions['tap'].update({'inventario': self.back})

    def back(self):
        if self.cascadaActual == 'inicial':
            self.salir()
        else:
            super().back()

    def stop_everything(self, on_spot):
        super().stop_everything(on_spot)
        Ed.current_qcm_idx = self.last_on_spot.idx

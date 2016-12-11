from engine.globs import EngineData as Ed, CAPA_OVERLAYS_INVENTARIO
from engine.globs.eventDispatcher import EventDispatcher
from .RenderedCircularMenu import RenderedCircularMenu
from .elements import CommandElement, InventoryElement, CascadeElement


class QuickCircularMenu(RenderedCircularMenu):
    radius = 18
    layer = CAPA_OVERLAYS_INVENTARIO

    def __init__(self, first, opciones=None):
        n, c, i, cmd, j = 'name', 'csc', 'icon', 'cmd', 'idx'
        cascadas = {
            "rotar_vista": [
                {n: 'Norte', i: "N", cmd: lambda: EventDispatcher.trigger('Rotar', 'Menu Rápido', {'vista': 'norte'})},
                {n: "Este", i: "E", cmd: lambda: EventDispatcher.trigger('Rotar', 'Menu Rápido', {'vista': 'este'})},
                {n: "Sur", i: "S", cmd: lambda: EventDispatcher.trigger('Rotar', 'Menu Rápido', {'vista': 'sur'})},
                {n: "Oeste", i: "O", cmd: lambda: EventDispatcher.trigger('Rotar', 'Menu Rápido', {'vista': 'oeste'})},
            ]
        }

        if opciones is None:
            opciones = [
                {j: 0, n: 'Estado', cmd: Ed.HERO.cambiar_estado, i: 'S'},
                {j: 1, n: 'Guardar', i: 'G', cmd: lambda: EventDispatcher.trigger('Save', 'Menu Rápido', {})},
                {j: 2, n: 'Consumibles', c: Ed.HERO.inventario('consumible'), i: 'C'},
                {j: 3, n: 'Equipables', c: Ed.HERO.inventario('equipable'), i: 'E'},
                {j: 4, n: 'Rotar Vista', c: cascadas['rotar_vista'], i: "R"}
            ]

        cascadas = {'inicial': []}
        for opt in [opciones[first]] + opciones[first + 1:] + opciones[:first]:
            if type(opt) is dict:
                if 'csc' in opt:
                    obj = CascadeElement(self, opt)
                elif 'cmd' in opt:
                    obj = CommandElement(self, opt)
            elif hasattr(opt, "nombre"):
                obj = InventoryElement(self, opt)

            obj.idx = opt['idx']
            cascadas['inicial'].append(obj)
            cascadas[obj.nombre] = obj.cascada

        super().__init__(cascadas)
        self.functions['tap'].update({'contextual': self.back})

    def back(self):
        if self.cascadaActual == 'inicial':
            self.salir()
        else:
            super().back()

    def stop_everything(self, on_spot):
        super().stop_everything(on_spot)
        Ed.current_qcm_idx = self.last_on_spot.idx

from engine.globs import EngineData as Ed, CAPA_OVERLAYS_INVENTARIO, FEATURE_ROTACION_MAPA
from engine.globs.eventDispatcher import EventDispatcher
from .RenderedCircularMenu import RenderedCircularMenu
from .elements import CommandElement, CascadeElement


class QuickCircularMenu(RenderedCircularMenu):
    radius = 18
    layer = CAPA_OVERLAYS_INVENTARIO

    def __init__(self, first, opciones=None):
        n, c, i, cmd, j = 'name', 'csc', 'icon', 'cmd', 'idx'
        cascadas = {
            "rotar_vista": [
                {n: 'Norte', i: "N", cmd: lambda: self.cmd_rotar_vista('north')},
                {n: "Este", i: "E", cmd: lambda: self.cmd_rotar_vista('east')},
                {n: "Sur", i: "S", cmd: lambda: self.cmd_rotar_vista('south')},
                {n: "Oeste", i: "O", cmd: lambda: self.cmd_rotar_vista('west')},
            ]
        }

        if opciones is None:
            opciones = [
                {j: 0, n: 'Estado', cmd: Ed.HERO.cambiar_estado, i: 'S'},
                {j: 1, n: 'Guardar', i: 'G', cmd: lambda: EventDispatcher.trigger('Save', 'Menu Rápido', {})},
                {j: 2, n: 'Consumibles', c: Ed.HERO.inventario('consumible'), i: 'C'},
                {j: 3, n: 'Equipables', c: Ed.HERO.inventario('equipable'), i: 'E'},
            ]

        if FEATURE_ROTACION_MAPA:
            opciones.append({j: 4, n: 'Rotar Vista', c: cascadas['rotar_vista'], i: "R"})

        cascadas = {'inicial': []}
        for opt in [opciones[first]] + opciones[first + 1:] + opciones[:first]:
            if type(opt) is dict:
                if 'csc' in opt:
                    obj = CascadeElement(self, opt)
                elif 'cmd' in opt:
                    obj = CommandElement(self, opt)

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

    @staticmethod
    def cmd_rotar_vista(direccion):
        # solo una abreviatura

        EventDispatcher.trigger('Rotate', 'Menu Rápido', {'view': direccion})

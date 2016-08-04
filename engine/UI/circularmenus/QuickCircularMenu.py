from .RenderedCircularMenu import RenderedCircularMenu, LetterElement, Title
from engine.IO.menucircular import CircularMenu
from engine.globs import EngineData as Ed, CAPA_OVERLAYS_INVENTARIO
from engine.globs.eventDispatcher import EventDispatcher


class InventoryElement(LetterElement):
    active = True
    item = None

    def __init__(self, parent, item):

        if type(item) is dict:
            nombre = item['name']
            icono = item['icon']
            cascada = item.get('csc')
            self.item = None
        else:
            nombre = item.nombre
            icono = item.image
            cascada = None
            self.item = item

        super().__init__(parent, nombre)

        if type(icono) is str:
            self.img_uns = self._crear_icono_texto(icono, 21, 21)
            self.img_sel = self._crear_icono_texto(icono, 33, 33)
        else:
            self.img_uns = self._crear_icono_image(21, 21)
            self.img_sel = self._crear_icono_image(33, 33)

        self.rect_uns = self.img_uns.get_rect()
        self.rect_sel = self.img_sel.get_rect()

        if self.in_place:
            self.image = self.img_sel
            self.rect = self.rect_sel
        else:
            self.image = self.img_uns
            self.rect = self.rect_uns
        self.title = Title(self, nombre)

        if cascada is not None:
            for j in range(len(cascada)):
                obj = InventoryElement(self.parent, cascada[j])
                obj.idx = j
                self.cascada.append(obj)

    def _crear_icono_image(self, w, h):
        image, _rect = self._crear_base(w, h)
        cant = Ed.HERO.inventario.cantidad(self.item)
        render = self.fuente_MP.render(str(cant), 1, self.font_none_color)
        renderect = render.get_rect(bottomright=_rect.bottomright)
        iconrect = self.item.image.get_rect(center=_rect.center)

        image.blit(self.item.image, iconrect)
        image.blit(render, renderect)

        return image

    def do_action(self):
        if self.item is not None:
            if hasattr(self.item, 'usar'):
                value = Ed.HERO.usar_item(self.item)
                self.img_uns = self._crear_icono_image(21, 21)
                self.img_sel = self._crear_icono_image(33, 33)
                self.image = self.img_sel
                return value
        return True


class CommandElement(LetterElement):
    active = True
    item = None

    def __init__(self, parent, item):

        nombre = item['name']
        icono = item['icon']
        self.command = item['cmd']

        super().__init__(parent, nombre)

        self.img_uns = self._crear_icono_texto(icono, 21, 21)
        self.img_sel = self._crear_icono_texto(icono, 33, 33)

        self.rect_uns = self.img_uns.get_rect()
        self.rect_sel = self.img_sel.get_rect()

        if self.in_place:
            self.image = self.img_sel
            self.rect = self.rect_sel
        else:
            self.image = self.img_uns
            self.rect = self.rect_uns
        self.title = Title(self, nombre)

    def do_action(self):
        self.command()
        self.parent.back()
        return True


class QuickCircularMenu(RenderedCircularMenu, CircularMenu):
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

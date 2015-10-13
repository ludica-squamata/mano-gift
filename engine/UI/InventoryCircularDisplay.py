from engine.IO.menucircular import CircularMenu, BaseElement
from engine.globs import EngineData as Ed, Constants as Cs
from pygame import font, Surface, SRCALPHA


class InventoryElement(BaseElement):
    active = True
    item = None

    def __init__(self, parent, item):

        if type(item) is dict:
            nombre = item['nombre']
            icono = item['icono']
            cascada = item.get('cascada')
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
            self.img_uns = self._crear_icono_image(icono, 21, 21)
            self.img_sel = self._crear_icono_image(icono, 33, 33)

        self.rect_uns = self.img_uns.get_rect()
        self.rect_sel = self.img_sel.get_rect()

        if self.in_place:
            self.image = self.img_sel
            self.rect = self.rect_sel
        else:
            self.image = self.img_uns
            self.rect = self.rect_uns

        if cascada is not None:
            for item in cascada:
                    self.cascada.append(InventoryElement(self.parent, item))

    @staticmethod
    def _crear_base(w, h):
        image = Surface((w, h), SRCALPHA)
        image.fill((125, 125, 125, 200))
        rect = image.get_rect()
        return image, rect

    def _crear_icono_texto(self, icono, w, h):
        image, _rect = self._crear_base(w, h)

        fuente = font.SysFont('Verdana', 15, bold = True)
        render = fuente.render(icono, 1, (0, 0, 0))
        renderect = render.get_rect(center = _rect.center)
        image.blit(render, renderect)
        return image

    def _crear_icono_image(self, icono, w, h):
        image, _rect = self._crear_base(w, h)
        fuente = font.SysFont('Verdana', 12)
        cant = Ed.HERO.inventario.cantidad(self.item)
        render = fuente.render(str(cant), 1, (0, 0, 0))
        renderect = render.get_rect(bottomright = _rect.bottomright)
        iconrect = icono.get_rect(center = _rect.center)

        image.blit(icono, iconrect)
        image.blit(render, renderect)

        return image

    def do_action(self):
        if self.item is not None:
            if hasattr(self.item, 'usar'):
                return Ed.HERO.usar_item(self.item)
        return True

    def update(self):
        super().update()
        if self.item is not None:
            self.img_uns = self._crear_icono_image(self.item.image, 21, 21)
            self.img_sel = self._crear_icono_image(self.item.image, 33, 33)


class InventoryCircularDisplay(CircularMenu):
    radius = 20

    def __init__(self):
        cx, cy = Ed.RENDERER.camara.rect.center
        n, c, i = 'nombre', 'cascada', 'icono'

        opciones = [
            {n: 'Consumibles', c: Ed.HERO.inventario('consumible'), i: 'C'},
            {n: 'Equipables', c: Ed.HERO.inventario('equipable'), i: 'E'}
        ]

        cascadas = {'inicial': []}
        for opt in opciones:
            obj = InventoryElement(self, opt)
            Ed.RENDERER.addOverlay(obj, Cs.CAPA_OVERLAYS_INVENTARIO)
            cascadas['inicial'].append(obj)
            cascadas[obj.nombre] = obj.cascada

        super().__init__(cascadas, cx, cy)

    def _change_cube_list(self):
        super()._change_cube_list()
        Ed.RENDERER.overlays.remove_sprites_of_layer(Cs.CAPA_OVERLAYS_INVENTARIO)
        for cuadro in self.cubos:
            Ed.RENDERER.addOverlay(cuadro, Cs.CAPA_OVERLAYS_INVENTARIO)

    def supress(self):
        super().supress()
        Ed.RENDERER.overlays.remove_sprites_of_layer(Cs.CAPA_OVERLAYS_INVENTARIO)
        for cuadro in self.cubos:
            Ed.RENDERER.addOverlay(cuadro, Cs.CAPA_OVERLAYS_INVENTARIO)

    def _modify_cube_list(self):
        super()._modify_cube_list()
        Ed.RENDERER.overlays.remove_sprites_of_layer(Cs.CAPA_OVERLAYS_INVENTARIO)
        for cuadro in self.cubos:
            Ed.RENDERER.addOverlay(cuadro, Cs.CAPA_OVERLAYS_INVENTARIO)

    def back(self):
        if self.cascadaActual == 'inicial':
            Ed.RENDERER.overlays.remove_sprites_of_layer(Cs.CAPA_OVERLAYS_INVENTARIO)
            Ed.DIALOGO = None
            Ed.MODO = 'Aventura'
        else:
            super().back()

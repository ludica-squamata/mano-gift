from .RenderedCircularMenu import RenderedCircularMenu, LetterElement
from engine.IO.menucircular import CircularMenu
from engine.globs import MobGroup, ItemGroup, Constants as Cs


class DialogElement(LetterElement):
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
                self.cascada.append(DialogElement(self.parent, item))

    def _crear_icono_image(self, icono, w, h):
        image, _rect = self._crear_base(w, h)
        iconrect = icono.get_rect(center=_rect.center)
        image.blit(icono, iconrect)

        return image

    def do_action(self):
        return True

    def update(self):
        super().update()
        if self.item is not None:
            self.img_uns = self._crear_icono_image(self.item.image, 21, 21)
            self.img_sel = self._crear_icono_image(self.item.image, 33, 33)

        if self.in_place:
            self.image = self.img_sel
            self.rect = self.rect_sel
        else:
            self.image = self.img_uns
            self.rect = self.rect_uns


class DialogCircularMenu(RenderedCircularMenu, CircularMenu):
    radius = 20
    layer = Cs.CAPA_OVERLAYS_DIALOGOS

    def __init__(self):
        n, c, i, = 'nombre', 'cascada', 'icono'

        opciones = [
            {n: 'Mobs', c: MobGroup.contents(), i: 'M'},
            {n: 'Props', c: ItemGroup.contents(), i: 'P'}
        ]

        cascadas = {'inicial': []}
        for opt in opciones:
            obj = DialogElement(self, opt)
            cascadas['inicial'].append(obj)
            cascadas[obj.nombre] = obj.cascada

        super().__init__(cascadas)
        self.show()
        # self.functions['tap'].update({'inventario': self.back})

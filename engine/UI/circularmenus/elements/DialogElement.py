from engine.IO.dialogo import Dialogo
from .LetterElement import LetterElement
from engine.misc import Resources as Rs
from engine.globs import EngineData as Ed


class DialogElement(LetterElement):
    active = True
    item = None

    def __init__(self, parent, item):
        self.item = None

        if 'cascada' in item:
            nombre = item['nombre']
            icono = item['icono']
            cascada = item.get('cascada')
            self.item = None

        elif 'head' in item:
            data = item['head']
            nombre = data['name']
            if data['icon']:
                icono = Rs.cargar_imagen(data['icon'])
            else:
                icono = nombre[0].upper()
            cascada = None
            self.item = item

        else:
            nombre = item['name']
            icono = item['icon']
            cascada = None
            self.item = item['item']

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
        if self.item is not None:
            # self.parent.salir()
            if Dialogo.pre_init(self.item['head'], *self.parent.locutores):
                self.parent.supress_all()
                Ed.DIALOG = Dialogo(self.item['body'], *self.parent.locutores)
                Ed.DIALOG.frontend.set_menu(self.parent)
                Ed.MODO = 'Dialogo'
            else:
                self.parent.cerrar()

        return True

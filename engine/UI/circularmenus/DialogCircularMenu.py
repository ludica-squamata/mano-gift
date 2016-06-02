from engine.globs import MobGroup, ItemGroup, EngineData as Ed, CAPA_OVERLAYS_DIALOGOS, ModData
from .RenderedCircularMenu import RenderedCircularMenu, LetterElement
from engine.IO.menucircular import CircularMenu
from engine.IO.dialogo import Dialogo
from os import path, listdir
from engine.misc import Resources as Rs

class DialogElement(LetterElement):
    active = True
    item = None

    def __init__(self, parent, item):

        if 'cascada' in item:
            nombre = item['nombre']
            icono = item['icono']
            cascada = item.get('cascada')
            self.item = None
        else:
            data = item['head']
            nombre = data['name']
            if data['icon']:
                icono = Rs.cargar_imagen(data['icon'])
            else:
                icono = nombre[0].upper()
            cascada = None
            self.item = item

        super().__init__(parent, nombre)

        if type(icono) is str:
            self.img_uns = self._crear_icono_texto(icono, 33, 33)
            self.img_sel = self._crear_icono_texto(icono, 40, 40)
        else:
            self.img_uns = self._crear_icono_image(icono, 33, 33)
            self.img_sel = self._crear_icono_image(icono, 40, 40)

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
            self.parent.salir()
            if Dialogo.pre_init(self.item['head'], *self.parent.locutores):
                Ed.DIALOG = Dialogo(self.item['body'], *self.parent.locutores)
                Ed.MODO = 'Dialogo'
            else:
                for mob in self.parent.locutores:
                    mob.hablando = False
                Ed.MODO = 'Aventura'

        return True

    def update(self):
        super().update()
        if self.in_place:
            self.image = self.img_sel
            self.rect = self.rect_sel
        else:
            self.image = self.img_uns
            self.rect = self.rect_uns


class DialogCircularMenu(RenderedCircularMenu, CircularMenu):
    radius = 20
    layer = CAPA_OVERLAYS_DIALOGOS

    def __init__(self, *locutores):
        n, c, i, = 'nombre', 'cascada', 'icono'
        self.locutores = locutores

        opciones = []
        for script in listdir(ModData.dialogos):
            ruta = ModData.dialogos + script
            if path.isfile(ruta):
                file = Rs.abrir_json(ruta)
                if file['head']['class'] == 'chosen':
                        opciones.append(file)

        cascadas = {'inicial': []}
        for opt in opciones:
            obj = DialogElement(self, opt)
            cascadas['inicial'].append(obj)

        super().__init__(cascadas)
        self.show()
        # self.functions['tap'].update({'inventario': self.back})

    def salir(self):
        self.cascadaActual = 'inicial'
        super().salir()

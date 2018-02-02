from .LetterElement import LetterElement
from engine.IO.dialogo import Dialogo
from engine.globs import EngineData
from engine.misc.resources import cargar_imagen


class TopicElement(LetterElement):
    active = True
    item = None

    def __init__(self, parent, item):
        data = item['head']
        nombre = data['name']
        if data['icon']:
            icono = cargar_imagen(data['icon'])
        else:
            icono = nombre[0].upper()
        self.item = item

        super().__init__(parent, nombre, icono)

    def do_action(self):
        if self.active:
            if Dialogo.pre_init(self.item['head'], *self.parent.locutores):
                self.parent.supress_all()
                dialogo = Dialogo(self.item, *self.parent.locutores)
                dialogo.frontend.set_menu(self.parent)
                EngineData.MODO = 'Dialogo'
                self.active = False
                self.parent.deregister()
            else:
                self.parent.cerrar()
        return True


class DialogOptionElement(LetterElement):
    active = True
    item = None

    def __init__(self, parent, item):

        nombre = item['name']
        icono = item['icon']
        self.item = item['item']

        super().__init__(parent, nombre, icono)

    def do_action(self):
        return True

from engine.globs import ModData
from .letter import LetterElement
from .descriptive_area import DescriptiveArea
from engine.misc.resources import cargar_imagen


class BranchElement(LetterElement):
    active = True
    item = None

    def __init__(self, parent, item):
        """Elemento para las opciones de un branch."""
        nombre = item['name']
        icono = item['icon']
        self.item = item['item']
        self.idx = item['idx']

        super().__init__(parent, nombre, icono, do_title=False)


class DialogObjectElement(LetterElement):
    active = True
    item = None
    idx = 0

    def __init__(self, parent, idx, item):
        """Elemento para mostrar ítems en un diálogo"""
        self.item = item
        self.idx = idx
        self.img_uns = self._create(21, 21)
        self.img_sel = self._create(33, 33)

        super().__init__(parent, self.item.nombre, None)

    def _create(self, w, h):
        image, _rect = self._crear_base(w, h)
        iconrect = self.item.image.get_rect(center=_rect.center)
        image.blit(self.item.image, iconrect)

        return image

    def do_action(self):
        pass


class DialogThemeElement(LetterElement):
    active = True
    item = None
    idx = 0

    def __init__(self, parent, idx, item):
        """Elemento para cambiar de tema en un diálogo"""
        image = cargar_imagen(ModData.graphs + 'themeglob left mini.png')
        self.item = item
        self.idx = idx

        super().__init__(parent, self.item, image)

    def do_action(self):
        pass


class DialogTopicElement(DialogThemeElement):

    def __init__(self, parent, idx, item):
        super().__init__(parent, idx, item)
        # Esta descripción es un placeholder. Debería haber algún lugar donde se ubicara la info sobre el topic.
        self.description = DescriptiveArea(self, 'Sabes sobre {}'.format(self.item.title()))

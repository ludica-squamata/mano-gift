from engine.globs.event_dispatcher import EventDispatcher
from .descriptive_area import DescriptiveArea
from .letter import LetterElement
from engine.globs import TEXT_FG
from pygame import font


class InventoryElement(LetterElement):
    active = True
    item = None
    description = None
    idx = 0

    def __init__(self, parent, item):

        self.item = item
        self.img_uns = self._create_icon_stack(21, 21, False, parent.entity)
        self.img_sel = self._create_icon_stack(33, 33, True, parent.entity)

        super().__init__(parent, self.item.nombre, None)
        self.description = DescriptiveArea(self, item.efecto_des)

    def _create_icon_stack(self, w, h, count, entity):
        image, _rect = self._crear_base(w, h)
        if count:
            fuente = font.Font('engine/libs/Verdana.ttf', 12)
            cant = entity.inventario.cantidad(self.item)
            render = fuente.render(str(cant), True, TEXT_FG)
            renderect = render.get_rect(bottom=_rect.bottom + 1, right=_rect.right - 1)
            image.blit(render, renderect)

        iconrect = self.item.image.get_rect(center=_rect.center)
        image.blit(self.item.image, iconrect)

        return image

    def command(self):
        if self.item is not None and self.item.tipo == 'consumible':
            value = self.item.usar(self.parent.entity)
            self.img_sel = self._create_icon_stack(33, 33, True, self.parent.entity)
            self.image = self.img_sel
            if value == 0:
                self.parent.del_item_from_cascade(self.nombre, 'Consumibles')
        elif self.item.tipo == 'equipable':
            self.parent.overwritten = True
            self.parent.salir()
            EventDispatcher.trigger('OpenMenu', 'Item', {'value': 'Equipo', "select": self.item.espacio})

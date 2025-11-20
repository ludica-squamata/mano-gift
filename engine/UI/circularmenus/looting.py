from .elements.descriptive_area import DescriptiveArea
from engine.libs import render_tagged_text
from .rendered import RenderedCircularMenu
from .elements import LetterElement


class LootingCircularMenu(RenderedCircularMenu):
    def __init__(self, parent, mob):
        self.name = "looting"
        self.parent = parent

        lootable = mob.inventario.uniques()
        cantidades = [mob.inventario.cantidad(item) for item in lootable]

        cascadas = {
            "inicial": [LooteableElement(self, lootable[i], cantidades[i]) for i in range(len(lootable))]
        }

        super().__init__(cascadas)


class LooteableElement(LetterElement):
    def __init__(self, parent, item, cantidad):
        self.item = item
        # self.action = action
        self.cantidad = cantidad
        self.cantidad_inicial = cantidad
        super().__init__(parent, item.nombre, item.image.copy(), do_title=True)
        self.description = DescriptiveArea(self, description=item.efecto_des)

        # self.functions['hold'].update({
        #     'accion': self.increment
        # })
        # self.functions['release'].update({
        #     'accion': self.confirm
        # })

        # self.register()
        self.ticks = 0

    def mostrar_cantidad(self):
        img_cant = render_tagged_text("<sn>" + str(self.cantidad) + "</sn>", self.w, justification=2)
        rect = img_cant.get_rect(right=33, bottom=33)

        imagen = self._crear_icono_image(self.item.image.copy(), 33, 33)
        imagen.blit(img_cant, rect)

        self.img_sel = imagen
        self.image = self.img_sel

    def update(self):
        super().update()
        if self.selected:
            self.mostrar_cantidad()
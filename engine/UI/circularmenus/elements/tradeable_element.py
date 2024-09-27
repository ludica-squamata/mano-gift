# from engine.globs.event_dispatcher import EventDispatcher
from .letter import LetterElement
from .descriptive_area import DescriptiveArea
from engine.libs import render_tagged_text


class TradeableElement(LetterElement):
    price = ''

    def __init__(self, parent, action, item, cantidad):
        self.item = item
        self.price = action + '_price'
        self.cantidad = cantidad
        super().__init__(parent, item.nombre, item.image, do_title=True)
        self.description = DescriptiveArea(self, description=item.efecto_des)
        self.mostrar_cantidad()

    def mostrar_cantidad(self):
        img_cant = render_tagged_text("<sn>" + str(self.cantidad) + "</sn>", self.w, justification=2)
        rect = img_cant.get_rect(right=self.rect.right, bottom=self.rect.bottom)
        self.image.blit(img_cant, rect)

    def do_action(self):
        node = self.parent.parent
        arbol = node.parent

        next_node = arbol[int(node.leads)]
        coin = self.item.data['trading']['coin_symbol']
        price = self.item.data['trading'][self.price]
        text = next_node.texto
        new_text = text.format(coin=coin, price=str(price))
        arbol[int(node.leads)] = new_text

        dialogo = arbol.parent
        dialogo.frontend.set_text(new_text)
        dialogo.frontend.show()
        dialogo.frontend.update()
        self.parent.salir()

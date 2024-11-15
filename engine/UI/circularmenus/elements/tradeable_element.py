from .letter import LetterElement
from .descriptive_area import DescriptiveArea
from engine.libs import render_tagged_text


class TradeableElement(LetterElement):

    def __init__(self, parent, action, item, cantidad):
        self.item = item
        self.action = action
        self.cantidad = cantidad
        super().__init__(parent, item.nombre, item.image, do_title=True)
        self.description = DescriptiveArea(self, description=item.efecto_des)
        cant_img, cant_rect = self.mostrar_cantidad()
        self.image.blit(cant_img, cant_rect)

    def mostrar_cantidad(self):
        img_cant = render_tagged_text("<sn>" + str(self.cantidad) + "</sn>", self.w, justification=2)
        rect = img_cant.get_rect(right=self.rect.right, bottom=self.rect.bottom)
        return img_cant, rect

    def do_action(self):
        node = self.parent.parent
        arbol = node.parent
        dialogo = arbol.parent

        coin = self.item.coin
        if coin is not None:
            next_node = arbol[int(node.leads)]
            text = next_node.texto
            price = self.item.price_sell if self.action == 'sell' else self.item.price_buy
            new_text = text.format(coin=coin, price=str(price))
            arbol[int(node.leads)] = new_text
            # self.cantidad -= 1
            dialogo.mostrar_nodo(next_node)
        else:
            # this clause covers un sellable items (like key items in other games)
            # and outdated item.json that don't have the proper keys set.
            next_node = arbol[dialogo.wont_buy]
            arbol.set_actual(next_node)
            dialogo.hablar()

        dialogo.frontend.show(False)
        self.parent.salir()

    def update(self):
        self.image.blit(*self.mostrar_cantidad())
        super().update()

from .letter import LetterElement
from .descriptive_area import DescriptiveArea
from engine.libs import render_tagged_text


class TradeableElement(LetterElement):

    def __init__(self, parent, action, item, cantidad):
        self.item = item
        self.action = action
        self.cantidad = cantidad
        self.cantidad_inicial = cantidad
        super().__init__(parent, item.nombre, item.image.copy(), do_title=True)
        self.description = DescriptiveArea(self, description=item.efecto_des)

        self.functions['hold'].update({
            'accion': self.increment
        })
        self.functions['release'].update({
            'accion': self.confirm
        })

        self.register()
        self.ticks = 0

    def mostrar_cantidad(self):
        img_cant = render_tagged_text("<sn>" + str(self.cantidad) + "</sn>", self.w, justification=2)
        rect = img_cant.get_rect(right=33, bottom=33)

        imagen = self._crear_icono_image(self.item.image.copy(), 33, 33)
        imagen.blit(img_cant, rect)

        self.img_sel = imagen
        self.image = self.img_sel

    def do_action(self):
        node = self.parent.parent
        arbol = node.parent
        dialogo = arbol.parent

        coin = self.item.coin
        if coin is not None:
            next_node = arbol[int(node.leads)]
            text = next_node.texto
            price = self.item.price_sell if self.action == 'sell' else self.item.price_buy
            precio = price * abs(self.cantidad - self.cantidad_inicial)
            if precio == 0:  # user tapped, meaning he wants only one item.
                delta = 1
                costo = price
            else:  # user held action key, increasng the size of the bulk.
                delta = abs(self.cantidad - self.cantidad_inicial)
                costo = precio
            self.parent.trade.set_delta(delta)
            new_text = text.format(coin=coin, price=str(costo))
            arbol[int(node.leads)] = new_text
            dialogo.mostrar_nodo(next_node)
        else:
            # this clause covers unsellable items (like key items in other games)
            # and outdated item.json that don't have the proper keys set.
            next_node = arbol[dialogo.wont_buy]
            arbol.set_actual(next_node)
            dialogo.hablar()

        dialogo.frontend.show(False)
        self.parent.salir()

    def update(self):
        super().update()
        if self.selected:
            self.mostrar_cantidad()

    def increment(self):
        self.ticks += 1
        if self.ticks % 30 == 0:
            self.cantidad -= 1
            if self.cantidad <= 0:
                self.do_action()

    def confirm(self):
        self.ticks = 0
        self.do_action()

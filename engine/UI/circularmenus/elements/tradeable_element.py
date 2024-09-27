from engine.globs.event_dispatcher import EventDispatcher
from .letter import LetterElement
from .descriptive_area import DescriptiveArea

class TradeableElement(LetterElement):
    def __init__(self, parent, item):
        self.item = item
        super().__init__(parent, item.nombre, item.image, do_title=True)
        self.description = DescriptiveArea(self, description=item.efecto_des)

    def do_action(self):
        node = self.parent.parent
        arbol = node.parent

        next_node = arbol[int(node.leads)]
        coin = self.item.data['trading']['coin_symbol']
        price = self.item.data['trading']['sell_price']
        text = next_node.texto
        new_text = text.format(coin=coin, price=str(price))
        arbol[int(node.leads)] = new_text

        dialogo = arbol.parent
        dialogo.frontend.set_text(new_text)
        dialogo.frontend.show()
        dialogo.frontend.update()
        self.parent.salir()


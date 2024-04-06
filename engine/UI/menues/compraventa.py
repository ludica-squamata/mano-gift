from engine.globs.event_dispatcher import EventDispatcher
from engine.globs import EngineData
from .menu import Menu


class BaseTradingMenu(Menu):
    # Metaclass para no copiar las mismas funciones en ambos menúes.
    def cancelar(self):
        EngineData.acceso_menues.clear()
        self.deregister()
        EventDispatcher.trigger('EndDialog', self, {'layer': self.layer})


class MenuSell(BaseTradingMenu):
    pass


class MenuBuy(BaseTradingMenu):
    pass


def trigger_trading_menus(event):
    if event.tipo == "TriggerBuyScreen":
        EventDispatcher.trigger('OpenMenu', "dialog", {'value': 'Comprar', "nombre": "Comprar"})
    elif event.tipo == "TriggerSellScreen":
        EventDispatcher.trigger('OpenMenu', "dialog", {'value': 'Vender', "nombre": "Vender"})


EventDispatcher.register(trigger_trading_menus, "TriggerBuyScreen", "TriggerSellScreen")

__all__ = [
    "MenuSell",
    "MenuBuy"
]

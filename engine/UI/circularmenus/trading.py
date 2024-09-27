from .rendered import RenderedCircularMenu
from .elements import TradeableElement
from engine.globs.event_dispatcher import EventDispatcher
from engine.globs import Mob_Group

class TradingCircularMenu(RenderedCircularMenu):
    first = 0
    traders = None
    def __init__(self, parent, cascadas):
        self.set_idxs(cascadas)
        self.parent = parent
        super().__init__(cascadas)

    def fill_participantes(self, participants):
        self.traders = {}
        for name in participants:
            if name == 'heroe':
                mob = Mob_Group.get_controlled_mob()
                mob.detener_movimiento()
                mob.AI.deregister()
            else:
                mob = Mob_Group.get_named(name)[0]
                mob.hablando = True
                mob.AI.trigger_node(25)
            self.traders[name] = mob

    def set_idxs(self, cascadas):
        for n in cascadas:
            cascada = cascadas[n]
            for element in cascada:  # aunque me gustaria ponerlo en un onliner.
                element.index = cascada.index(element)  # esto soluciona el tema de recordar la posición del item.

            if self.first <= len(cascada)-1:
                for idx, opt in enumerate([cascada[self.first]] + cascada[self.first + 1:] + cascada[:self.first]):
                    opt.idx = idx
            else:
                for idx, opt in enumerate(cascada):
                    opt.idx = idx


class BuyingCM(TradingCircularMenu):
    def __init__(self, parent, participants):
        self.fill_participantes(participants)
        buyable = [self.traders[name].inventario.contenido() for name in self.traders if name != 'heroe'][0]
        cascadas = {
            'inicial':[
                [TradeableElement(self, item) for item in buyable]
            ]
        }
        super().__init__(parent, cascadas)

class SellingCM(TradingCircularMenu):
    def __init__(self, parent, participants):
        self.fill_participantes(participants)
        sellable = [self.traders[name].inventario.contenido() for name in self.traders if name == 'heroe'][0]
        cascadas = {
            'inicial': [TradeableElement(self, item) for item in sellable]
        }
        super().__init__(parent, cascadas)

def trigger_trading_menu(event):
    menu = None
    if event.tipo == 'TriggerSellScreen':
        menu = SellingCM
    elif event.tipo == 'TriggerBuyScreen':
        menu = BuyingCM

    dialogo = event.origin.parent.parent
    dialogo.toggle_pause()
    dialogo.frontend.hide()
    menu(event.origin, event.data['participants'])

class Trade:
    pass

#
# def engage_dialog(event):
#     if event.data['nom'] == 'accion' and event.data['type'] == 'tap':
#         if "ReactivateDialog" in EventDispatcher.get_registered():
#             EventDispatcher.trigger('ReactivateDialog', 'KEY', {})



EventDispatcher.register(trigger_trading_menu, "TriggerBuyScreen","TriggerSellScreen")
# EventDispatcher.register(engage_dialog, "Key")
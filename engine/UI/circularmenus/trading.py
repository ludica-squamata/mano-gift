from engine.globs.event_dispatcher import EventDispatcher
from engine.globs.event_aware import EventAware
from .rendered import RenderedCircularMenu
from .elements import TradeableElement
from engine.globs import Mob_Group


class TradingCircularMenu(RenderedCircularMenu):
    first = 0
    traders = None
    trade = None

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
                mob.paused = True
                mob.pause_overridden = True
            else:
                mob = Mob_Group.get_named(name)[0]
                mob.hablando = True
                mob.paused = True
                mob.AI.trigger_node(25)
                mob.pause_overridden = True

            self.traders[name] = mob

    def set_idxs(self, cascadas):
        for n in cascadas:
            cascada = cascadas[n]
            for element in cascada:
                index = cascada.index(element)  # esto soluciona el tema de recordar la posición del item.
                element.index = index  # aunque me gustaria ponerlo en un onliner.

            if self.first <= len(cascada) - 1:
                for idx, opt in enumerate([cascada[self.first]] + cascada[self.first + 1:] + cascada[:self.first]):
                    opt.idx = idx
            else:
                for idx, opt in enumerate(cascada):
                    opt.idx = idx

    def salir(self):
        self.trade.engage()
        super().salir()


class BuyingCM(TradingCircularMenu):
    def __init__(self, parent, participants):
        from engine.scenery import new_item
        self.fill_participantes(participants)
        trading = parent.parent.parent.trading
        buyable, cantidades = [], []
        for trader in self.traders:
            if trader in trading:
                for key in trading[trader]:
                    buyable.append(new_item(self, key, trading[trader][key]['ruta']))
                    cantidades.append(trading[trader][key]['cant'])

        cascadas = {
            'inicial': [TradeableElement(self, 'buy', buyable[i], cantidades[i]) for i in range(len(buyable))]
        }
        self.trade = Trade(self)
        super().__init__(parent, cascadas)


class SellingCM(TradingCircularMenu):
    def __init__(self, parent, participants):
        self.fill_participantes(participants)
        sellable = self.traders['heroe'].inventario.uniques()
        cantidades = [self.traders['heroe'].inventario.cantidad(item) for item in sellable]
        cascadas = {
            'inicial': [TradeableElement(self, "sell", sellable[i], cantidades[i]) for i in range(len(sellable))]
        }
        self.trade = Trade(self)
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


class Trade(EventAware):
    engaged = False

    def __init__(self, parent):
        super().__init__()
        self.parent = parent

        self.functions['tap'].update({'accion': self.re_engage_dialog})
        EventDispatcher.register(self.concrete_trade, "Trade")

    def engage(self):
        for trader in self.parent.traders.values():
            trader.pause = True
            trader.hablando = True
            trader.pause_overriden = True
            if hasattr(trader.AI, 'deregister'):
                trader.AI.deregister()

        self.engaged = True

    def disengage(self):
        for trader in self.parent.traders.values():
            trader.pause = False
            trader.pause_overridden = False
            trader.hablando = False
            if hasattr(trader.AI, 'register'):
                trader.AI.register()

        EventDispatcher.trigger('TogglePause', self, {'value': False})
        self.engaged = False

    def re_engage_dialog(self):
        if self.engaged:
            EventDispatcher.trigger('ReactivateDialog', self, {'value': True})
            self.engaged = False

    def concrete_trade(self, event):
        self.disengage()
        self.deregister()
        print(self, event)


EventDispatcher.register(trigger_trading_menu, "TriggerBuyScreen", "TriggerSellScreen")

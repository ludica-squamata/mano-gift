from engine.globs.event_dispatcher import EventDispatcher
from engine.globs import Mob_Group, Tiempo, EngineData
from engine.globs.event_aware import EventAware
from .rendered import RenderedCircularMenu
from .elements import TradeableElement


class TradingCircularMenu(RenderedCircularMenu):
    traders = None
    trade = None

    name = ''

    def __init__(self, parent, cascadas):
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
                mob = Mob_Group.get_by_trait('nombre', name)
                mob.hablando = True
                mob.paused = True
                mob.AI.trigger_node(25)
                mob.pause_overridden = True

            self.traders[name] = mob

    def salir(self):
        self.trade.engage()
        super().salir()

    def __repr__(self):
        return self.name


class BuyingCM(TradingCircularMenu):
    def __init__(self, parent, participants):
        self.name = 'Buying CM'
        self.fill_participantes(participants)
        for trader in self.traders:
            mob = Mob_Group.get_by_trait('nombre', trader)
            if mob is not None:
                buyable = mob.inventario.uniques()
                cantidades = [mob.inventario.cantidad(item) for item in buyable]

                cascadas = {
                    'inicial': [TradeableElement(self, "buy", buyable[i], cantidades[i]) for i in range(len(buyable))]
                }
                self.trade = Trade(self)
                super().__init__(parent, cascadas)


class SellingCM(TradingCircularMenu):

    @classmethod
    def is_possible(cls):
        mob = Mob_Group.get_controlled_mob()
        return len(mob.inventario) > 0

    def __init__(self, parent, participants):
        self.name = 'Selling CM'
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
    possible = False
    if event.tipo == 'TriggerSellScreen':
        menu = SellingCM
        possible = menu.is_possible()
    elif event.tipo == 'TriggerBuyScreen':
        menu = BuyingCM
        possible = True

    dialogo = event.origin.parent.parent
    if possible:
        dialogo.toggle_pause()
        dialogo.frontend.hide()
        menu(event.origin, event.data['participants'])
    else:
        arbol = dialogo.arbol
        next_node = arbol[dialogo.cant_sell]
        arbol.set_actual(next_node)
        dialogo.hablar()


class Trade(EventAware):
    engaged = False
    delta = 0

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

        EventDispatcher.trigger('TogglePause', self, {'value': False})
        self.engaged = False

    def re_engage_dialog(self):
        if self.engaged:
            dialog_id = self.parent.parent.parent.parent.id
            EventDispatcher.trigger('ReactivateDialog', self, {'value': True, 'id': dialog_id})
            self.engaged = False

    def set_delta(self, delta):
        self.delta = delta

    def concrete_trade(self, event):
        self.disengage()
        self.deregister()
        if event.data['value'] is True:
            buyer, seller = None, None
            if type(self.parent) is BuyingCM:
                # BuyingCM > Nodo > Arbol > Dialogo.locutores[Nodo.emisor]
                buyer = self.parent.parent.parent.parent.locutores[self.parent.parent.emisor]
                seller = self.parent.parent.parent.parent.locutores[self.parent.parent.receptor]
            elif type(self.parent) is SellingCM:
                buyer = self.parent.parent.parent.parent.locutores[self.parent.parent.receptor]
                seller = self.parent.parent.parent.parent.locutores[self.parent.parent.emisor]

            item = self.parent.actual.item
            value = item.price_buy if type(self.parent) is BuyingCM else item.price_sell
            coin = item.coin

            for _ in range(self.delta):
                buyer.recibir_item(item)
                seller.vender_item(item)

            buyer.entregar_dinero(coin, value)
            seller.recibir_dinero(coin, value)

            timestamp = Tiempo.clock.timestamp()

            transactions = [
                {'trader': buyer.nombre, 'item': item.nombre, 'delta': self.delta, 'tiempo': timestamp},
                {'trader': seller.nombre, 'item': item.nombre, 'delta': -self.delta, 'tiempo': timestamp}
            ]
            EngineData.extend_trades(transactions)

    def __repr__(self):
        return "Trade"


EventDispatcher.register(trigger_trading_menu, "TriggerBuyScreen", "TriggerSellScreen")

from .DialogInterface import DialogInterface
from engine.globs import EngineData, CAPA_OVERLAYS_DIALOGOS
from engine.globs.event_aware import EventAware
from engine.globs.eventDispatcher import EventDispatcher


class PropDescription (EventAware):
    item = None
    frontend = None

    def __init__(self, item):
        super().__init__()

        self.item = item
        if item.nombre is None or item.descripcion is None:
            self.salir()
        else:
            self.frontend = DialogInterface(self)
            self.frontend.set_text(item.nombre+': '+self.item.descripcion)

        self.functions['tap'].update({
            'accion': self.salir,
            'contextual': self.salir,
            'arriba': lambda: self.desplazar_texto('arriba'),
            'abajo': lambda: self.desplazar_texto('abajo')})

        self.functions['hold'].update({
            'arriba': lambda: self.desplazar_texto('arriba'),
            'abajo': lambda: self.desplazar_texto('abajo')})

        EngineData.MODO = 'Dialogo'

    def desplazar_texto(self, direccion):
        if direccion == 'arriba':
            self.frontend.scroll(+1)
        elif direccion == 'abajo':
            self.frontend.scroll(-1)

    def salir(self):
        self.deregister()
        EventDispatcher.trigger('EndDialog', self, {'layer': CAPA_OVERLAYS_DIALOGOS})

from .DialogInterface import DialogInterface
from engine.globs import EngineData, CAPA_OVERLAYS_DIALOGOS
from engine.globs.event_aware import EventAware


class PropDescription (EventAware):

    def __init__(self, item):
        super().__init__()
        self.item = item
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
        EngineData.DIALOG = self

    def listener(self, event):
        try:
            if event.origin == 'Modo.Dialogo':
                self.use_function(event.data['type'], event.data['nom'])
        except KeyError:
            pass

    def desplazar_texto(self, direccion):
        if direccion == 'arriba':
            self.frontend.scroll(+1)
        elif direccion == 'abajo':
            self.frontend.scroll(-1)

    def salir(self):
        self.deregister()
        EngineData.end_dialog(CAPA_OVERLAYS_DIALOGOS)

    def update(self):
        pass

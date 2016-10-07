from .Dialog import DialogInterface
from engine.globs import EngineData, CAPA_OVERLAYS_DIALOGOS


class PropDescription:
    def __init__(self, item):
        self.item = item
        self.frontend = DialogInterface(self)
        self.frontend.set_text(item.nombre+': '+self.item.descripcion)

        self.functions = {
            'tap': {
                'hablar': lambda: EngineData.end_dialog(CAPA_OVERLAYS_DIALOGOS),
                'cancelar': lambda: EngineData.end_dialog(CAPA_OVERLAYS_DIALOGOS),
                'arriba': lambda: self.desplazar_texto('arriba'),
                'abajo': lambda: self.desplazar_texto('abajo'),
            },
            'hold': {
                'arriba': lambda: self.desplazar_texto('arriba'),
                'abajo': lambda: self.desplazar_texto('abajo'),
            }
        }

    def use_function(self, mode, key):
        if mode in self.functions:
            if key in self.functions[mode]:
                self.functions[mode][key]()

    def desplazar_texto(self, direccion):
        if direccion == 'arriba':
            self.frontend.scroll(+1)
        elif direccion == 'abajo':
            self.frontend.scroll(-1)

    def update(self):
        pass

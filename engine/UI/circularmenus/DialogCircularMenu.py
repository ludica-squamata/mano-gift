from engine.globs import EngineData as Ed, CAPA_OVERLAYS_CIRCULAR, ModData
from .RenderedCircularMenu import RenderedCircularMenu
from .elements import DialogElement, CommandElement
from engine.misc import Resources as Rs
from os import path, listdir


class DialogCircularMenu(RenderedCircularMenu):
    radius = 15
    layer = CAPA_OVERLAYS_CIRCULAR

    def __init__(self, *locutores):
        self.locutores = locutores

        opciones = []
        idx = -1
        for script in listdir(ModData.dialogos):
            ruta = ModData.dialogos + script
            if path.isfile(ruta):
                file = Rs.abrir_json(ruta)
                if file['head']['class'] == 'chosen':
                    idx += 1
                    file.update({'idx': idx})
                    opciones.append(file)

        cascadas = {'inicial': []}
        for opt in opciones:
            obj = DialogElement(self, opt)
            obj.idx = opt['idx']
            cascadas['inicial'].append(obj)

        super().__init__(cascadas)
        self.show()

        self.functions['tap'].update({'cancelar': self.back})

    def cerrar(self):
        for mob in self.locutores:
            mob.hablando = False
        Ed.MODO = 'Aventura'
        self.salir()

    def salir(self):
        self.cascadaActual = 'inicial'
        super().salir()

    def back(self):
        if self.cascadaActual == 'inicial':
            self.cerrar()
        else:
            super().back()

    def enter(self):
        self.supress_all()
        elm = CommandElement(self, {'name': 'Aceptar', 'icon': 'A', 'cmd': lambda: None, 'idx': 0})
        super().add_element('inicial', elm)

    def add_element(self, cascada, element):
        elm = DialogElement(self, element)
        super().add_element('inicial', elm)



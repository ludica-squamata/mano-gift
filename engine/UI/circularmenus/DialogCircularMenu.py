from engine.globs import EngineData as Ed, CAPA_OVERLAYS_CIRCULAR, ModData
from .RenderedCircularMenu import RenderedCircularMenu
from .elements import TopicElement, DialogOptionElement
from engine.misc.resources import abrir_json
from os import path, listdir


class DialogCircularMenu(RenderedCircularMenu):
    radius = 15
    layer = CAPA_OVERLAYS_CIRCULAR
    locutores = None

    def __init__(self, *locutores):
        self.locutores = locutores

        opciones = []
        idx = -1
        for script in listdir(ModData.dialogos):
            ruta = ModData.dialogos + script
            if path.isfile(ruta):
                file = abrir_json(ruta)
                if file['head']['class'] == 'chosen':
                    idx += 1
                    file.update({'idx': idx})
                    opciones.append(file)

        cascadas = {'inicial': []}
        for opt in opciones:
            obj = TopicElement(self, opt)
            obj.idx = opt['idx']
            cascadas['inicial'].append(obj)

        super().__init__(cascadas)
        self.functions['tap'].update({'contextual': self.back})

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

    def add_element(self, cascada, element):
        elm = DialogOptionElement(self, element)
        super().add_element(cascada, elm)

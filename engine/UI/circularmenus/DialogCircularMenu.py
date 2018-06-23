from engine.globs import EngineData, ModData
from .RenderedCircularMenu import RenderedCircularMenu
from .elements import TopicElement, DialogOptionElement
from engine.misc.resources import abrir_json
from os import path, listdir


class DialogCircularMenu(RenderedCircularMenu):
    radius = 15
    locutores = None

    def __init__(self, *locutores):
        self.locutores = locutores

        cascadas = {'inicial': []}
        idx = -1
        for script in listdir(ModData.dialogos):
            ruta = ModData.dialogos + script
            if path.isfile(ruta):
                file = abrir_json(ruta)
                if TopicElement.pre_init(file['head'], locutores):
                    idx += 1
                    file.update({'idx': idx})
                    obj = TopicElement(self, file)
                    cascadas['inicial'].append(obj)

        super().__init__(cascadas)
        self.functions['tap'].update({'contextual': self.back})

    @classmethod
    def is_possible(cls, *locutores) -> bool:
        for script in listdir(ModData.dialogos):
            ruta = ModData.dialogos + script
            if path.isfile(ruta):
                file = abrir_json(ruta)
                if TopicElement.pre_init(file['head'], locutores):
                    return True

    def cerrar(self):
        for mob in self.locutores:
            mob.hablando = False
        EngineData.MODO = 'Aventura'
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

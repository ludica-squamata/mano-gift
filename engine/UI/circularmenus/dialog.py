from .rendered import RenderedCircularMenu
from engine.globs import ModData
from engine.misc.resources import abrir_json
from os import path, listdir
from engine.IO.dialogo import Dialogo, Discurso


class DialogCircularMenu(RenderedCircularMenu):
    locutores = None

    def __init__(self, *locutores):
        self.locutores = locutores
        self.change_radius = False
        self.radius = 60
        self.nombre = 'Dialog'

        for script in listdir(ModData.dialogos):
            ruta = ModData.dialogos + script
            if path.isfile(ruta):
                file = abrir_json(ruta)
                if Discurso.pre_init(file['head'], *locutores):
                    # hay que ver que pre_init() verifique bien los dialogos, porque ahora son todos scripteados.
                    dialogo = Dialogo(file, *locutores)
                    dialogo.frontend.set_menu(self)
                else:
                    # aca habría que cerrar el menu, porque es inválido, o capaz abrir el dialogo por default.
                    # aunque en realidad, este else esta mal porque los dialogos inválidos se descartan en el loop
                    pass

        super().__init__({'inicial': []})
        self.deregister()

    @classmethod
    def is_possible(cls, *locutores) -> bool:
        for script in listdir(ModData.dialogos):
            ruta = ModData.dialogos + script
            if path.isfile(ruta):
                file = abrir_json(ruta)
                if Discurso.pre_init(file['head'], *locutores):
                    return True

    def cerrar(self):
        for mob in self.locutores:
            mob.hablando = False
        self.salir()

    def salir(self):
        self.cascadaActual = 'inicial'
        super().salir()

    def back(self):
        if self.cascadaActual == 'inicial':
            self.cerrar()
        else:
            super().backward()

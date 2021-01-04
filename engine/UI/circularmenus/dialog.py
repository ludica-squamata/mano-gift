from engine.globs import ModData, Mob_Group, GameState
from engine.IO.dialogo import Dialogo, Discurso
from engine.misc.resources import abrir_json
from .rendered import RenderedCircularMenu
from os import path, listdir


class DialogCircularMenu(RenderedCircularMenu):
    locutores = None

    def __init__(self, file, *locutores):
        self.locutores = locutores
        self.change_radius = False
        self.radius = 60
        self.nombre = 'Dialog'

        dialogo = Dialogo(file, *locutores)
        dialogo.frontend.set_menu(self)

        super().__init__({'inicial': []})
        self.deregister()

    @classmethod
    def is_possible(cls, *locutores):
        for script in listdir(ModData.dialogos):
            ruta = ModData.dialogos + script
            if path.isfile(ruta):
                file = cls.preprocess_locutor(abrir_json(ruta))
                name = 'dialog.{}.enabled'.format(file['head']['about'])
                if not GameState.get(name) and '..' not in name:
                    GameState.set(name, False)
                if Discurso.pre_init(file['head'], *locutores):
                    return file, True
        return None, False

    @staticmethod
    def preprocess_locutor(file):
        hero_name = Mob_Group.character_name
        if 'heroe' in file['head']['locutors']:
            idx = file['head']['locutors'].index('heroe')
            file['head']['locutors'][idx] = hero_name

            for s_idx in file['body']:
                node = file['body'][s_idx]
                if node['from'] == 'heroe':
                    node['from'] = hero_name
                # elif, because the hero wouldn't be talking to himself.
                elif node['to'] == 'heroe':
                    node['to'] = hero_name

                if 'reqs' in node and 'loc' in node['reqs'] and node['reqs']['loc'] == 'heroe':
                    node['reqs']['loc'] = hero_name
        return file

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

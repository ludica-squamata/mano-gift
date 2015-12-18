﻿from os import getcwd as cwd, path, listdir
from importlib import machinery

class ModData:
    mod_folder = ''
    data = {}

    # carpetas varias
    graphs = ''
    dialogos = ''
    mapas = ''
    mobs = ''
    quests = ''
    items = ''
    scripts = ''
    scenes = ''
    
    @classmethod
    def init(cls, ini):
        from engine.misc import Util as U
        
        if not cls._find_mod_folder(ini):
            U.salir("la ruta no existe")
        
        data = cls._get_file_data('mod.json')
        if data is not None:
            
            cls.data = data
            root = cls.mod_folder
            
            cls.graphs = root+data['folders']['graficos']+'/'
            cls.dialogos = root+data['folders']['dialogos']+'/'
            cls.mapas = root+data['folders']['mapas']+'/'
            cls.mobs = root+data['folders']['mobs']+'/'
            cls.quests = root+data['folders']['quest']+'/'
            cls.items = root+data['folders']['items']+'/'
            cls.scripts = root+data['folders']['scripts']+'/'
            cls.scenes = root+data['folders']['scenes']+'/'
            
            for script in listdir(cls.scripts):
            # lo convertí en un loop para poder agregar, por ejemplo,
            # una pantalla de gameover sin tener que buscar ese nombre
                ruta = cls.scripts+script
                if path.isfile(ruta):
                    name = script.rstrip('.py')
                    module = machinery.SourceFileLoader("module.name", ruta).load_module()
                    if hasattr(module, name) and not hasattr(cls,name):
                        # lo resolví mmás fácil. Si ésta clase no tiene el nombre ya...
                        setattr(cls,name,(getattr(module, name)))
                        # añadirlo.
        
        else:
            U.salir('No data in mod folder')
    
    @classmethod
    def _find_mod_folder(cls, ini):
        folder = path.normpath(path.join(cwd(), ini['folder']))
        if not path.exists(folder):
            folder = path.normpath(ini['folder'])
            if not path.exists(folder):
                return False
        
        cls.mod_folder = folder.replace('\\','/')+'/'
        return True
    
    @classmethod
    def _get_file_data(cls, filename):
        from engine.misc import Resources as r
        ruta = cls.mod_folder+filename
        if not path.exists(ruta):
            return None
        
        data = r.abrir_json(ruta)
        return data

from os import getcwd as cwd, path
from .globs import EngineData as ED
from .misc import Resources as r

def find_mod_folder(ini):
    folder = path.normpath(path.join(cwd(),ini['folder']))
    if not path.exists(folder):
        folder = path.normpath(ini['folder'])
        if not path.exists(folder):
            return False
    
    ED.mod_folder = folder
    return True

def get_file_data(filename):
    folder = ED.mod_folder
    ruta = path.join(folder,filename)
    if path.exists(ruta):
        data = r.abrir_json(ruta)
        return data
    else:
        print(folder)

def set_engineIni(datos):
    ruta = cwd()+'engine.ini'
    r.guardar_json(ruta,datos)
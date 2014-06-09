from os import getcwd as cwd, path
from engine.misc import Resources as r

class ModData:
    
    mod_folder = ''
    
    @staticmethod
    def find_mod_folder(ini):
        folder = path.normpath(path.join(cwd(),ini['folder']))
        if not path.exists(folder):
            folder = path.normpath(ini['folder'])
            if not path.exists(folder):
                return False
        
        ModData.mod_folder = folder
        return True
    
    @staticmethod
    def get_file_data(filename):
        folder = ModData.mod_folder
        ruta = path.join(folder,filename)
        if path.exists(ruta):
            data = r.abrir_json(ruta)
            return data
        else:
            print(folder)

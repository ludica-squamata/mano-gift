from os import getcwd as cwd, path

class ModData:
    
    mod_folder = ''
    data = {}
    graphfolder = ''
    
    def init(ini):
        from engine.misc import Util as U
        if not ModData.find_mod_folder(ini):
            U.salir("la ruta no existe")
        
        data = ModData.get_file_data('mod.json')
        if data != None:
            
            ModData.data = data
            root = ModData.mod_folder
            
            ModData.graphs = root+data['folders']['graficos']+'/'
            ModData.dialogos = root+data['folders']['dialogos']+'/'
            ModData.mapas = root+data['folders']['mapas']+'/'
            ModData.mobs = root+data['folders']['mobs']+'/'
            ModData.quests = root+data['folders']['quest']+'/'
            ModData.items = root+data['folders']['items']+'/'
            ModData.scripts = root+data['folders']['scripts']+'/'
            ModData.scenes = root+data['folders']['scenes']+'/'
        else:
            U.salir('No data in mod folder')
    
    @staticmethod
    def find_mod_folder(ini):

        folder = path.normpath(path.join(cwd(),ini['folder']))
        if not path.exists(folder):
            folder = path.normpath(ini['folder'])
            if not path.exists(folder):
                return False
        
        ModData.mod_folder = folder.replace('\\','/')+'/'
        return True
    
    @staticmethod
    def get_file_data(filename):
        from engine.misc import Resources as r
        _folder = path.join(cwd(),'demo_data\\')
        folder = ModData.mod_folder
        ruta = folder+filename
        if not path.exists(ruta):
            ruta = _folder+filename
            ModData.mod_folder = _folder
        
        data = r.abrir_json(ruta)
        return data
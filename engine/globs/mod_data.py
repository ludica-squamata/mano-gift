from os import getcwd as cwd, path

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
        from importlib import machinery
        import types
        
        if not cls.find_mod_folder(ini):
            U.salir("la ruta no existe")
        
        data = cls.get_file_data('mod.json')
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
            
            loader = machinery.SourceFileLoader("module.name", root+data['intro'])
            m = loader.load_module()
            cls.intro = getattr(m, "intro")
            
        else:
            U.salir('No data in mod folder')
    
    @classmethod
    def find_mod_folder(cls, ini):

        folder = path.normpath(path.join(cwd(), ini['folder']))
        if not path.exists(folder):
            folder = path.normpath(ini['folder'])
            if not path.exists(folder):
                return False
        
        cls.mod_folder = folder.replace('\\','/')+'/'
        return True
    
    @classmethod
    def get_file_data(cls, filename):
        from engine.misc import Resources as r
        _folder = path.join(cwd(),'demo_data\\')
        folder = cls.mod_folder
        ruta = folder+filename
        if not path.exists(ruta):
            ruta = _folder+filename
            cls.mod_folder = _folder
        
        data = r.abrir_json(ruta)
        return data
    
    def intro(cls):
        pass

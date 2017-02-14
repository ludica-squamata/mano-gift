from os import getcwd as cwd, path, listdir
from importlib import machinery
from engine.misc import Util, Resources
from engine.globs.tiempo import Tiempo


class ModData:
    mod_folder = ''
    data = {}

    # carpetas varias
    graphs = ''
    dialogos = ''
    mapas = ''
    mobs = ''
    items = ''
    scripts = ''
    QMC = None

    @classmethod
    def init(cls, ini_data):

        real = ini_data.get('real_clock', False)
        min_l = ini_data.get('minute_lenght', 60)
        Tiempo.set_clock(real, min_l)

        if not cls._find_mod_folder(ini_data):
            Util.salir("la ruta no existe")

        data = cls._get_file_data('mod.json')
        if data is not None:

            cls.data = data
            root = cls.mod_folder

            cls.graphs = root + data['folders']['graficos'] + '/'
            cls.dialogos = root + data['folders']['dialogos'] + '/'
            cls.mapas = root + data['folders']['mapas'] + '/'
            cls.mobs = root + data['folders']['mobs'] + '/'
            cls.items = root + data['folders']['items'] + '/'
            cls.scripts = root + data['folders']['scripts'] + '/'

            for script in listdir(cls.scripts):
                # lo convertí en un loop para poder agregar, por ejemplo,
                # una pantalla de gameover sin tener que buscar ese nombre
                ruta = cls.scripts + script

                if path.isfile(ruta):
                    name = script.rstrip('.py')
                    # if sys.version_info.minor == 3:  # python 3.3
                    module = machinery.SourceFileLoader("module.name", ruta).load_module()
                    # elif sys.version_info.minor == 4:  # python 3.4
                    # Deshabilitado porque me tira una exception que no entiendo.
                    # module = machinery.SourceFileLoader("module.name", ruta).exec_module()

                    if hasattr(module, name) and not hasattr(cls, name):
                        # lo resolví mmás fácil. Si ésta clase no tiene el nombre ya...
                        setattr(cls, name, (getattr(module, name)))
                        # añadirlo.

                    elif name == 'circularmenu':
                        cls.QMC = []
                        i = -1
                        for d in cls.data.get('circularmenu', []):
                            if hasattr(module, d['name']):
                                i += 1
                                d.update({'idx': i})
                                spec = getattr(module, d['name'])
                                if type(spec) is list:
                                    d.update({'csc': spec})
                                else:
                                    d.update({'cmd': spec})
                                cls.QMC.append(d)

        else:
            Util.salir('No data in mod folder')

    @classmethod
    def _find_mod_folder(cls, ini):
        folder = path.normpath(path.join(cwd(), ini['folder']))
        if not path.exists(folder):
            folder = path.normpath(ini['folder'])
            if not path.exists(folder):
                return False

        cls.mod_folder = folder.replace('\\', '/') + '/'
        return True

    @classmethod
    def _get_file_data(cls, filename):
        ruta = cls.mod_folder + filename
        if not path.exists(ruta):
            return None

        data = Resources.abrir_json(ruta)
        return data

    @classmethod
    def get_script_method(cls, scriptname, methodname):
        ruta = cls.scripts + scriptname
        module = machinery.SourceFileLoader("module.name", ruta).load_module()
        if hasattr(module, methodname):
            return getattr(module, methodname)

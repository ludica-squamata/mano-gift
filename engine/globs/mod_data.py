from os import getcwd as cwd, path, listdir
from engine.misc import salir, abrir_json
from engine.globs.tiempo import Tiempo
from importlib import import_module


class ModData:
    mod_folder = ''
    data = {}

    # carpetas varias
    graphs = ''
    dialogos = ''
    mapas = ''
    mobs = ''
    items = ''
    fd_scripts = ''
    pkg_scripts = ''
    fd_player = ''
    custommenus = None
    QMC = None

    @classmethod
    def init(cls, ini_data):

        real = ini_data.get('real_clock', False)
        min_l = ini_data.get('minute_lenght', 60)
        Tiempo.set_clock(real, min_l)

        if not cls._find_mod_folder(ini_data):
            salir("la ruta no existe")

        data = cls._get_file_data(ini_data['data_file'])
        if data is None:
            salir('No data in mod folder')

        else:
            cls.data = data
            root = cls.mod_folder

            cls.graphs = root + data['folders']['graficos'] + '/'
            cls.dialogos = root + data['folders']['dialogos'] + '/'
            cls.mapas = root + data['folders']['mapas'] + '/'
            cls.mobs = root + data['folders']['mobs'] + '/'
            cls.items = root + data['folders']['items'] + '/'
            cls.fd_scripts = root + data['folders']['scripts'] + '/'
            cls.fd_player = root + data['folders']['player'] + '/'
            cls.pkg_scripts = '.'.join([ini_data['folder'], data['folders']['scripts']])

            loaded = []
            cls.custommenus = {}
            cls.QMC = []
            for keyword in cls.data.get('custom', ''):
                if keyword == 'menus':
                    for d in cls.data['custom']['menus']:
                        loaded.append(d['script'])
                        ruta = cls.fd_scripts + d['script']
                        module = import_module(cls.pkg_scripts + '.' + d['script'], ruta)
                        menu = getattr(module, d['name'])
                        cls.custommenus[d['name']] = menu

                elif keyword == 'circular':
                    skip = 0
                    for i, d in enumerate(cls.data['custom']['circular']):
                        ruta = cls.fd_scripts + d['script']
                        module = import_module(cls.pkg_scripts + '.' + d['script'], ruta)
                        loaded.append(d['script'])
                        if hasattr(module, d['name']):
                            d.update({'idx': i-skip})
                            spec = getattr(module, d['name'])
                            if type(spec) is list:
                                d.update({'csc': spec})
                            else:
                                d.update({'cmd': spec})
                            cls.QMC.append(d)
                        else:
                            skip += 1

            folders = [cls.fd_scripts, cls.fd_scripts + 'behaviours/', cls.fd_scripts + 'events/']
            for folder in folders:
                package = folder.split('/')[-2]+'.' if folder != cls.fd_scripts else ''
                for script in listdir(folder):
                    ruta = folder + script
                    if path.isfile(ruta):
                        script_name = script.rstrip('.py')
                        if script_name not in loaded:
                            import_module(cls.pkg_scripts + '.' + package + script_name, folder)

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

        data = abrir_json(ruta)
        return data

    @classmethod
    def get_script_method(cls, scriptname, methodname):
        ruta = cls.fd_scripts + scriptname
        module = import_module(cls.fd_scripts + scriptname, ruta)
        if hasattr(module, methodname):
            return getattr(module, methodname)

from os import getcwd as cwd, path, listdir
from engine.misc import salir, abrir_json, raw_load_module
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
    fd_scripts = ''
    pkg_scripts = ''
    custommenus = {}
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

            cls.pkg_scripts = '.'.join([ini_data['folder'], data['folders']['scripts']])

            loaded = []
            for keyword in cls.data.get('custom', ''):
                cls.custommenus = {}
                if keyword == 'menus':
                    for d in cls.data['custom']['menus']:
                        loaded.append(d['script'])
                        ruta = cls.fd_scripts + d['script'] + '.py'
                        _module = raw_load_module(ruta)
                        menu = getattr(_module, d['name'])
                        cls.custommenus[d['name']] = menu

                elif keyword == 'circular':
                    cls.QMC = []
                    i = -1
                    for d in cls.data['custom']['circular']:
                        ruta = cls.fd_scripts + d['script'] + '.py'
                        _module = raw_load_module(ruta)
                        loaded.append(d['script'])
                        if hasattr(_module, d['name']):
                            i += 1
                            d.update({'idx': i})
                            spec = getattr(_module, d['name'])
                            if type(spec) is list:
                                d.update({'csc': spec})
                            else:
                                d.update({'cmd': spec})
                            cls.QMC.append(d)

            folders = [cls.fd_scripts, cls.fd_scripts + 'behaviours/', cls.fd_scripts + 'events/']
            for folder in folders:
                package = folder.split('/')[-2]+'.' if folder != cls.fd_scripts else ''
                for script in listdir(folder):
                    ruta = folder + script
                    if path.isfile(ruta):
                        script_name = script.rstrip('.py')
                        if script_name not in loaded:
                            raw_load_module(folder, cls.pkg_scripts+'.' + package + script_name)

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
        _module = raw_load_module(ruta)
        if hasattr(_module, methodname):
            return getattr(_module, methodname)

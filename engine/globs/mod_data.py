from os import getcwd as cwd, path, listdir
from engine.misc import salir, abrir_json
from engine.globs.tiempo import Tiempo
from importlib import import_module
from datetime import datetime
from random import randint


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
    custom_attr = None
    QMC = None

    dialogs_by_topic = None

    use_latitude = True

    character_generator = None

    preloaded_chunk_csv = {}

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
            cls.class_dialogs_by_topic()

            loaded = []
            cls.custommenus = {}
            cls.custom_attr = {}
            cls.character_generator = {}
            cls.QMC = []
            for keyword in cls.data.get('custom', ''):
                if keyword == 'menus':
                    for d in cls.data['custom'][keyword]:
                        loaded.append(d['script'])
                        ruta = cls.fd_scripts + d['script']
                        module = import_module(cls.pkg_scripts + '.' + d['script'], ruta)
                        menu = getattr(module, d['name'])
                        cls.custommenus[d['name']] = menu

                elif keyword == 'circular':
                    skip = 0
                    for i, d in enumerate(cls.data['custom'][keyword]):
                        ruta = cls.fd_scripts + d['script']
                        module = import_module(cls.pkg_scripts + '.' + d['script'], ruta)
                        loaded.append(d['script'])
                        if hasattr(module, d['name']):
                            d.update({'idx': i - skip})
                            spec = getattr(module, d['name'])
                            if type(spec) is list:
                                d.update({'csc': spec})
                            else:
                                d.update({'cmd': spec})
                            cls.QMC.append(d)
                        else:
                            skip += 1

                elif keyword == 'attributes':
                    for c in cls.data['custom'][keyword]:
                        loaded.append(c['name'])
                        ruta = cls.fd_scripts + 'mobs/' + c['script']
                        script_name = c['script'].rstrip('.py')
                        module = import_module(cls.pkg_scripts + '.mobs.' + script_name, ruta)
                        cls.custom_attr[c['name']] = getattr(module, c['name'])

                elif keyword == 'derivation':
                    c = cls.data['custom'][keyword]
                    loaded.append(c['name'])
                    ruta = cls.fd_scripts + c['script']
                    script_name = c['script'].rstrip('.py')
                    module = import_module(cls.pkg_scripts + '.' + script_name, ruta)
                    cls.attr_derivation = getattr(module, c['name'])

                elif keyword == 'world_properties':
                    props = cls.data['custom'][keyword]
                    cls.use_latitude = props['use_latitude']
                    year = props['year_lenght']
                    month = props['month_lenght']
                    week = props['week_lenght']
                    Tiempo.set_year(year, month, week)

                elif keyword == "characters":
                    for c in cls.data['custom'][keyword]:
                        data = cls.data['custom'][keyword][c]
                        loaded.append(data['name'])
                        ruta = cls.fd_scripts + 'mobs/' + data['script']
                        script_name = data['script'].rstrip('.py')
                        module = import_module(cls.pkg_scripts + '.mobs.' + script_name, ruta)
                        cls.character_generator[c] = getattr(module, data['name'])

            if not len(cls.QMC):
                cls.QMC = None

            folders = [cls.fd_scripts, cls.fd_scripts + 'behaviours/', cls.fd_scripts + 'events/']
            for folder in folders:
                package = folder.split('/')[-2] + '.' if folder != cls.fd_scripts else ''
                for script in listdir(folder):
                    ruta = folder + script
                    if path.isfile(ruta):
                        script_name = script.rstrip('.py')
                        if script_name not in loaded:
                            import_module(cls.pkg_scripts + '.' + package + script_name, folder)

    @staticmethod
    def attr_derivation(attr):
        # this hook is intentended to be applied when no custom derivation exists.
        return attr

    @classmethod
    def class_dialogs_by_topic(cls):
        cls.dialogs_by_topic = {}
        for script in listdir(cls.dialogos):
            ruta = cls.dialogos + script
            if path.isfile(ruta):
                about = abrir_json(ruta)['head']['about']
                if about != '':  # rules out the template.
                    cls.dialogs_by_topic[about] = ruta  # la ruta, y no el dict entero, para evitar la sobrecarga.

    @staticmethod
    def generate_id():
        r = randint(0, 99999)
        now = ''.join([char for char in str(datetime.now()) if char not in [' ', '.', ':', '-']])
        now = now[0:-5] + '-' + str(r).rjust(5, '0')
        return now

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

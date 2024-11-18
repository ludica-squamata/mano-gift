from engine.globs import GRUPO_ITEMS, Tagged_Items, ModData
from engine.globs.event_dispatcher import EventDispatcher
from engine.UI.prop_description import PropDescription
from engine.mapa.light_source import LightSource
from engine.base import ShadowSprite, AzoeSprite
from engine.misc import cargar_imagen
from importlib import import_module
from os.path import join
import types


class Escenografia(ShadowSprite):
    accionable = False
    action = None
    tipo = 'Prop'
    grupo = GRUPO_ITEMS
    luz = None

    def __init__(self, parent, x, y, z=0, nombre=None, data=None, imagen=None, rect=None):
        """
        :param imagen:
        :param x:
        :param y:
        :param data:

        :type imagen:str
        :type x:int
        :type y:int
        :type data:dict
        :return:
        """

        if imagen is None and data is not None:
            if 'imagenes' in data:
                imagen = data['imagenes']['prop']
            else:
                imagen = data.get('image')
        super().__init__(parent, imagen=imagen, rect=rect, x=x, y=y, dz=z)
        self.data = data
        self.nombre = data.get('nombre', nombre)
        self.solido = 'solido' in data.get('propiedades', [])
        self.proyectaSombra = 'sin_sombra' not in data.get('propiedades', [])
        keys = []
        if self.solido:
            keys.append('solido')
        if not self.proyectaSombra:
            keys.append('sin_sombra')
        if len(keys):
            Tagged_Items.add_item(self, *keys)
        if data.get('proyecta_luz', False):
            self.luz = LightSource(self, self.nombre, data, x, y)
        self.descripcion = data.get('descripcion', "Esto es un ejemplo")

        self.event_handlers = {}
        self.add_listeners()  # carga de event listeners

    def __repr__(self):
        c = self.__class__.__name__
        n = self.nombre
        i = self.id
        return f'Prop {c} ({n}, id:{i})'

    def show_description(self):
        PropDescription(self)

    def update(self, *args):
        super().update(*args)
        if self.luz is not None:
            self.luz.update()

    def add_listeners(self):
        """
        carga los listeners definido en el
        :return:None
        """
        if self.data.get('script') and self.data.get('eventos'):
            # cargar un archivo por ruta
            ruta = join(ModData.fd_scripts, 'events', self.data['script'])
            m = import_module(ruta, self.data['script'][:-3])

            for event_name, func_name in self.data['eventos'].items():
                if hasattr(m, func_name):
                    # esto le asigna la instancia actual como self a la función,
                    # así puede acceder a propiedades del sprite
                    method = types.MethodType(getattr(m, func_name), self)
                    self.event_handlers[event_name] = method
                    EventDispatcher.register(method, event_name)

    def remove_listeners(self):
        """
        quitar listeners, como parte de la limpieza de un sprite
        :return:None
        """
        if self.event_handlers:
            for event_name, f in self.event_handlers:
                EventDispatcher.deregister(f, event_name)


class Item(AzoeSprite):
    stackable = False
    subtipo = None

    # solo los items equipables tienen un subtipo distinto de None,
    # pero esto les permite ser comparados con otros tipos de item.

    is_colocable = False  # en principio.

    def __init__(self, parent, nombre, data):
        self.nombre = nombre
        self.data = data
        self.peso = data['peso']
        self.volumen = data['volumen']
        self.efecto_des = data.get('efecto', {}).get('des', '')
        self.stackable = 'stackable' in data['propiedades']
        self.data = data
        self.peso = self.data['peso']
        self.volumen = self.data['volumen']
        self.efecto_des = self.data.get('efecto', {}).get('des', '')
        self.stackable = 'stackable' in self.data['propiedades']
        imagen = cargar_imagen(join(ModData.graphs, self.data['imagenes']['item']))
        super().__init__(parent, imagen=imagen)

    def __eq__(self, other):
        # __eq__() ya no pregunta por el ID porque el ID hace único a cada item.
        test_1 = other.nombre == self.nombre
        # test_2 = self.tipo == other.tipo  # esto es lo mismo que preguntar por self.__class__
        # if hasattr(self, 'subtipo') and hasattr(other, 'subtipo'):
        #     test_3 = self.subtipo == other.subtipo
        # else:
        #     test_3 = False
        tests = [test_1]  # , test_2, test_3
        return all(tests)

    def __ne__(self, other):
        if other.nombre != self.nombre:
            return True
        elif self.id != other.id:
            return True
        else:
            return False

    def __hash__(self):
        return hash(self.nombre + str(self.volumen) + str(self.peso) + self.tipo)

    def __repr__(self):
        return self.nombre + ' (' + self.tipo + ')'

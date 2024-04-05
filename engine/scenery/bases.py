from engine.base import ShadowSprite, EventListener, AzoeSprite
from engine.UI.prop_description import PropDescription
from engine.mapa.light_source import LightSource
from engine.globs import GRUPO_ITEMS, Tagged_Items


class Escenografia(ShadowSprite, EventListener):
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


class Item(AzoeSprite):
    stackable = False

    def __init__(self, parent, nombre, imagen, data):
        self.nombre = nombre
        self.peso = data['peso']
        self.volumen = data['volumen']
        self.efecto_des = data['efecto']['des']
        self.stackable = 'stackable' in data['propiedades']
        super().__init__(parent, imagen=imagen)

    def __eq__(self, other):
        if other.__class__ == self.__class__ and self.id == other.id:
            return True
        else:
            return False

    def __ne__(self, other):
        if other.__class__ != self.__class__:
            return True
        elif self.id != other.id:
            return True
        else:
            return False

    def __repr__(self):
        return self.nombre + ' (' + self.tipo + ')'

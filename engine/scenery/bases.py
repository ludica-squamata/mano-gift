from engine.UI.propdescription import PropDescription
from engine.base import ShadowSprite, EventListener
from engine.mapa.LightSource import LightSource


class Escenografia(ShadowSprite, EventListener):
    accionable = False
    action = None

    def __init__(self, nombre, x, y, z=0, data=None, imagen=None, rect=None):
        """
        :param nombre:
        :param imagen:
        :param x:
        :param y:
        :param data:
        :type nombre:str
        :type imagen:str
        :type x:int
        :type y:int
        :type data:dict
        :return:
        """
        self.nombre = nombre
        self.tipo = 'Prop'
        self.data = data
        if imagen is None and data is not None:
            imagen = data.get('image')
        super().__init__(imagen=imagen, rect=rect, x=x, y=y, dz=z)
        self.solido = 'solido' in data.get('propiedades', [])
        self.proyectaSombra = 'proyecta_sombra' in data
        if data.get('proyecta_luz', False):
            self.luz = LightSource(self, *data['proyecta_luz'])
        self.descripcion = data.get('descripcion', "Esto es un ejemplo")
        self.face = data.get('cara', 'front')

        self.add_listeners()  # carga de event listeners

    def rotate_view(self, np):
        pass

    def __repr__(self):
        return "<%s sprite(%s)>" % (self.__class__.__name__, self.nombre)

    def show_description(self):
        PropDescription(self)


class Item:
    stackable = False
    tipo = ''

    def __init__(self, nombre, imagen, data):
        self.nombre = nombre
        self.image = imagen
        self.ID = data['ID']
        self.peso = data['peso']
        self.volumen = data['volumen']
        self.efecto_des = data['efecto']['des']
        self.stackable = 'stackable' in data['propiedades']

    def __eq__(self, other):
        if other.__class__ == self.__class__ and self.ID == other.ID:
            return True
        else:
            return False

    def __ne__(self, other):
        if other.__class__ != self.__class__:
            return True
        elif self.ID != other.ID:
            return True
        else:
            return False

    def __repr__(self):
        return self.nombre + ' (' + self.tipo + ')'

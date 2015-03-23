from engine.base import ShadowSprite, EventListener
from engine.misc import Util as U
from engine.misc import Resources as r
from pygame import mask as MASK
from .items import *


class Escenografia(ShadowSprite, EventListener):
    def __init__(self, nombre, imagen, x, y, data):
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
        super().__init__(imagen, x=x, y=y)
        self.solido = 'solido' in data.get('propiedades', [])
        self.proyectaSombra = data.get('proyecta_sombra', True)

        self.add_listeners()  # carga de event listeners

    def update(self):
        super().update()
        # self.dirty = 1


class Agarrable(Escenografia):
    def __init__(self, nombre, imagen, x, y, data):
        data.setdefault('proyecta_sombra', False)
        super().__init__(nombre, imagen, x, y, data)
        self.subtipo = data['subtipo']
        self.accion = 'agarrar'

    def __call__(self):
        args = self.nombre, self.image, self.data
        if self.subtipo == 'consumible':
            return Consumible(*args)
        elif self.subtipo == 'equipable':
            return Equipable(*args)
        elif self.subtipo == 'armadura':
            return Armadura(*args)
        elif self.subtipo == 'arma':
            return Arma(*args)
        elif self.subtipo == 'accesorio':
            return Accesorio(*args)
        elif self.subtipo == 'pocion':
            return Pocion(*args)

    def update(self):
        pass
        # self.dirty = 1


class Movible(Escenografia):
    def __init__(self, nombre, imagen, x, y, data):
        p = data.get('propiedades', ['solido'])
        if 'solido' not in p:
            p.append('solido')
            data['propiedades'] = p
        super().__init__(nombre, imagen, x, y, data)
        self.accion = 'mover'


class Trepable(Escenografia):
    def __init__(self, nombre, imagen, x, y, data):
        super().__init__(nombre, imagen, x, y, data)
        self.accion = 'trepar'


class Operable(Escenografia):
    estados = {}
    estado_actual = 0

    def __init__(self, nombre, imagen, x, y, data):
        data.setdefault('proyectar_sombra', False)
        p = data.get('propiedades', ['solido'])
        if 'solido' not in p:
            p.append('solido')
            data['propiedades'] = p
        super().__init__(nombre, imagen, x, y, data)
        # self._sprSombra._visible = self.proyectaSombra
        self.accion = 'operar'

        for estado in data['operable']:
            ID = estado['ID']
            self.estados[ID] = {}
            for attr in estado:
                if attr == 'image':
                    img = r.cargar_imagen(estado[attr])
                    mask = MASK.from_surface(img)
                    self.estados[ID].update({'image': img, 'mask': mask})
                elif attr == 'next':
                    self.estados[ID].update({'next': estado[attr]})
                else:
                    self.estados[ID].update({attr: estado[attr]})

        self.image = self.estados[self.estado_actual]['image']
        self.mask = self.estados[self.estado_actual]['mask']
        self.solido = self.estados[self.estado_actual]['solido']

    def operar(self):
        self.estado_actual = self.estados[self.estado_actual]['next']
        for attr in self.estados[self.estado_actual]:
            if hasattr(self, attr):
                setattr(self, attr, self.estados[self.estado_actual][attr])

    def update(self):
        pass
        # self.dirty = 1


class Destruible(Escenografia):
    def __init__(self, nombre, imagen, x, y, data):
        super().__init__(nombre, imagen, x, y, data)
        self.accion = 'romper'

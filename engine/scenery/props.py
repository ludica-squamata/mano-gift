from engine.base import ShadowSprite, EventListener
from engine.globs import ItemGroup, ModData
from engine.misc import Resources
from pygame import mask
from .items import *


class Escenografia(ShadowSprite, EventListener):
    accion = None

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
        try:
            dialogo = Resources.abrir_json(ModData.dialogos + self.nombre + '.json')
            self.data.update({'dialog': dialogo})
        except IOError:
            pass

        self.add_listeners()  # carga de event listeners


class Agarrable(Escenografia):
    def __init__(self, nombre, imagen, x, y, data):
        data.setdefault('proyecta_sombra', False)
        super().__init__(nombre, imagen, x, y, data)
        self.subtipo = data['subtipo']
        self.accion = 'agarrar'
        ItemGroup[self.nombre] = self

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


class Movible(Escenografia):
    def __init__(self, nombre, imagen, x, y, data):
        p = data.get('propiedades', ['solido'])
        if 'solido' not in p:
            p.append('solido')
            data['propiedades'] = p
        super().__init__(nombre, imagen, x, y, data)
        self.accion = 'mover'
        ItemGroup[self.nombre] = self

    def mover(self, dx, dy):
        col_mapa = False
        if self.stage.mapa.mask.overlap(self.mask, (self.mapX + dx, self.mapY)) is not None:
            col_mapa = True

        if self.stage.mapa.mask.overlap(self.mask, (self.mapX, self.mapY + dy)) is not None:
            col_mapa = True

        if not col_mapa:
            self.reubicar(dx, dy)
            return True

        return False


class Trepable(Escenografia):
    def __init__(self, nombre, imagen, x, y, data):
        super().__init__(nombre, imagen, x, y, data)
        self.accion = 'trepar'


class Operable(Escenografia):
    estados = {}
    estado_actual = 0

    def __init__(self, nombre, imagen, x, y, data):
        super().__init__(nombre, imagen, x, y, data)
        self.accion = 'operar'
        ItemGroup[self.nombre] = self

        for estado in data['operable']:
            idx = estado['ID']
            self.estados[idx] = {}
            for attr in estado:
                if attr == 'image':
                    img = Resources.cargar_imagen(estado[attr])
                    mascara = mask.from_surface(img)
                    self.estados[idx].update({'image': img, 'mask': mascara})
                elif attr == 'next':
                    self.estados[idx].update({'next': estado[attr]})
                else:
                    self.estados[idx].update({attr: estado[attr]})

        self.image = self.estados[self.estado_actual]['image']
        self.mask = self.estados[self.estado_actual]['mask']
        self.solido = self.estados[self.estado_actual]['solido']

    def operar(self):
        self.estado_actual = self.estados[self.estado_actual]['next']
        for attr in self.estados[self.estado_actual]:
            if hasattr(self, attr):
                setattr(self, attr, self.estados[self.estado_actual][attr])


class Destruible(Escenografia):
    def __init__(self, nombre, imagen, x, y, data):
        super().__init__(nombre, imagen, x, y, data)
        self.accion = 'romper'

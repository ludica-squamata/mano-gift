from engine.globs import Item_Group, ModData, GRUPO_OPERABLES, GRUPO_AGARRABLES, GRUPO_MOVIBLES, Tiempo
from engine.misc.resources import abrir_json, cargar_imagen
from .bases import Escenografia
from pygame import Rect
from .items import *

__all__ = ['Agarrable', 'Movible', 'Trepable', 'Operable', 'Destruible', 'EstructuraCompuesta', 'Escenografia']


class Agarrable(Escenografia):
    accionable = True

    def __init__(self, parent, x, y, z, data):
        data.setdefault('proyecta_sombra', False)
        super().__init__(parent, x, y, z=z, data=data)
        self.subtipo = data['subtipo']
        self.grupo = GRUPO_AGARRABLES
        Item_Group.add(self.nombre, self, self.grupo)

    def action(self, entity):
        item = self.return_item()
        if entity.tipo == 'Mob':
            entity.inventario.agregar(item)
            EventDispatcher.trigger('DeleteItem', 'Mob', {'obj': self})

        if "dialog" in self.data:
            ref = self.data['dialog']
            EventDispatcher.trigger('TookItem', 'Prop', {'who': entity,
                                                         'what': item,
                                                         'when': Tiempo.clock.timestamp(),
                                                         'about': ref})

    def return_item(self):
        args = self.parent, self.nombre, self.image, self.data
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
    accionable = False

    def __init__(self, parent, x, y, z, data):
        super().__init__(parent, x, y, z=z, data=data)
        self.grupo = GRUPO_MOVIBLES
        Item_Group.add(self.nombre, self, self.grupo)

    def action(self, *args, **kwargs):
        pass

    def mover(self, dx, dy):
        col_mapa = False
        # detectar colision contra otros props fijos, como la casa
        # if self.parent.mask.overlap(self.mask, (self.mapRect.x + dx, self.mapRect.y)) is not None:
        #     col_mapa = True
        #
        # if self.parent.mask.overlap(self.mask, (self.mapRect.x, self.mapRect.y + dy)) is not None:
        #     col_mapa = True

        if not col_mapa:
            self.reubicar(dx, dy)
            return True

        return False


class Trepable(Escenografia):
    accionable = True

    def __init__(self, parent, x, y, z, data):
        super().__init__(parent, x, y, z, data)
        self.accion = 'trepar'


class Operable(Escenografia):
    estados = {}
    estado_actual = 0
    enabled = True
    accionable = True

    def __init__(self, parent, x, y, z, data):
        self.estados = {}
        self.enabled = data.get('enabled', True)
        self.grupo = GRUPO_OPERABLES

        images = {}
        for estado in data['operable']:
            idx = estado['ID']
            self.estados[idx] = {}
            for attr in estado:
                if attr == 'image':
                    if estado[attr] not in images:
                        img = cargar_imagen(ModData.graphs + estado[attr])
                        images[estado[attr]] = img
                    else:
                        img = images[estado[attr]]
                    self.estados[idx].update({'image': img})
                elif attr == 'next':
                    self.estados[idx].update({'next': estado[attr]})
                elif attr == 'event':
                    f = ModData.get_script_method(self.data['script'], estado[attr])
                    self.estados[idx].update({'event': f})
                else:
                    self.estados[idx].update({attr: estado[attr]})

        super().__init__(parent, x, y, z=z, imagen=self.estados[0]['image'], data=data)
        Item_Group.add(self.nombre, self, self.grupo)

    def action(self, entity):
        if entity.tipo == 'Mob' and self.enabled:
            self.operar()

    def operar(self, estado=None):
        if estado is None:
            self.estado_actual = self.estados[self.estado_actual]['next']
        else:
            self.estado_actual = estado
        for attr in self.estados[self.estado_actual]:
            if hasattr(self, attr):
                setattr(self, attr, self.estados[self.estado_actual][attr])
            elif attr == 'event':
                self.estados[self.estado_actual][attr](self.nombre, self.estados[self.estado_actual])


class Destruible(Escenografia):
    def __init__(self, parent, x, y, z, data):
        super().__init__(parent, x, y, z=z, data=data)
        self.accion = 'romper'


class EstructuraCompuesta(Escenografia):
    def __init__(self, parent, x, y, data):
        self.x, self.y = x, y
        self.w, self.h = data['width'], data['height']
        self.rect = Rect(self.x, self.y, self.w, self.h)
        self.props = self.build_props(data, x, y)

        super().__init__(parent, x, y, data=data, rect=self.rect)
        self.proyectaSombra = data.get('proyecta_sombra', False)

    def build_props(self, data, dx, dy):
        from engine.scenery import new_prop
        props = []
        for nombre in data['componentes']:
            ruta = data['referencias'][nombre]
            imagen = None
            propdata = {}
            for x, y, z in data['componentes'][nombre]:
                if type(ruta) is dict:
                    propdata = ruta.copy()

                elif ruta.endswith('.json'):
                    propdata = abrir_json(ruta)

                elif ruta.endswith('.png'):
                    imagen = ruta

                prop = new_prop(self.parent, dx + x, dy + y, z=z, nombre=nombre, img=imagen, data=propdata)
                props.append(prop)

        return props

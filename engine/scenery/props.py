from engine.misc.resources import abrir_json, split_spritesheet, cargar_imagen
from engine.globs.eventDispatcher import EventDispatcher
from engine.globs import Item_Group, ModData
from engine.globs.renderer import Renderer
from .bases import Escenografia
from pygame import Rect
from .items import *

__all__ = ['Agarrable', 'Movible', 'Trepable', 'Operable', 'Destruible', 'Estructura3D', 'Escenografia']


class Agarrable(Escenografia):
    accionable = True

    def __init__(self, nombre, x, y, z, data):
        data.setdefault('proyecta_sombra', False)
        super().__init__(nombre, x, y, z, data)
        self.subtipo = data['subtipo']
        Item_Group[self.nombre] = self

    def action(self, entity):
        if entity.tipo == 'Mob':
            item = self.return_item()
            entity.inventario.agregar(item)
            EventDispatcher.trigger('DeleteItem', 'Mob', {'obj': self})

    def return_item(self):
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
    accionable = True

    def __init__(self, nombre, x, y, z, data):
        super().__init__(nombre, x, y, z, data)
        Item_Group[self.nombre] = self

    def mover(self, dx, dy):
        col_mapa = False
        if self.stage.mapa.mask.overlap(self.mask, (self.mapRect.x + dx, self.mapRect.y)) is not None:
            col_mapa = True

        if self.stage.mapa.mask.overlap(self.mask, (self.mapRect.x, self.mapRect.y + dy)) is not None:
            col_mapa = True

        if not col_mapa:
            self.reubicar(dx, dy)
            return True

        return False

    def update(self):
        super().update()
        x, y = self.mapRect.x // 32, self.mapRect.y // 32
        self.stage.grilla.set_transitable((x, y), False)


class Trepable(Escenografia):
    accionable = True

    def __init__(self, nombre, x, y, z, data):
        super().__init__(nombre, x, y, z, data)
        self.accion = 'trepar'


class Operable(Escenografia):
    estados = {}
    estado_actual = 0
    enabled = True
    accionable = True

    def __init__(self, nombre, x, y, z, data):
        super().__init__(nombre, x, y, z, data)
        self.estados = {}
        self.enabled = self.data.get('enabled', True)
        Item_Group[self.nombre] = self

        for estado in data['operable']:
            idx = estado['ID']
            self.estados[idx] = {}
            for attr in estado:
                if attr == 'image':
                    img = cargar_imagen(estado[attr])
                    # mascara = mask.from_surface(img)
                    self.estados[idx].update({'image': img})
                elif attr == 'next':
                    self.estados[idx].update({'next': estado[attr]})
                elif attr == 'event':
                    f = ModData.get_script_method(self.data['script'], estado[attr])
                    self.estados[idx].update({'event': f})
                else:
                    self.estados[idx].update({attr: estado[attr]})

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
    def __init__(self, nombre, x, y, z, data):
        super().__init__(nombre, x, y, z, data)
        self.accion = 'romper'


class Estructura3D(Escenografia):
    faces = {}
    face = 'front'
    _chopped = False

    def __init__(self, nombre, x, y, data):
        self.nombre = nombre
        self.faces = {'front': None, 'right': None, 'back': None, 'left': None}
        self.face = data.get('cara', 'front')
        self.x, self.y = x, y
        self.w, self.h = data['width'], data['height']
        self.rect = Rect(self.x, self.y, self.w, self.h)

        for face in data['componentes']:
            if len(data['componentes'][face]):
                self.faces[face] = self.build_face(data, x, y, face)

        self.props = self.faces[self.face]
        super().__init__(nombre, x, y, data=data, rect=self.rect)
        self.proyectaSombra = False
        EventDispatcher.register(self.rotate_view, 'RotateEverything')

    def build_face(self, data, dx, dy, face):
        from engine.scenery import new_prop
        props = []
        for nombre in data['componentes'][face]:
            ruta = data['referencias'][nombre]
            imagen = None
            propdata = {}
            for x, y, z in data['componentes'][face][nombre]:
                if type(ruta) is dict:
                    propdata = ruta.copy()

                elif ruta.endswith('.json'):
                    propdata = abrir_json(ruta)

                elif ruta.endswith('.png'):
                    w, h = data['width'], data['height']
                    faces = self.chop_faces(ruta, w=w, h=h, required_face=face)
                    imagen = faces[face]

                if 'cara' not in propdata:
                    propdata.update({'cara': face})

                prop = new_prop(nombre, dx + x, dy + y, z=z, img=imagen, data=propdata)
                props.append(prop)

        return props

    def chop_faces(self, ruta_img, w, h, required_face='front'):
        if not self._chopped:
            spritesheet = split_spritesheet(ruta_img, w=w, h=h)
            d = {}
            if len(spritesheet) > 1:
                for idx, face in enumerate(['front', 'left', 'right', 'back']):
                    d[face] = spritesheet[idx]
            else:
                # print('aca',required_face)
                d[required_face] = spritesheet[0]
            # self._chopped = d
            return d
        else:
            return self._chopped

    def rotate_view(self, event):
        np = event.data['view']
        objects_faces = ['front', 'right', 'back', 'left']
        idx = objects_faces.index(self.face)
        temp = [objects_faces[idx]] + objects_faces[idx + 1:] + objects_faces[:idx]

        for prop in self.faces[self.face]:
            Renderer.camara.remove_obj(prop)

        self.face = temp[np]

        for prop in self.faces[self.face]:
            Renderer.camara.add_real(prop)

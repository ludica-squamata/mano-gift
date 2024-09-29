from engine.globs import Item_Group, ModData, GRUPO_OPERABLES, GRUPO_AGARRABLES, GRUPO_MOVIBLES, Tagged_Items, Tiempo
from engine.globs.event_dispatcher import EventDispatcher
from engine.misc.resources import abrir_json, cargar_imagen
from .bases import Escenografia
from pygame import Rect

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
        from .new_prop import new_item
        item = new_item(self.parent, self.nombre, self.data)
        item.is_colocable = True  # si fue agarrable en algún momento, es por lo tanto también colocable.
        if entity.tipo == 'Mob':
            entity.inventario.agregar(item)
            # removes the prop from the map, but not the item from the world.
            EventDispatcher.trigger('DeleteItem', 'Prop', {'obj': self})

        if "dialog" in self.data:
            ref = self.data['dialog']
            EventDispatcher.trigger('TookItem', 'Prop', {'who': entity,
                                                         'what': item,
                                                         'when': Tiempo.clock.timestamp(),
                                                         'about': ref})


class Movible(Escenografia):
    accionable = False

    def __init__(self, parent, x, y, z, data):
        super().__init__(parent, x, y, z=z, data=data)
        self.grupo = GRUPO_MOVIBLES
        Item_Group.add(self.nombre, self, self.grupo)
        Tagged_Items.add_item(self, 'movibles')

    def mover(self, dx, dy):
        col_mapa = False
        # detectar colision contra las cajas de colision del propio mapa
        if self.parent.mask.overlap(self.mask, (self.rel_x + dx, self.rel_y)) is not None:
            col_mapa = True

        if self.parent.mask.overlap(self.mask, (self.rel_x, self.rel_y + dy)) is not None:
            col_mapa = True

        if not col_mapa:
            self.reubicar(dx, dy)
            return True

        return False


class Trepable(Escenografia):
    accionable = True
    salida = None

    def __init__(self, parent, x, y, z, data):
        super().__init__(parent, x, y, z=z, data=data)
        self.accion = 'trepar'
        Tagged_Items.add_item(self, 'trepables')

    def action(self, entity):
        # acá debería iniciar una animación del mob trepando.
        if self.salida is not None:
            self.salida.trigger(entity)


class Operable(Escenografia):
    estados = {}
    estado_actual = 0
    enabled = True
    accionable = True

    def __init__(self, parent, x, y, z, data):
        self.estados = {}
        self.enabled = data.get('enabled', True)
        self.grupo = GRUPO_OPERABLES
        Tagged_Items.add_item(self, 'operables')
        if 'AI' in data:
            # issue #109, item 5. Los props operables deberían tener un árbol de comportamiento como los mobs.
            self.AI = abrir_json(ModData.mobs + 'behaviours/' + data['AI'] + '.json')
            # probablemente no esté en mobs/behaviours junto a las AIs de los mobs, sino en una carpeta separada.
            # pero eso requería crear una nueva propiedad de ModData...

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
        Tagged_Items.add_item(self, 'destruibles')


class EstructuraCompuesta(Escenografia):
    def __init__(self, parent, x, y, data):
        self.x, self.y = x, y
        self.w, self.h = data['width'], data['height']
        self.rect = Rect(self.x, self.y, self.w, self.h)
        self.proyectaSombra = data.get('proyecta_sombra', False)
        self.props = self.build_props(parent, data, x, y)

        super().__init__(parent, x, y, data=data, rect=self.rect)

    def build_props(self, parent, data, dx, dy):
        from engine.scenery import new_prop
        props = []
        for nombre in data['componentes']:
            ruta = data['referencias'][nombre]
            imagen = None
            propdata = {'propiedades': []}
            for x, y, z in data['componentes'][nombre]:
                if type(ruta) is dict:
                    propdata = ruta.copy()

                elif ruta.endswith('.json'):
                    propdata = abrir_json(ModData.items + ruta)

                elif ruta.endswith('.png'):
                    imagen = ruta

                if not self.proyectaSombra:
                    propdata['propiedades'].append('sin_sombra')

                prop = new_prop(parent, dx + x, dy + y, z=z, nombre=nombre, img=imagen, data=propdata)
                props.append(prop)

        return props

from engine.globs import Prop_Group, ModData, Tiempo, Tagged_Items, Mob_Group
from engine.globs import GRUPO_OPERABLES, GRUPO_AGARRABLES, GRUPO_MOVIBLES, COLOR_COLISION
from engine.misc.resources import abrir_json, cargar_imagen, split_spritesheet
from engine.globs.event_dispatcher import EventDispatcher
from engine.UI.circularmenus import ContainerCircularMenu
from pygame import Rect, mask as mask_module
from .bases import Escenografia
from itertools import cycle

__all__ = ['Agarrable', 'Movible', 'Trepable', 'Operable', 'Destruible',
           'EstructuraCompuesta', 'Escenografia', 'Contenedor', 'Transicional']


class Agarrable(Escenografia):
    accionable = True

    def __init__(self, parent, x, y, z, data):
        self.prop_type = 'Agarrable'
        data.setdefault('proyecta_sombra', False)
        super().__init__(parent, x, y, z=z, data=data)
        self.subtipo = data['subtipo']
        self.grupo = GRUPO_AGARRABLES
        Prop_Group.add(self.nombre, self, self.grupo)

    def action(self, entity):
        from .new_prop import new_item
        item = new_item(self.parent, self.data)
        if entity.tipo == 'Mob':
            entity.inventario.agregar(item)
            # removes the prop from the map, but not the item from the world.
            EventDispatcher.trigger('DeleteItem', 'Prop', {'obj': self})

            # plays the pick up sound (WIP).
            EventDispatcher.trigger('PlaySound', self, {'sound': 'pick up'})

        if "dialog" in self.data:
            ref = self.data['dialog']
            EventDispatcher.trigger('TookItem', 'Prop', {'who': entity,
                                                         'what': item,
                                                         'when': Tiempo.clock.timestamp(),
                                                         'about': ref})


class Movible(Escenografia):
    accionable = False

    def __init__(self, parent, x, y, z, data):
        self.prop_type = 'Movible'
        super().__init__(parent, x, y, z=z, data=data)
        self.grupo = GRUPO_MOVIBLES
        Prop_Group.add(self.nombre, self, self.grupo)
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
        self.prop_type = 'Trepable'
        super().__init__(parent, x, y, z=z, data=data)
        self.accion = 'trepar'
        Prop_Group.add(self.nombre, self, self.grupo)
        Tagged_Items.add_item(self, 'trepables')

    def action(self, entity):
        # acá debería iniciar una animación del mob trepando.
        if self.salida is not None:
            self.salida.trigger(entity, self.accion)


class Operable(Escenografia):
    estados = {}
    estado_actual = 0
    enabled = True
    accionable = True

    def __init__(self, parent, x, y, z, data):
        self.prop_type = 'Operable'
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
        Prop_Group.add(self.nombre, self, self.grupo)

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
        self.prop_type = 'Destruible'
        super().__init__(parent, x, y, z=z, data=data)
        self.accion = 'romper'
        Tagged_Items.add_item(self, 'destruibles')
        Prop_Group.add(self.nombre, self, self.grupo)


class EstructuraCompuesta(Escenografia):
    accionable = True

    def __init__(self, parent, x, y, data):
        self.prop_type = 'EstructuraCompuesta'
        self.x, self.y = x, y
        self.w, self.h = data['width'], data['height']
        self.rect = Rect(self.x, self.y, self.w, self.h)
        self.proyectaSombra = data.get('proyecta_sombra', False)
        self.props = self.build_props(parent, data, x, y)
        Prop_Group.add(self.nombre, self, self.grupo)
        self.accion = 'entrar'

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

                if nombre == 'colisiones':
                    ruta = ModData.graphs + imagen
                    self.mask = mask_module.from_threshold(cargar_imagen(ruta), COLOR_COLISION, [1, 1, 1, 255])
                    parent.mask.draw(self.mask, [x, y])
                    imagen = None

                elif not self.proyectaSombra:
                    propdata['propiedades'].append('sin_sombra')

                if imagen is not None:
                    prop = new_prop(parent, dx + x, dy + y, z=z, nombre=nombre, img=imagen, data=propdata)
                    props.append(prop)

        return props

    def action(self, entity):
        # acá debería iniciar una animación del mob trepando.
        if self.salida is not None:
            self.salida.trigger(entity, self.accion)


class Contenedor(Operable):
    accionable = True
    entity = None

    def __init__(self, parent, x, y, z, data):
        self.prop_type = 'Contenedor'
        from engine.mobs.inventory import Inventory
        super().__init__(parent, x, y, z, data=data)
        self.inventario = Inventory()
        self._fill(data['contenido'])
        self.menu = None

    def action(self, mob):
        super().operar()
        if mob is Mob_Group.get_controlled_mob():
            if len(self.inventario):
                self.entity = mob
                EventDispatcher.trigger('Deregister', self, {'mob': mob})
                self.menu = ContainerCircularMenu(self)

    def close(self):
        self.operar(estado=0)

    def _fill(self, contenido):
        from .new_prop import new_item
        for item_name in contenido:
            data = abrir_json(ModData.items + '/' + item_name + '.json')
            for _ in range(contenido[item_name]):
                item = new_item(self, data)
                self.inventario.agregar(item)


class Transicional(Escenografia):
    imgs_summer = None
    imgs_autumn = None
    imgs_winter = None
    imgs_spring = None

    current_season = 'summer'

    wind_strength = 0
    timer_animacion = 0
    frame_animacion = 0

    current_cyler = None

    summer_cycler = None
    autumn_cycler = None
    winter_cycler = None
    spring_cycler = None

    enabled = True

    def __init__(self, parent, x, y, data):
        self.prop_type = 'Transisional'
        self.x, self.y = x, y
        self.frame_animacion = 1000 / 20
        self.proyectaSombra = data.get('proyecta_sombra', False)
        image = self.create(data['spritesheet'])
        self.colisiones(parent, *data['colisión'])
        super().__init__(parent, x, y, data=data, imagen=image)
        Prop_Group.add(self.nombre, self, self.grupo)
        EventDispatcher.register(self.set_season_images, 'UpdateTime')

    def create(self, image_dir):
        spritesheet = split_spritesheet(ModData.graphs + image_dir, 113, 136)
        self.imgs_summer = spritesheet[0], spritesheet[4], spritesheet[8]
        self.imgs_autumn = spritesheet[1], spritesheet[5], spritesheet[9]
        self.imgs_winter = spritesheet[2], spritesheet[6], spritesheet[10]
        self.imgs_spring = spritesheet[3], spritesheet[7], spritesheet[11]
        self.summer_cycler = cycle(self.imgs_summer)
        self.autumn_cycler = cycle(self.imgs_autumn)
        self.winter_cycler = cycle(self.imgs_winter)
        self.spring_cycler = cycle(self.imgs_spring)

        # set the cyclers to the start of the seasons
        next(self.summer_cycler)
        next(self.autumn_cycler)
        next(self.winter_cycler)
        next(self.spring_cycler)

        self.current_cyler = self.summer_cycler

        return spritesheet[0]

    def colisiones(self, parent, x, y, w, h):
        mask = mask_module.Mask([w, h])
        mask.fill()
        parent.mask.draw(mask, [x + self.x, y + self.y])

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def set_season_images(self, event):
        current_season = event.data['current_season']
        if current_season != self.current_season:
            self.current_season = current_season
            if self.current_season == 'summer':
                self.current_cyler = self.summer_cycler
                next(self.spring_cycler)  # resets the previous season's cycler
            elif self.current_season == 'autumn':
                self.current_cyler = self.autumn_cycler
                next(self.summer_cycler)
            elif self.current_season == 'winter':
                self.current_cyler = self.winter_cycler
                next(self.autumn_cycler)
            elif self.current_season == 'spring':
                self.current_cyler = self.spring_cycler
                next(self.winter_cycler)

            self.image = next(self.current_cyler)

    def set_animation_framerate(self, value: int):
        self.frame_animacion = 1000 / value

    def animate(self):
        self.timer_animacion += 1
        if self.timer_animacion >= self.frame_animacion and self.enabled:
            self.timer_animacion = 0
            self.image = next(self.current_cyler)

    def update(self, *args):
        super().update(*args)
        self.animate()

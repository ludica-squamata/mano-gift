from engine.globs.event_dispatcher import EventDispatcher
from engine.misc.resources import split_spritesheet
from engine.globs import Item_Group, ModData
from pygame import transform
from .bases import Item


class Tradeable(Item):
    price_sell = 0
    price_buy = 0
    coin = None

    def __init__(self, parent, data):
        super().__init__(parent, data)
        if "trading" in data:
            self.price_sell = data['trading']['sell_price']
            self.price_buy = data['trading']['buy_price']
            self.coin = data['trading']['coin_symbol']


class Equipable(Tradeable):
    def __init__(self, parent, data):
        super().__init__(parent, data)
        self.tipo = 'equipable'
        self.subtipo = data['subtipo']
        self.espacio = data['efecto']['equipo']
        Item_Group.add(self.nombre, self, self.tipo)


class Consumible(Tradeable):
    def __init__(self, parent, data):
        super().__init__(parent, data)
        self.tipo = 'consumible'
        self.data = data
        Item_Group.add(self.nombre, self, self.tipo)

    def usar(self, mob):
        stat = self.data.get('efecto', {}).get('stat', '')
        mod = self.data.get('efecto', {}).get('mod', '')
        method = self.data.get('efecto', {}).get('method', '')
        valor = 0

        if method == 'percentage':
            valmaximo = mob[stat + 'Max']
            valactual = mob[stat]
            valor = int((mod * valmaximo) / 100)
            if valor + valactual > valmaximo:
                valor = valmaximo
            else:
                valor += valactual

            mob[stat] = valor

        elif method == 'incremental':
            actual = mob[stat]
            valor = actual + mod
            mob[stat] = valor

        m, s, v, f, h = 'mob', 'stat', 'value', 'factor', 'method'
        EventDispatcher.trigger('UsedItem', self.nombre, {m: mob, s: stat, v: valor, f: mod, h: method})
        EventDispatcher.trigger('PlaySound', self, {'sound': 'powerup'})
        return mob.inventario.remover(self)


class Utilizable(Tradeable):
    def __init__(self, parent, data):
        super().__init__(parent, data)
        self.tipo = "utilizable"
        Item_Group.add(self.nombre, self, self.tipo)


libros = {}


def load_book_spritesheet():
    global libros
    ruta = ModData.graphs + 'items/libros_spritesheet.png'
    imagenes = split_spritesheet(ruta, 24, 24)
    for i, color in enumerate('azul,rojo,verde,amarillo,cian,magenta'.split(',')):
        libros[color] = {}
        for j, key in enumerate('abajo,item,paginas,canto,derecha'.split(',')):
            libros[color][key] = imagenes[(i * 5) + j]
        libros[color]['prop'] = transform.rotate(imagenes[(i * 5) + 3],90)
        libros[color]['izquierda'] = transform.flip(imagenes[(i * 5) + 4], True, False)

class Libro(Utilizable):
    # inicialización
    words = 0  # aribitary
    difficulty = 0  # 0–100
    technicality = 0  # 0–100
    quality = 0  # calidad del libro 0–100
    subtipo = "libro"

    def __init__(self, parent, data:dict):
        self.words = data['book']['words']
        self.difficulty = data['book']['difficulty']  # 0–100
        self.technicality = data['book']['technicality']  # 0–100
        self.quality = data['book']['quality']  # 0–100
        self.integrity = data['book']['integrity']  # 0–100
        self.reading_mode = data['book']['reading_mode']  # linear or reference

        if data['color'] not in libros:
            load_book_spritesheet()
        data.update({'imagenes':libros[data['color']]})

        super().__init__(parent, data)

        self.posisiones = {
            'abajo':[4,5],
            'izquierda':[3,10],
            'derecha':[3,10]
        }

        # event triggers
        self.on_open = []
        self.on_read_tick = []
        self.on_finish = []

        on_open = data['effects']['on_open']
        on_read_tick = data['effects']['on_read_tick']
        on_finish = data['effects']['on_finish']
        if on_open is not None:
            color, value = on_open
            self.on_open = [Effect(color, value)]

        if on_read_tick is not None:
            color, value = on_read_tick
            self.on_read_tick = [Effect(color, value)]

        if on_finish is not None:
            color, value = on_finish
            self.on_finish = [Effect(color, value)]

    def integrity_loss_per_minute(self):
        loss = 0.01
        self.integrity = max(0, self.integrity - loss)

class Effect:
    def __init__(self, color, value):
        self.color = color
        self.value = value

    def apply(self,mob):
        mob.afinidades[self.color].incrementar_por(self.value)


class Colocable(Item):
    def __init__(self, parent, entity, data, item):
        super().__init__(parent, data)
        self.tipo = 'colocable'
        self.entity = entity
        self.item = item

    # noinspection unresolved-references
    def action(self):
        from .new_prop import new_prop
        x, y, z = self._get_placement_position()
        prop = new_prop(self.parent.parent, x, y, z, self.nombre, self.data)
        self.parent.inventario.remover(self.item)
        self.parent.parent.parent.place_placeable_props(prop)
        return prop

    # noinspection unresolved-references
    def _get_placement_position(self):
        """Establece las coordinadas donde aparecerá el prop relativas al mob que lo colocó.

        Aún no funciona completamente bien."""

        x, y, z = 0, 0, 0
        w, h = self.rect.size
        if self.parent.body_direction == 'abajo':
            x = int(self.parent.rel_x)
            y = int(self.parent.rel_y + h)
            z = int(self.parent.rect.bottom + h // 2)
        elif self.parent.body_direction == 'arriba':
            x = self.parent.rel_x
            y = self.parent.rel_y - h // 2
            z = self.parent.rect.top + h // 2
        elif self.parent.body_direction == 'izquierda':
            x = self.parent.rect.left + w // 2
            y = self.parent.rel_y
            z = self.parent.rect.centery
        elif self.parent.body_direction == 'derecha':
            x = self.parent.rel_x + w // 2
            y = self.parent.rel_y
            z = self.parent.rect.centery

        return x, y, z


class Armadura(Equipable):
    def __init__(self, parent, data):
        super().__init__(parent, data)
        self.proteccion = data['efecto']['proteccion']


class Arma(Equipable):
    def __init__(self, parent, data):
        super().__init__(parent, data)


class Accesorio(Equipable):
    def __init__(self, parent, data):
        super().__init__(parent, data)


class Pocion(Consumible):
    def __init__(self, parent, data):
        super().__init__(parent, data)

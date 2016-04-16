from pygame import mask, Rect, font, draw
from engine.libs import render_textrect


class Nodo:
    g, f = 0, 0
    x, y = 0, 0
    transitable = True
    image = None
    is_default = True

    def __init__(self, x, y, value=True):
        self.x = x
        self.y = y
        self.rect = Rect((x * 32, y * 32), (32, 32))
        self.img_t = self.create_image(32, 32, (0, 255, 0))
        self.img_i = self.create_image(32, 32, (255, 0, 0))
        self.set_transitable(value)
        self._default = value

    def create_image(self, w, h, color):
        fuente = font.SysFont('Verdana', 10)
        s = '\n'.join([str(self.x), str(self.y)])
        render = render_textrect(s, fuente, self.rect, (0, 0, 0), color, 1)
        draw.rect(render, (0, 0, 0), (0, 0, w - 1, h - 1), 1)
        return render

    def set_transitable(self, value):
        self.transitable = value
        if value:
            self.image = self.img_t
        else:
            self.image = self.img_i
        self.is_default = False
    
    def restore_status(self):
        self.set_transitable(self._default)
        self.is_default = True

    def __bool__(self):
        return self.transitable

    def __repr__(self):
        return 'Nodo ' + str(self.x) + ',' + str(self.y) + '(' + str(self.transitable) + ')'

    def __str__(self):
        return 'Nodo ' + str(self.x) + ',' + str(self.y) + '(' + str(self.transitable) + ')'


class Grilla:
    _cuadros = None
    _indexes = None
    _index = 0
    _lenght = 0
    _modified = []

    def __init__(self, mascara, t):
        self._cuadros = {}
        self._indexes = []
        self._modified = []

        self.create(mascara, t)

    def create(self, mascara, t):
        w, h = mascara.get_size()
        test = mask.Mask((t, t))
        test.fill()
        for y in range(h // t):
            for x in range(w // t):
                self._indexes.append((x, y))
                self._lenght += 1
                if mascara.overlap(test, (x * t, y * t)):
                    self._cuadros[x, y] = Nodo(x, y, False)
                else:
                    self._cuadros[x, y] = Nodo(x, y, True)

    def update(self):
        for item in self._modified:
            self._cuadros[item].restore_status()
        self._modified.clear()
    
    def set_transitable(self,item,value):
        if item in self._cuadros:
            self._cuadros[item].set_transitable(value)
            if item not in self._modified:
                self._modified.append(item)
        
    def __getitem__(self, item):
        if type(item) is int:
            if 0 <= item <= self._lenght:
                return self._cuadros[self._indexes[item]]

        elif type(item) is tuple:
            if item in self._cuadros:
                return self._cuadros[item]

    def __contains__(self, item):
        if type(item) is int:
            if 0 <= item <= self._lenght:
                return True
        if item in self._cuadros:
            return True
        return False

    def __iter__(self):
        return self

    def __next__(self):
        key = self._indexes[self._index]
        if self._index + 1 < len(self._indexes):
            self._index += 1
            result = self._cuadros[key]

        else:
            self._index = 0
            raise StopIteration

        return result

    def __len__(self):
        return self._lenght

    def __repr__(self):
        return 'Grilla'

    def draw(self, image):
        for (x, y) in self._cuadros:
            cuadro = self._cuadros[x, y]
            image.blit(cuadro.image, cuadro.rect)
        return image

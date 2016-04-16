# A* module
from pygame import mask, Rect, font, draw
from random import choice
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


def a_star(inicio, destino, mapa):
    cerrada = []  # The set of nodes already evaluated.
    abierta = [inicio]  # The set of tentative nodes to be evaluated, initially containing the start node
    camino = {}  # The map of navigated nodes.

    inicio.g = 0  # Cost from start along best known path.
    # Estimated total cost from start to goal through y.
    inicio.f = inicio.g + heuristica_estimada(inicio, destino)

    while abierta:
        actual = lowest_f(abierta)  # the node in openset having the lowest f_score[] value
        if actual == destino:
            return reconstruir_camino(camino, destino)

        abierta.remove(actual)
        cerrada.append(actual)

        vecinos = mirar_vecinos(actual, mapa)
        for vecino in vecinos:
            punt_g_tentativa = actual.g + costo_g(actual, vecino)
            if vecino not in cerrada or punt_g_tentativa < vecino.g:
                camino[vecino] = actual
                vecino.g = punt_g_tentativa
                vecino.f = vecino.g + heuristica_estimada(vecino, destino)
                if vecino not in abierta:
                    abierta.append(vecino)


def heuristica_estimada(node, goal):
    return 10 * (abs(node.x - goal.x) + abs(node.y - goal.y))


def costo_g(actual, vecino):
    if actual.x - vecino.x != 0 and actual.y - vecino.y != 0:  # diagonal
        return 14
    else:
        return 10


def lowest_f(abierta):
    # returns the node in openset having the lowest f_score value
    f_min = min([nodo.f for nodo in abierta])
    candidatos = []
    elegido = None
    for nodo in abierta:
        if nodo.f == f_min:
            candidatos.append(nodo)
            elegido = nodo

    if len(candidatos) > 1:  # empate
        return choice(candidatos)
    else:
        return elegido


def mirar_vecinos(nodo, grilla):
    cuadros = []
    direcciones = ((0, -1), (1, -1), (1, 0), (1, 1), (-1, 1), (-1, 0), (-1, -1), (0, 1))
    for dx, dy in direcciones:
        x, y = nodo.x + dx, nodo.y + dy
        if (x, y) in grilla:
            n = grilla[x, y]
            if n:
                cuadros.append(n)

    return cuadros


def reconstruir_camino(camino, nodo_actual):
    if nodo_actual in camino:
        nodo = camino[nodo_actual]
        p = reconstruir_camino(camino, nodo)
        p.append(nodo_actual)
        return p
    else:
        return [nodo_actual]

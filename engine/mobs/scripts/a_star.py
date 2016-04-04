# A* module
from pygame import mask, Rect
from random import choice


class Nodo:
    g, f = 0, 0
    x, y = 0, 0
    transitable = True

    def __init__(self, x, y, t, value=True):
        self.x = x
        self.y = y
        self.transitable = value
        self.rect = Rect(x,y,t,t)

    def set_transitable(self, value):
        self.transitable = value

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

    def __init__(self, mascara, t):
        w, h = mascara.get_size()
        self._cuadros = {}
        self._indexes = []

        test = mask.Mask((t, t))
        test.fill()

        for y in range(h // t):
            for x in range(w // t):
                self._indexes.append((x, y))
                self._lenght += 1
                if mascara.overlap(test, (x * t, y * t)):
                    self._cuadros[x, y] = Nodo(x, y, False)
                else:
                    self._cuadros[x, y] = Nodo(x, y True)

    def __getitem__(self, item):
        if type(item) is int:
            if 0 <= item <= self._lenght:
                return self._cuadros[self._indexes[item]]

        elif type(item) is tuple:
            if item in self._cuadros:
                return self._cuadros[item]

    def __setitem__(self, key, value):
        pass

    def __delitem__(self, key):
        pass

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

# A* module
from math import sqrt
from pygame import mask


def a_star(inicio, destino, mapa, others, heuristica='euclidean'):
    cerrada = []  # The set of nodes already evaluated.
    abierta = [inicio]  # The set of tentative nodes to be evaluated, initially containing the start node
    camino = {}  # The map of navigated nodes.

    # inicio.g = 0  # Cost from start along best known path.
    # Estimated total cost from start to goal through y.
    inicio.f = heuristica_estimada(inicio, destino, heuristica)

    while abierta:
        abierta.sort(key=lambda nodo: nodo.f)
        actual = abierta.pop(0)  # the node in openset having the lowest f_score[] value
        if actual == destino:
            return reconstruir_camino(camino, destino)

        cerrada.append(actual)

        vecinos = mirar_vecinos(actual, 32, mapa, others)
        for vecino in vecinos:
            punt_g_tentativa = actual.g + vecino.g
            if vecino not in cerrada or punt_g_tentativa < vecino.g:
                vecino.g = punt_g_tentativa
                vecino.f = vecino.g + heuristica_estimada(vecino, destino, heuristica)
                camino[vecino] = actual
                if vecino not in abierta:
                    abierta.append(vecino)


def heuristica_estimada(node, goal, method):
    if method == 'manhattan':
        return abs(node.x - goal.x) + abs(node.y - goal.y)
    elif method == 'euclidean':
        return int(sqrt((node.x - goal.x) ** 2 + (node.y - goal.y) ** 2))


def mirar_vecinos(nodo, size, mascara, others):
    cuadros = []
    test = mask.Mask((size, size))
    test.fill()
    direcciones = ((0, -1), (1, 0), (0, 1), (-1, 0))
    mascara_actual = mascara.copy()
    for other in others:
        mascara_actual.draw(other.mask, other.rect.topleft)

    for dx, dy in direcciones:
        x, y = nodo.x + (dx * size), nodo.y + (dy * size)
        vecino = Nodo(x, y, size)
        if not mascara_actual.overlap(test, (x, y)):
            cuadros.append(vecino)

    return cuadros


def reconstruir_camino(camino, nodo_actual):
    if nodo_actual in camino:
        nodo = camino[nodo_actual]
        p = reconstruir_camino(camino, nodo)
        p.append(nodo_actual)
        return p
    else:
        return [nodo_actual]


def determinar_direccion(curr_p, next_p):
    px, py = curr_p
    nx, ny = next_p

    dx = px - nx
    dy = py - ny

    if dx > dy:
        if dy < 0:
            direccion = 'abajo'
        else:
            direccion = 'izquierda'
    else:
        if dx < 0:
            direccion = 'derecha'
        else:
            direccion = 'arriba'

    return direccion


class Nodo:
    x = 0
    y = 0
    f = 0
    g = 0
    transitable = True

    def __init__(self, x, y, size):
        self.s = size
        self.x = x
        self.y = y

    def __repr__(self):
        return '(' + str(self.x) + ',' + str(self.y) + ') f: ' + str(self.f)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y, self.s))

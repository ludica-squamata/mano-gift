# A* module
from pygame import mask
from random import choice


class Nodo:
    g, f = 0, 0
    x, y = 0, 0
    transitable = True

    def __init__(self, x, y, boole=True):
        self.x = x
        self.y = y
        self.transitable = boole

    def __repr__(self):
        return 'Nodo ' + str(self.x) + ',' + str(self.y) + '(' + str(self.transitable) + ')'

    def __str__(self):
        return str((self.x, self.y))


def generar_grilla(mascara, imagen):
    ancho = imagen.get_width()
    alto = imagen.get_height()

    tamanio = w, h = 32, 32
    _test = mask.Mask(tamanio)
    _test.fill()

    cuadros = {}
    for y in range(int(alto / h)):
        for x in range(int(ancho / w)):
            if mascara.overlap(_test, (x * 32, y * 32)):
                cuadros[x, y] = Nodo(x, y, False)
            else:
                cuadros[x, y] = Nodo(x, y, True)
    return cuadros


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
            if n.transitable:
                cuadros.append(n)

    return cuadros


def reconstruir_camino(camino, nodo_actual):
    if nodo_actual in camino:
        p = reconstruir_camino(camino, camino[nodo_actual])
        return str(p) + ';' + str(nodo_actual)
    else:
        return nodo_actual

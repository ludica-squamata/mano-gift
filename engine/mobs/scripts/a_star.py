# A* module
from math import sqrt


def a_star(inicio, destino, mapa, heuristica='manhattan'):
    cerrada = []  # The set of nodes already evaluated.
    abierta = [inicio]  # The set of tentative nodes to be evaluated, initially containing the start node
    camino = {}  # The map of navigated nodes.

    inicio.g = 0  # Cost from start along best known path.
    # Estimated total cost from start to goal through y.
    inicio.f = inicio.g + heuristica_estimada(inicio, destino, heuristica)

    while abierta:
        abierta.sort(key=lambda nodo: nodo.f)
        actual = abierta.pop(0)  # the node in openset having the lowest f_score[] value
        if actual == destino:
            return reconstruir_camino(camino, destino)

        cerrada.append(actual)

        vecinos = mirar_vecinos(actual, mapa)
        for vecino in vecinos:
            punt_g_tentativa = actual.g + vecino.g
            if vecino not in cerrada or punt_g_tentativa < vecino.g:
                camino[vecino] = actual
                vecino.g = punt_g_tentativa
                vecino.f = vecino.g + heuristica_estimada(vecino, destino, heuristica)
                if vecino not in abierta:
                    abierta.append(vecino)


def heuristica_estimada(node, goal, method):
    if method == 'manhattan':
        return abs(node.x - goal.x) + abs(node.y - goal.y)
    elif method == 'euclidean':
        return int(sqrt((node.x - goal.x)**2+(node.y - goal.y)**2))


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

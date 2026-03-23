# A* module
from math import sqrt
from pygame import mask
import heapq

# CACHE GLOBAL DE NODOS
nodos_cache = {}


def get_nodo(x, y, size):
    key = (x, y, size)
    if key not in nodos_cache:
        nodos_cache[key] = Nodo(x, y, size)
    return nodos_cache[key]


def a_star(inicio, destino, mapa, others, heuristica='euclidean'):
    cerrada = set()
    abierta = []
    camino = {}

    inicio.g = 0
    inicio.f = heuristica_estimada(inicio, destino, heuristica)

    heapq.heappush(abierta, inicio)

    w, h = mapa.get_size()
    MAX_ITER = w * h * 4
    iteraciones = 0

    while abierta:
        iteraciones += 1
        if iteraciones > MAX_ITER:
            raise RuntimeError("A* excedió iteraciones")

        actual = heapq.heappop(abierta)

        if actual in cerrada:
            continue

        # comparación por posición
        if actual.x == destino.x and actual.y == destino.y:
            return reconstruir_camino(camino, actual)

        cerrada.add(actual)

        vecinos = mirar_vecinos(actual, mapa, others)
        for vecino in vecinos:
            if vecino in cerrada:
                continue

            punt_g_tentativa = actual.g + costo_terreno(vecino)

            # IMPORTANTE: g inicial debe ser alto
            if punt_g_tentativa < vecino.g:
                camino[vecino] = actual
                vecino.g = punt_g_tentativa
                vecino.f = vecino.g + heuristica_estimada(vecino, destino, heuristica)

                heapq.heappush(abierta, vecino)

    return None


def costo_terreno(_):
    # placeholder, acá iria el costo del terreno
    return 1


def heuristica_estimada(node, goal, method):
    if method == 'manhattan':
        return abs(node.x - goal.x) + abs(node.y - goal.y)
    elif method == 'euclidean':
        return int(sqrt((node.x - goal.x) ** 2 + (node.y - goal.y) ** 2))


def mirar_vecinos(nodo, mascara, others):
    cuadros = []
    test = mask.Mask((32, 32), fill=True)
    direcciones = ((0, -1), (1, 0), (0, 1), (-1, 0))
    mascara_actual = mascara.copy()
    for other in others:
        mascara_actual.draw(other.mask, other.rect.topleft)

    for dx, dy in direcciones:
        x = nodo.x + dx * 32
        y = nodo.y + dy * 32

        if x < 0 or y < 0:
            continue
        if x > 800 or y > 800:  # acá había otro cuello de botella.
            continue  # la multiplicación estaba dando resultados por encima de mil, cuando lo máximo debería ser 800.
            # aunque esto hace más todavía que los mobs nunca puedan salir del chunk.

        vecino = get_nodo(x, y, 32)  # CLAVE

        if not mascara_actual.overlap(test, (x, y)):
            cuadros.append(vecino)

    return cuadros


def reconstruir_camino(camino, nodo_actual):
    path = [nodo_actual]
    while nodo_actual in camino:
        nodo_actual = camino[nodo_actual]
        path.append(nodo_actual)
    path.reverse()
    return path


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
        self.g = float('inf')
        self.f = float('inf')

    def __repr__(self):
        return '(' + str(self.x) + ',' + str(self.y) + ') f: ' + str(self.f)

    def __eq__(self, other):
        return isinstance(other, Nodo) and self.x == other.x and self.y == other.y

    def __lt__(self, other):
        if self.f == other.f:
            return (self.f - self.g) < (other.f - other.g)
        return self.f < other.f

    def __hash__(self):
        return hash((self.x, self.y, self.s))

    def distancia_a(self, other):
        return heuristica_estimada(self, other, 'euclidean')

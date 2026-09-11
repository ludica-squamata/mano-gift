# A* module
from math import sqrt
from pygame import mask
from itertools import cycle
import heapq

# CACHE GLOBAL DE NODOS
nodos_cache = {}


def get_nodo(x, y, adress):
    key = (x, y, tuple(adress))
    if key not in nodos_cache:
        nodos_cache[key] = Nodo(x, y, adress)
    return nodos_cache[key]


def a_star(inicio, destino, mapa, others, heuristica='euclidean'):
    cerrada = set()
    abierta = []
    camino = {}

    inicio.g = 0
    inicio.f = heuristica_estimada(inicio, destino, heuristica)

    heapq.heappush(abierta, inicio)

    while abierta:

        actual = heapq.heappop(abierta)

        if actual in cerrada:
            continue

        # comparación por posición
        if actual == destino:
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


def heuristica_estimada(node, goal, method:str):
    if method == 'manhattan':
        return abs(node.x - goal.x) + abs(node.y - goal.y)
    elif method == 'euclidean':
        if tuple(node.adress) != tuple(goal.adress):
            global_x1 = node.adress[0] * 800 + node.x
            global_y1 = node.adress[1] * 800 + node.y

            global_x2 = goal.adress[0] * 800 + goal.x
            global_y2 = goal.adress[1] * 800 + goal.y

            return int(sqrt((global_x1 - global_x2) ** 2 + (global_y1 - global_y2) ** 2))
        else:
            return int(sqrt((node.x - goal.x) ** 2 + (node.y - goal.y) ** 2))


def mirar_vecinos(nodo, mapa, others):
    cuadros = []
    obstaculos = []
    test = mask.Mask((32, 32), fill=True)
    direcciones = ((0, -1), (0, 1), (-1, 0), (1, 0))
    for other in others:
        obs = Nodo(other.rel_cx // 32 * 32, other.rel_cy // 32 * 32, tuple(other.parent.adress))
        obstaculos.append(obs)

    for dx, dy in direcciones:
        x = nodo.x + dx * nodo.size
        y = nodo.y + dy * nodo.size

        if x < 0 or y < 0:
            adress = (nodo.adress[0]+dx, nodo.adress[1]+dy)
            chunk = mapa.get_chunk_by_adress(adress)
            if chunk is None:
                # This means that the chunk was not yet generated. There is no point that mobs,
                # other than the one controlled by the player, load maps when the player isn't seeing them.
                mascara_actual = mask.Mask((800, 800), fill=False)
                # Provisionally, a chunk-sized, blank mask is generated, for the purpose of collision detection.
                # Though this might be untrue. The mob should recheck his route once the map is fully generated.
            else:
                adress = chunk.adress
                mascara_actual = chunk.mask
            x += 800 * abs(dx)
            y += 800 * abs(dy)

        elif x >= 800 or y >= 800:
            adress = (nodo.adress[0] + dx, nodo.adress[1] + dy)
            chunk = mapa.get_chunk_by_adress(adress)
            if chunk is None:
                mascara_actual = mask.Mask((800, 800), fill=False)
            else:
                adress = chunk.adress
                mascara_actual = chunk.mask
            x -= 800 * abs(dx)
            y -= 800 * abs(dy)

        else:
            mascara_actual = mapa.get_chunk_by_adress(nodo.adress).mask
            adress = nodo.adress

        vecino = get_nodo(x, y, adress)  # CLAVE
        vecino.reset_node()  # only resets g and f values

        if vecino.transitable and vecino not in obstaculos and not mascara_actual.overlap(test, (x, y)):
            cuadros.append(vecino)

    return cuadros


def reconstruir_camino(camino, nodo_actual):
    path = [nodo_actual]
    while nodo_actual in camino:
        nodo_actual = camino[nodo_actual]
        path.append(nodo_actual)
    path.reverse()
    return path


def determinar_direccion(actual, curr_p, next_p):
    px, py = curr_p
    nx, ny = next_p

    dx = nx - px
    dy = ny - py

    direccion = actual
    if dx < 0:
        direccion = "izquierda"
    elif dx > 0:
        direccion = "derecha"
    if dy < 0:
        direccion = "arriba"
    elif dy > 0:
        direccion = "abajo"

    return direccion


class Nodo:
    x = 0
    y = 0
    f = 0
    g = 0
    transitable = True

    def __init__(self, x, y, adress):
        self.size = 32
        self.x = x
        self.y = y
        self.adress = adress
        self.g = float('inf')
        self.f = float('inf')

    def __repr__(self):
        return '(' + str(self.x) + ',' + str(self.y) + ') f: ' + str(self.f)

    def __eq__(self, other):
        o = other
        return isinstance(o, Nodo) and self.x == o.x and self.y == o.y and o.adress == tuple(self.adress)

    def compare(self, x, y):
        return self.x == x and self.y == y

    def __lt__(self, other):
        if self.f == other.f:
            return (self.f - self.g) < (other.f - other.g)
        return self.f < other.f

    def __str__(self):
        return '(' + str(self.x) + ',' + str(self.y) + ')'

    def __getitem__(self, item: int):
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        else:
            raise IndexError

    def __hash__(self):
        return hash((self.x, self.y, tuple(self.adress)))

    def reset_node(self):
        self.g = float('inf')
        self.f = float('inf')

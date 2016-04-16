# movimiento.py
# scripts de movimiento para los mobs.
from .a_star import a_star
from engine.globs import CUADRO


def ai_patrol(mob):
    curr_p = [mob.mapX, mob.mapY]
    if curr_p == mob.camino[mob.next_p]:
        mob.next_p += 1
        if mob.next_p >= len(mob.camino):
            mob.next_p = 0
            if mob.reversa:
                mob.camino.reverse()
    punto_proximo = mob.camino[mob.next_p]

    direccion = determinar_direccion(curr_p, punto_proximo)
    return direccion


def ai_pursue(mob):
    objetivo = mob.objetivo
    curr_p = [mob.mapX, mob.mapY]
    punto_proximo = [objetivo.mapX, objetivo.mapY]
    direccion = determinar_direccion(curr_p, punto_proximo)
    return direccion


def ai_flee(mob):
    from math import sqrt
    cx, cy = [mob.mapX, mob.mapY]
    rutas_escape = [[0, 0], [480, 0], [0, 480], [480, 480]]
    dists = []
    dirs = []
    for dx, dy in rutas_escape:
        dirs.append(determinar_direccion([cx, cy], [dx, dy]))
        dists.append(sqrt((dx - cx) ** 2 + (dy - cy) ** 2))

    direccion = dirs[dists.index(min(dists))]
    return direccion


def iniciar_persecucion(mob, objetivo):
    curr_pos = int(mob.mapX / 32), int(mob.mapY / 32)
    obj_pos = int(objetivo.mapX / 32), int(objetivo.mapY / 32)
    ruta = generar_camino(curr_pos, obj_pos, mob.stage.grilla)
    camino = None
    if type(ruta) == list:
        camino = simplificar_camino(ruta)
    elif ruta is None:
        iniciar_persecucion(mob, objetivo)
    else:
        camino = [[ruta.x, ruta.y]]
    return camino


def generar_camino(inicio, destino, grilla):
    """Genera un camino de puntos de grilla.
    inicio y destino deben ser un tuple Gx,Gy"""
    ruta = a_star(grilla[inicio], grilla[destino], grilla)
    if type(ruta) == str:
        camino = [[int(i) * CUADRO for i in punto.strip('()').split(',')] for punto in ruta.split(';')]
        return camino
    return ruta


def simplificar_camino(camino):
    x, y = camino[0]
    fin = camino[-1]
    simple = []
    nx, ny = 0, 0
    for i in range(len(camino[1:])):
        dx, dy = camino[i]
        if i + 1 <= len(camino):
            nx, ny = camino[i + 1]

        if nx != x and ny != y:
            simple.append([dx, dy])
            x = dx
            y = dy
    simple.append(fin)
    return simple


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

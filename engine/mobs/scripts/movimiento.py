# movimiento.py
# scripts de movimiento para los mobs.
from .a_star import Astar
from engine.globs import Constants as C


def AI_patrol(mob):
    curr_p = [mob.mapX, mob.mapY]
    if curr_p == mob.camino[mob.next_p]:
        mob.next_p += 1
        if mob.next_p >= len(mob.camino):
            mob.next_p = 0
            if mob.reversa:
                mob.camino.reverse()
    punto_proximo = mob.camino[mob.next_p]

    direccion = _determinar_direccion(curr_p, punto_proximo)
    return direccion


def AI_pursue(mob):
    objetivo = mob.objetivo
    curr_p = [mob.mapX, mob.mapY]
    punto_proximo = [objetivo.mapX, objetivo.mapY]
    direccion = _determinar_direccion(curr_p, punto_proximo)
    return direccion


def AI_flee(mob):
    from math import sqrt
    cX, cY = [mob.mapX, mob.mapY]
    rutas_escape = [[0, 0], [480, 0], [0, 480], [480, 480]]
    dists = []
    dirs = []
    for dx, dy in rutas_escape:
        dirs.append(_determinar_direccion([cX, cY], [dx, dy]))
        dists.append(sqrt((dx - cX) ** 2 + (dy - cY) ** 2))

    direccion = dirs[dists.index(min(dists))]
    return direccion


def iniciar_persecucion(mob, objetivo):
    CURR_POS = int(mob.mapX / 32), int(mob.mapY / 32)
    OBJ_POS = int(objetivo.mapX / 32), int(objetivo.mapY / 32)
    ruta = generar_camino(CURR_POS, OBJ_POS, mob.stage.grilla)
    if type(ruta) == list:
        camino = simplificar_camino(ruta)
    elif ruta == None:
        iniciar_persecucion(mob, objetivo)
    else:
        camino = [[ruta.x, ruta.y]]
    return camino


def generar_camino(inicio, destino, grilla):
    '''Genera un camino de puntos de grilla.
    inicio y destino deben ser un tuple Gx,Gy'''
    ruta = Astar(grilla[inicio], grilla[destino], grilla)
    if type(ruta) == str:
        camino = [[int(i) * C.CUADRO for i in punto.strip('()').split(',')] for punto in ruta.split(';')]
        return camino
    return ruta


def simplificar_camino(camino):
    x, y = camino[0]
    fin = camino[-1]
    simple = []
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


def _determinar_direccion(curr_p, next_p):
    pX, pY = curr_p
    nX, nY = next_p

    dx = pX - nX
    dy = pY - nY

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

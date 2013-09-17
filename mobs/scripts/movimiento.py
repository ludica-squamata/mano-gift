# movimiento.py
# scripts de movimiento para los mobs.
from random import randint, choice
from .a_star import Astar
from globs import Constants as C

def AI_wander(mob):
    mob.ticks += 1
    mob.mov_ticks += 1
    direccion = mob.direccion
    if mob.mov_ticks == 3:
        mob.mov_ticks = 0
        pos = 10
        if randint(1,101) <= pos:
            lista = list(mob.direcciones.keys())
            lista.remove(mob.direccion)
            direccion = choice(lista)
    return direccion

def AI_patrol(mob):
    curr_p = [mob.mapX,mob.mapY]
    if curr_p == mob.patrol_p[mob.next_p]:
        mob.next_p += 1
        if mob.next_p >= len(mob.patrol_p):
            mob.next_p = 0
    punto_proximo = mob.patrol_p[mob.next_p]
    
    direccion = _determinar_direccion(curr_p,punto_proximo)
    return direccion

def AI_caminar_por_ruta(mob):
    curr_p = [mob.mapX,mob.mapY]
    if curr_p == mob.camino[mob.next_p]:
        mob.next_p += 1
        if mob.next_p >= len(mob.camino):
            mob.next_p = 0
            mob.camino.reverse()
    punto_proximo = mob.camino[mob.next_p]
    
    direccion = _determinar_direccion(curr_p,punto_proximo)
    return direccion

def generar_camino (mob):
    grilla = mob.stage.grilla
    mob_ini = mob.punto_inicio
    mob_fin = mob.punto_destino
    for i in range(len(grilla)):
        punto = [grilla[i].x*C.CUADRO,grilla[i].y*C.CUADRO]
        if punto == mob_ini:
           inicial = i
        elif punto == mob_fin:
           destino = i
    
    ruta = Astar(grilla[inicial],grilla[destino],grilla)
    camino = [[int(i)*C.CUADRO for i in punto.strip('()').split(',')] for punto in ruta.split(';')]
    return camino

def _determinar_direccion(curr_p,next_p):
    pX,pY = curr_p
    nX,nY = next_p
    
    dx = pX-nX
    dy = pY-nY
    
    if dx > dy:
        if dy < 0: direccion = 'abajo'
        else: direccion = 'derecha'
    else:
        if dx < 0: direccion = 'izquierda'
        else: direccion = 'arriba'
    
    return direccion
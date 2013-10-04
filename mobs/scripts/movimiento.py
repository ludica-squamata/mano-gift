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
        if randint(1,101) <= 10: # 10% de probabilidad
            lista = list(mob.direcciones.keys())
            lista.remove(mob.direccion)
            direccion = choice(lista)
    return direccion

def AI_patrol(mob):
    curr_p = [mob.mapX,mob.mapY]
    if curr_p == mob.camino[mob.next_p]:
        mob.next_p += 1
        if mob.next_p >= len(mob.camino):
            mob.next_p = 0
            if mob.reversa:
                mob.camino.reverse()
    punto_proximo = mob.camino[mob.next_p]
    
    direccion = _determinar_direccion(curr_p,punto_proximo)
    return direccion

def AI_pursue(mob):
    curr_p = [mob.mapX,mob.mapY]
    if curr_p == mob.camino[mob.next_p]:
        mob.next_p += 1
        if mob.next_p >= len(mob.camino):
            mob.next_p = 0
    punto_proximo = mob.camino[mob.next_p]
    direccion = _determinar_direccion(curr_p,punto_proximo)
    return direccion
    

def generar_camino (inicio,destino,grilla):
    inicio = list(inicio)
    destino = list(destino)
    inicial,final = '',''
    for i in range(len(grilla)):
        punto = [grilla[i].x*C.CUADRO,grilla[i].y*C.CUADRO]
        if punto == inicio:
           inicial = i
        elif punto == destino:
           final = i
        
        if inicial != '' and final != '':
            break
            
    ruta = Astar(grilla[inicial],grilla[final],grilla)
    camino = [[int(i)*C.CUADRO for i in punto.strip('()').split(',')] for punto in ruta.split(';')]
    return camino

def simplificar_camino(camino):
    x,y = camino[0]
    fin = camino[-1]
    simple = []
    for i in range(len(camino[1:])):
        dx,dy = camino[i]
        if i+1 <= len(camino):
            nx,ny = camino[i+1]
            
        if nx != x and ny != y:
            simple.append([dx,dy])
            x = dx
            y = dy
    simple.append(fin)
    return simple

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


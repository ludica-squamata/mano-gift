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

def iniciar_persecucion(mob,objetivo):
    CURR_POS = int(mob.mapX/32),int(mob.mapY/32)
    OBJ_POS = int(objetivo.mapX/32),int(objetivo.mapY/32)
    ruta = generar_camino(CURR_POS,OBJ_POS,mob.stage.grilla)
    if type(ruta) == list:
        camino = simplificar_camino(ruta)
    elif type(ruta) == None:
        iniciar_persecucion(mob,objetivo)
    else:
        camino = [[ruta.x,ruta.y]]
    return camino

def generar_camino (inicio,destino,grilla):
    '''Genera un camino de puntos de grilla.
    inicio y destino deben ser un tuple Gx,Gy'''        
    ruta = Astar(grilla[inicio],grilla[destino],grilla)
    if type(ruta) == str:
        camino = [[int(i)*C.CUADRO for i in punto.strip('()').split(',')] for punto in ruta.split(';')]
        return camino
    return ruta
    
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


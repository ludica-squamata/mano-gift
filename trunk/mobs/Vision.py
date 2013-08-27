from pygame import mask
from misc import Resources as r

class area_vision:
    _masks = {} # máscaras de visión ordenadas por direcciones.
    mask = None # máscara de visión actual
    _direccion = None 
    
    def __init__ (self,direccion):
        direcciones = ['abajo','arriba','derecha','izquierda']
        visiones = r.split_spritesheet('mobs/visiones.png',w=96,h=96)
        vis_pos = [
            {'x':-32, 'y':   0},
            {'x':-32, 'y': -64},
            {'x':-64, 'y': -32},
            {'x':  0, 'y': -32}]
        
        for i  in range(len(direcciones)):
            self._masks[direcciones[i]] = {'mask':mask.from_surface(visiones[i]),
                                           'dpos':vis_pos[i]}
        
        self.cambiar_direccion(direccion)
    
    def x (self,mob):
        return mob.mapX + self._masks[self._direccion]['dpos']['x']
    
    def y (self,mob):
        return mob.mapY + self._masks[self._direccion]['dpos']['y']
    
    def cambiar_direccion(self,direccion):
        #reorienta la mascara.
        if direccion != 'ninguna':
            self._direccion = direccion
            self.mask = self._masks[self._direccion]['mask']
    

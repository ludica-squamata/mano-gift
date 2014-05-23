from math import tan, radians
from pygame import Color, Surface, draw, mask, transform
from globs import MobGroup

class Sensitivo:
    vision = None # triangulo de la visión. posición por default = arriba
    vx,vy = 0,0 # posicion de la visión, puesta acá por si el mob no se mueve
    
    @staticmethod
    def generar_tri_vision(largo):
        '''Crea el triangulo de la visión (fg azul, bg transparente).
        
        Devuelve un surface.'''
        
        def _ancho(largo):
            an = radians(40)
            return round(largo*round(tan(an),2))
        ancho = _ancho(largo)

        negro = Color(0,0,0)
        azul = Color(0,0,255)
        
        megasurf = Surface((ancho*2,largo))
        draw.polygon(megasurf,azul,[[0,0],[ancho,largo],[ancho*2,0]]) 
        megasurf.set_colorkey(negro)
    
        return megasurf
    
    @staticmethod
    def generar_cir_vision(radio):
        '''crea un circulo de vision, que se usa cuando el mob
        detecta algo, pues escapar del triangulo es muy sencillo'''
        
        negro = Color(0,0,0)
        azul = Color(0,0,255)
        surf = Surface((radio*2,radio*2))
        draw.circle(surf,azul,[radio,radio],radio,0)
        surf.set_colorkey(negro)
        return surf
    
    def mover_tri_vis (self,direccion):
        '''Gira el triangulo de la visión.
        
        Devuelve el surface del triangulo rotado, y la posicion en x e y'''
        tx,ty,tw,th = self.mapX,self.mapY,self.rect.w,self.rect.h
        img = self.vision
        if direccion == 'abajo':
            surf = transform.flip(img,False,True)
            w,h = surf.get_size()
            y = ty+th
            x = tx+(tw/2)-w/2
        elif direccion == 'izquierda':
            surf = transform.rotate(img,-90.0)
            w,h = surf.get_size()
            x = tx+tw
            y = ty+(th/2)-h/2
        elif direccion == 'derecha':
            surf = transform.rotate(img,+90.0)
            w,h = surf.get_size()
            x = tx-w
            y = ty+(th/2)-h/2
        else:
            surf = img
            w,h = surf.get_size()
            y = ty-h
            x = tx+(tw/2)-w/2
        return surf,int(x),int(y)
    
    def mover_cir_vis(self,dummy = None):
        '''Si la visión es circular, entonces se usa esta función
        para moverla. El argumento dummy viene a ser la direccion,
        pero como no hay que girar el circulo, es indistinta.'''
        
        tx,ty,tw,th = self.mapX,self.mapY,self.rect.w,self.rect.h
        w,h = self.cir_vis.get_size()
        x = int(tx+(tw/2)-(w/2))
        y = int(ty+(th/2)-(h/2))
        return self.cir_vis,x,y

    def ver (self):
        '''Realiza detecciones con la visión del mob'''
        detected = []
        if self.direccion != 'ninguna':
            vision,self.vx,self.vy = self.mover_vis(self.direccion)
            for key in MobGroup:
                mob =  MobGroup[key]
                if mob != self:
                    vis_mask = mask.from_surface(vision)
                    x,y = self.vx-mob.mapX, self.vy-mob.mapY
                    if mob.mask.overlap(vis_mask,(x,y)):
                        detected.append(mob)
        
        return detected
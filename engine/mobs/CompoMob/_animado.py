from engine.globs import Tiempo as T, Constants as C
from engine.misc import Util as U, Resources as r
from pygame import mask

class Animado:
    __key_anim = '' #para uso interno de animar_caminar
    ticks, mov_ticks = 0,0
    atacando = False
    images = {} # incluye todas las imagenes del mob, arriba abajo izquierda y derecha
    death_img = None # sprite del mob muerto.
    dead = False
        
    def cargar_anims(self,ruta_imgs,seq,alpha=False):
        dicc = {}
        spritesheet = r.split_spritesheet(ruta_imgs)
        dires = ['abajo','arriba','derecha','izquierda']
        keys = []
        
        for L in seq:
            for D in dires:
                keys.append(L+D)
        
        for key in keys:
            if not alpha:
                dicc[key] = spritesheet[keys.index(key)]
            else:
                _alpha = mask.from_threshold(spritesheet[keys.index(key)], C.COLOR_COLISION, (1,1,1,255))
                dicc[key] = _alpha
        return dicc
    
    def animar_caminar(self):
        '''cambia la orientación del sprite y controla parte de la animación'''
        
        key = self.__key_anim
        self.t_image = None
        
        self.timer_animacion += T.FPS.get_time()
        if self.timer_animacion >= self.frame_animacion:
            self.timer_animacion = 0
            if self.direccion != 'ninguna':
                if key == 'D'+self.direccion:
                    key = 'I'+self.direccion
                elif key == 'I'+self.direccion:
                    key = 'D'+self.direccion
                else:
                    key = 'D'+self.direccion
                self.t_image = self.images[key]
                self.calcular_sombra()
                self.__key_anim = key
    
    def calcular_sombra(self):
        image = U.crear_sombra(self.t_image)
        image.blit(self.t_image,[0,0])
        self.image = image
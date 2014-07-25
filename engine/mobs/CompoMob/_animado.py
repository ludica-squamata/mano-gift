from engine.globs import Tiempo as T, Constants as C
from engine.misc import Util as U, Resources as r
from engine.base import _giftSprite
from ._movil import Movil
from pygame import mask

class Animado(Movil, _giftSprite):  # necesita Movil para tener direccion, giftSprite para las imagenes
    ticks, mov_ticks = 0, 0
    atacando = False
    death_img = None  # sprite del mob muerto.
    dead = False
    _step = 'S'

    def __init__(self, *args, **kwargs):
        #self.anim_counter = 0 estas variables ya no se usan
        #self.anim_limit = 20 a no ser que sean parte de shadowSprite
        self.timer_animacion = 0
        self.frame_animacion = 1000/12
        super().__init__(*args, **kwargs)

    @staticmethod
    def cargar_anims(ruta_imgs,seq,alpha=False):
        dicc = {}
        spritesheet = r.split_spritesheet(ruta_imgs)
        idx = -1
        for L in seq:
            for D in ['abajo','arriba','izquierda','derecha']:
                key = L+D
                idx += 1
                if not alpha:
                    dicc[key] = spritesheet[idx]
                else:
                    dicc[key] = mask.from_threshold(spritesheet[idx], C.COLOR_COLISION, (1,1,1,255))
        return dicc
    
    def animar_caminar(self):
        """cambia la orientación del sprite y controla parte de la animación"""

        self.timer_animacion += T.FPS.get_time()
        if self.timer_animacion >= self.frame_animacion:
            self.timer_animacion = 0
            if self.direccion != 'ninguna':
                if self._step == 'D':
                    self._step = 'I'
                else:
                    self._step = 'D'

                key = self._step+self.direccion

                self.image = self.imagenN(key)
                self.mask = self.mascaraN(key)
    
    def animar_ataque (self,limite):
        # construir la animación
        frames,alphas = [],[]
        for L in ['A','B','C']:
            frames.append(self.cmb_atk_img[L+self.direccion])
            alphas.append(self.cmb_atk_alpha[L+self.direccion])
            
        # iniciar la animación
        self.atk_counter += 1
        if self.atk_counter > limite:
            self.atk_counter = 0
            self.atk_img_index += 1
            if self.atk_img_index > len(frames)-1:
                self.atk_img_index = 0
                self.atacando = False
            
            self.image = frames[self.atk_img_index]
            #self.mask = self.cmb_walk_alpha['S'+self.direccion]
            self.mask = alphas[self.atk_img_index]
            #self.calcular_sombra(frames[self.atk_img_index])
    
    def calcular_sombra(self,current_image):
        ImagenConSombra = U.crear_sombra(current_image)
        ImagenConSombra.blit(current_image,[0,0])
        self.image = ImagenConSombra
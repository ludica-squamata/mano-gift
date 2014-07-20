from engine.globs import Tiempo as T, Constants as C
from engine.misc import Util as U, Resources as r
from pygame import mask
from ._movil import Movil
from engine.base import _giftSprite


class Animado(Movil, _giftSprite):  # necesita Movil para tener direccion, giftSprite para las imagenes
    ticks, mov_ticks = 0, 0
    atacando = False
    death_img = None  # sprite del mob muerto.
    dead = False
    _step = 'S'

    def __init__(self, *args, **kwargs):
        self.anim_counter = 0
        self.anim_limit = 20
        self.timer_animacion = 0
        self.frame_animacion = 1000/12
        super().__init__(*args, **kwargs)

    @staticmethod
    def cargar_anims(ruta_imgs,seq,alpha=False):
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
    
    def calcular_sombra(self,current_image):
        ImagenConSombra = U.crear_sombra(current_image)
        ImagenConSombra.blit(current_image,[0,0])
        self.image = ImagenConSombra
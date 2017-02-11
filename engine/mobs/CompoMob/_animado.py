from engine.globs import Tiempo, COLOR_COLISION
from engine.misc import Resources
from ._movil import Movil
from pygame import mask


class Animado(Movil):  # necesita Movil para tener direccion, giftSprite para las imagenes
    ticks, mov_ticks = 0, 0
    atacando = False
    death_img = None  # sprite del mob muerto.
    dead = False

    _step = 'S'
    estado = ''  # idle, o cmb. Indica si puede atacar desde esta posición, o no.

    cmb_atk_img = {}  # combat position images.
    cmb_atk_alpha = {}  # combat position images's alpha.
    cmb_walk_img = {}  # combat walking images.
    cmb_walk_alpha = {}  # combat walking images's alpha.

    atk_counter = 0
    atk_img_index = -1

    timer_animacion = 0
    frame_animacion = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timer_animacion = 0
        self.frame_animacion = 1000 / 12

    @staticmethod
    def cargar_anims(ruta_imgs, seq, alpha=False):
        dicc = {}
        spritesheet = Resources.split_spritesheet(ruta_imgs)
        idx = -1
        for L in seq:
            for D in ['abajo', 'arriba', 'izquierda', 'derecha']:
                key = L + D
                idx += 1
                if not alpha:
                    dicc[key] = spritesheet[idx]
                else:
                    dicc[key] = mask.from_threshold(spritesheet[idx], COLOR_COLISION, (1, 1, 1, 255))
        return dicc

    def animar_caminar(self):
        """cambia la orientación del sprite y controla parte de la animación"""

        self.timer_animacion += Tiempo.FPS.get_time()
        if self.timer_animacion >= self.frame_animacion:
            self.timer_animacion = 0
            if self.direccion != 'ninguna':
                if self._step == 'R':
                    self._step = 'L'
                else:
                    self._step = 'R'

        key = self._step + self.direccion
        self.image = self.imagen_n(key)

    def animar_ataque(self, limite):
        # construir la animación
        frames, alphas = [], []
        for L in ['A', 'B', 'C']:
            frames.append(self.cmb_atk_img[L + self.direccion])
            alphas.append(self.cmb_atk_alpha[L + self.direccion])

        # iniciar la animación
        self.atk_counter += 1
        if self.atk_counter > limite:
            self.atk_counter = 0
            self.atk_img_index += 1
            if self.atk_img_index < len(frames):
                self.image = frames[self.atk_img_index]
                self.mask = alphas[self.atk_img_index]
            else:
                self.atk_img_index = 0
                self.atacando = False
                self.images = self.cmb_walk_img
                self.mascaras = self.cmb_walk_alpha
                self.image = self.images['S' + self.direccion]
                self.mask = self.mascaras['S' + self.direccion]

    def mover(self):
        self.animar_caminar()
        super().mover()

    def accion(self):
        if self.estado == 'cmb':
            self.atacando = True

    def update(self):
        if self.atacando:
            self.animar_ataque(5)

    def detener_movimiento(self):
        super().detener_movimiento()
        key = 'S' + self.direccion
        self.image = self.imagen_n(key)

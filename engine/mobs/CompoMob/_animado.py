from engine.misc.resources import split_spritesheet, combine_mob_spritesheets
from engine.globs import Tiempo, COLOR_COLISION, ModData
from ._movil import Movil
from pygame import mask


class Animado(Movil):  # necesita Movil para tener dirección
    atacando = False
    death_img = None  # sprite del mob muerto.
    dead = False

    step = 'S'
    estado = ''  # idle, o cmb. Indica si puede atacar desde esta posición, o no.

    idle_walk_img = None  # imagenes normales, head front
    cmb_atk_img = None  # combat position images, head front
    cmb_walk_img = None  # combat walking images, head front

    # Nuevos sets de imágenes para los movimientos de la cabeza.
    idle_left_img = None  # idle, head left
    idle_right_img = None  # idle, head right
    idle_back_img = None

    atk_left_img = None  # attacking, head left
    atk_right_img = None  # attacking, head right
    atk_back_img = None

    cmb_left_img = None  # combat, head left
    cmb_right_img = None  # combat, head right
    cmb_back_img = None

    head_direction = 'front'  # front, left, right
    body_direction = 'abajo'  # abajo, arriba, izquierda, derecha

    heads = None  # contraparte de "images"

    atk_counter = 0
    atk_img_index = -1

    timer_animacion = 0
    frame_animacion = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.timer_animacion = 0
        self.frame_animacion = 1000 / 6

    @staticmethod
    def cargar_alpha(ruta_imgs: str, seq: list):
        dicc = {}
        spritesheet = split_spritesheet(ModData.graphs + ruta_imgs)
        idx = -1
        for L in seq:
            for D in ['abajo', 'arriba', 'izquierda', 'derecha']:
                key = L + D
                idx += 1
                dicc[key] = mask.from_threshold(spritesheet[idx], COLOR_COLISION, (1, 1, 1, 255))
        return dicc

    @staticmethod
    def cargar_anims2(frames: list, seq: list):
        dicc = {}
        idx = -1
        for L in seq:
            for D in ['abajo', 'arriba', 'izquierda', 'derecha']:
                key = L + D
                idx += 1
                dicc[key] = frames[idx]

        return dicc

    def cargar_head_anims(self, ruta_heads, ruta_body, seq, request='front'):
        dicc = {}
        sprites = combine_mob_spritesheets(ModData.graphs + ruta_heads, ModData.graphs + ruta_body)
        dicc['front'] = sprites[0:12]  # las 12 imagenes que venimos usando hasta ahora. mirando al frente
        dicc['left'] = sprites[12:24]  # nuevas imagenes con el mob mirando a izquierda
        dicc['right'] = sprites[24:36]  # y a derecha.
        return self.cargar_anims2(dicc[request], seq)

    def animar_caminar(self):
        """cambia la orientación del sprite y controla parte de la animación"""

        self.timer_animacion += Tiempo.FPS.get_time()
        if self.timer_animacion >= self.frame_animacion:
            self.timer_animacion = 0
            if self.direccion != 'ninguna':
                if self.step == 'R':
                    self.step = 'L'
                else:
                    self.step = 'R'

        key = self.step + self.direccion
        self.image = self.imagen_n(key)

    def animar_ataque(self, limite):
        # construir la animación
        frames, alphas = [], []
        for L in ['A', 'B', 'C']:
            frames.append(self.cmb_atk_img[L + self.direccion])

        # iniciar la animación
        self.atk_counter += 1
        if self.atk_counter > limite:
            self.atk_counter = 0
            self.atk_img_index += 1
            if self.atk_img_index < len(frames):
                self.image = frames[self.atk_img_index]

            else:
                self.atk_img_index = 0
                self.atacando = False
                self.images = self.cmb_walk_img
                self.image = self.images['S' + self.direccion]

    def accion(self):
        if self.estado == 'cmb':
            self.atacando = True

    def cambiar_estado(self):
        if self.estado == 'idle':
            self.estado = 'cmb'
            self.images = self.cmb_walk_img
            self.heads = {'front': self.cmb_walk_img,
                          'left': self.cmb_left_img,
                          'right': self.cmb_right_img}

        elif self.estado == 'cmb':
            self.estado = 'idle'
            self.images = self.idle_walk_img
            self.heads = {'front': self.idle_walk_img,
                          'right': self.idle_left_img,
                          'left': self.idle_right_img}

        self.animar_caminar()

    def rotar_cabeza(self, orientacion='front'):
        head_direction = None
        # estos dos bloques sólo funcionan bien cuando el cuerpo mira hacia abajo
        # quizás habría que discriminar primero por la dirección del cuerpo.
        if self.head_direction == 'left':
            if orientacion != 'left':
                head_direction = 'front'

        elif self.head_direction == 'right':
            if orientacion != 'right':
                head_direction = 'front'

        elif orientacion == 'back':
            # este bloque funciona bien, porque la cabeza no puede mirar hacia atrás si el cuerpo mira adelante
            head_direction = 'front'
            self.body_direction = 'arriba'

        elif self.head_direction == 'front' and self.body_direction == 'arriba':
            # este bloque es para cuando el cuerpo mira hacia arriba. Derecha e izquierda deberían estar invertidos.
            # tal vez habría que hacer lo mismo para cuando el cuerpo mira a derecha y a izquierda.
            if orientacion == 'left':
                head_direction = 'right'

            elif orientacion == 'right':
                head_direction = 'left'

            elif orientacion == 'front':
                head_direction = 'front'

        if head_direction is None:
            head_direction = orientacion
        self.head_direction = head_direction
        self.images = self.heads[self.head_direction]  # front, left or right

    def translate(self, orientacion):
        # esta funcion debería mover sólo el cuerpo.
        if self.direccion == 'abajo':
            if orientacion != 'back':
                return 'abajo'
            else:
                return 'arriba'

        elif self.direccion == 'arriba':
            if orientacion == 'left':
                return 'arriba'
            elif orientacion == 'right':
                return 'arriba'
            elif orientacion == 'back':
                pass
            elif orientacion == 'front':
                pass

        elif self.direccion == 'izquierda':
            if orientacion == 'left':
                pass
            elif orientacion == 'right':
                pass
            elif orientacion == 'back':
                pass
            elif orientacion == 'front':
                pass

        elif self.direccion == 'derecha':
            if orientacion == 'left':
                pass
            elif orientacion == 'right':
                pass
            elif orientacion == 'back':
                pass
            elif orientacion == 'front':
                pass

    def cambiar_direccion(self, direccion=None):
        super().cambiar_direccion(direccion)
        if not self.moviendose:
            self.image = self.images['S' + self.direccion]
            self.step = 'S'

    def cambiar_direccion2(self, orientacion):
        direccion = self.translate(orientacion)
        self.rotar_cabeza(orientacion)
        self.cambiar_direccion(direccion)

    def update(self, *args):
        super().update(*args)
        if self.atacando:
            self.animar_ataque(5)
        if self.moviendose:
            self.animar_caminar()

    def detener_movimiento(self):
        super().detener_movimiento()
        self.step = 'S'
        key = 'S' + self.direccion
        self.image = self.imagen_n(key)

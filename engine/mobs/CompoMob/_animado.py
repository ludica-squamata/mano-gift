from engine.globs.event_dispatcher import EventDispatcher
from engine.globs import Tiempo, COLOR_COLISION, ModData
from engine.misc.resources import split_spritesheet
from pygame import mask, Surface, SRCALPHA
from ._movil import Movil
from os.path import join
from os import listdir


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

    atk_left_img = None  # attacking, head left
    atk_right_img = None  # attacking, head right

    cmb_left_img = None  # combat, head left
    cmb_right_img = None  # combat, head right

    head_direction = 'front'  # front, left, right
    body_direction = 'abajo'  # abajo, arriba, izquierda, derecha

    heads = None  # contraparte de "images"

    atk_counter = 0
    atk_img_index = -1

    timer_animacion = 0
    frame_animacion = 0
    timer_rotacion = 0
    cuentapasos = 0

    timer_blinking = 0

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.timer_animacion = 0
        self.frame_animacion = 1000 / 6
        self.blinking_eyes = {'front': {}, 'right': {}, 'left': {}}

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
    def cargar_anims(ruta_imgs, seq, alpha=False, request='front'):
        assert request in ['left', 'right', 'front']
        # the "request" parameter exists for compatibility with cargar_head_anims()

        dicc = {}
        spritesheet = split_spritesheet(ModData.graphs + ruta_imgs)
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
                self.cuentapasos += 1
                if self.step == 'R':
                    self.step = 'L'
                else:
                    self.step = 'R'

        if self['AI'].name != 'controllable':
            EventDispatcher.trigger('SoundEvent', self,
                                    {'type': 'movement', 'intensity': 1, 'sound': 'walking_on_grass'})

        key = self.step + self.direccion
        self.image = self.imagen_n(key)

    def animate_standing_position(self):
        """Rotates the body to align it with the head at the same direction"""
        orientacion = None
        self.timer_rotacion += 1
        if self.timer_rotacion % 120 == 0 and self.head_direction != 'front':

            if self.body_direction == 'izquierda':
                if self.head_direction == 'left':
                    orientacion = 'back'
                elif self.head_direction == 'right':
                    orientacion = 'front'

            elif self.body_direction == 'derecha':
                if self.head_direction == 'left':
                    orientacion = 'front'
                elif self.head_direction == 'right':
                    orientacion = 'back'

            elif self.body_direction == 'abajo':
                if self.head_direction == 'left':
                    orientacion = 'left'
                elif self.head_direction == 'right':
                    orientacion = 'right'

            elif self.body_direction == 'arriba':
                if self.head_direction == 'left':
                    orientacion = 'right'
                elif self.head_direction == 'right':
                    orientacion = 'left'

            self.cambiar_direccion2(orientacion)

    def animate_walking_head_orientation(self):
        orientacion = None
        if self.cuentapasos % 12 == 0:
            if self.body_direction == 'abajo':
                orientacion = 'front'
            elif self.body_direction == 'arriba':
                orientacion = 'back'
            elif self.body_direction == 'izquierda':
                orientacion = 'left'
            elif self.body_direction == 'derecha':
                orientacion = 'right'

            self.cambiar_direccion2(orientacion)

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
            EventDispatcher.trigger('PlaySound', self, {'sound': 'miss'})
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
        self.timer_rotacion = 0
        if self.body_direction == 'abajo':
            if orientacion == 'back':
                self.body_direction = 'arriba'
                head_direction = 'front'

            if orientacion == 'right':
                if self.head_direction == 'right':
                    self.body_direction = 'derecha'
                    head_direction = 'front'
                elif self.head_direction == 'left':
                    head_direction = 'front'

            elif orientacion == 'left':
                if self.head_direction == 'left':
                    self.body_direction = 'izquierda'
                    head_direction = 'front'
                elif self.head_direction == 'right':
                    head_direction = 'front'

            elif orientacion == 'front':
                head_direction = 'front'

        elif self.body_direction == 'arriba':
            if orientacion == 'front':
                self.body_direction = 'abajo'
                head_direction = 'front'

            if orientacion == 'left':
                if self.head_direction != 'right':
                    head_direction = 'right'
                else:
                    self.body_direction = 'izquierda'
                    head_direction = 'front'

            elif orientacion == 'right':
                if self.head_direction != 'left':
                    head_direction = 'left'
                else:
                    self.body_direction = 'derecha'
                    head_direction = 'front'
            elif orientacion == 'back':
                head_direction = 'front'

        elif self.body_direction == 'izquierda':
            if orientacion == 'back':
                if self.head_direction != 'left':
                    head_direction = 'left'
                else:
                    self.body_direction = 'arriba'
                    head_direction = 'front'
            elif orientacion == 'front':
                if self.head_direction != 'right':
                    head_direction = 'right'
                else:
                    self.body_direction = 'abajo'
            elif orientacion == 'right':
                if self.head_direction != 'right':
                    head_direction = 'right'
                else:
                    head_direction = 'front'
                    self.body_direction = 'abajo'
            elif orientacion == 'left':
                head_direction = 'front'

        elif self.body_direction == 'derecha':
            if orientacion == 'back':
                if self.head_direction != 'right':
                    head_direction = 'right'
                else:
                    head_direction = 'front'
                    self.body_direction = 'arriba'
            elif orientacion == 'front':
                if self.head_direction != 'left':
                    head_direction = 'left'
                else:
                    self.body_direction = 'abajo'
            elif orientacion == 'left':
                if self.head_direction != 'left':
                    head_direction = 'left'
                else:
                    head_direction = 'front'
                    self.body_direction = 'abajo'
            elif orientacion == 'right':
                head_direction = 'front'

        if head_direction is None:
            head_direction = orientacion
        self.head_direction = head_direction
        self.images = self.heads[self.head_direction]  # front, left or right

    def animar_parpadeo(self, command: str):
        """command might be squint; blink, or open"""
        full_command, direccion = '',''
        if self.head_direction == 'front':
            if self.body_direction == 'abajo':
                full_command = f'front_{command}'
                direccion = 'front'
            elif self.body_direction == 'izquierda':
                full_command = f'left_{command}'
                direccion = 'left'
            elif self.body_direction == 'derecha':
                full_command = f'right_{command}'
                direccion = 'right'

        if len(direccion):
            if full_command in self.blinking_eyes[direccion]:
                image = self.blinking_eyes[direccion][full_command]
                self.image.blit(image, [0, 0])

    def cargar_parpadeo(self):
        front_names = ['front_open', 'left_squint', 'left_blink', 'right_squint', 'right_blink', 'front_blink']
        front_index = [0, 1, 2, 3, 7, 11]
        right_names = ['right_open', 'right_squint', 'right_blink']
        right_index = [4, 5, 6]
        left_names = ['left_open', 'left_squint', 'left_blink']
        left_index = [8, 9, 10]
        template = self.data['imagenes']['idle'].lstrip('/mobs/imagenes').rstrip('idle_walk_body.png')
        spritesheet = None
        for file in listdir(join(ModData.graphs, 'mobs', 'imagenes')):
            if 'blinking' in file and template in file:
                ruta = join(ModData.graphs, 'mobs', 'imagenes', file)
                spritesheet = split_spritesheet(ruta)
                break
        if spritesheet is not None:
            for i, key in enumerate(front_names):
                self.blinking_eyes['front'][key] = spritesheet[front_index[i]]

            squint = Surface([32, 32], SRCALPHA)
            squint.blit(spritesheet[1].subsurface(0, 0, 16, 32), [1, 0])
            squint.blit(spritesheet[3].subsurface(16, 0, 16, 32), [17, 0])
            self.blinking_eyes['front']['front_squint'] = squint

            for i, key in enumerate(right_names):
                self.blinking_eyes['right'][key] = spritesheet[right_index[i]]
            for i, key in enumerate(left_names):
                self.blinking_eyes['left'][key] = spritesheet[left_index[i]]

    def cambiar_direccion(self, direccion=None):
        super().cambiar_direccion(direccion)
        self.body_direction = direccion
        if not self.moviendose:
            self.image = self.images['S' + self.direccion]
            self.step = 'S'

    def cambiar_direccion2(self, orientacion):
        self.rotar_cabeza(orientacion)
        self.cambiar_direccion(self.body_direction)

    def update(self, *args):
        super().update(*args)
        if self.atacando:
            self.animar_ataque(5)
        if self.moviendose:
            self.animar_caminar()
            self.animate_walking_head_orientation()
        else:
            self.animate_standing_position()
        if self.timer_rotacion == 240:
            self.animar_parpadeo('squint')
        elif self.timer_rotacion == 320:
            self.animar_parpadeo('blink')
        elif self.timer_rotacion == 420:
            self.animar_parpadeo('open')
            self.timer_rotacion = 0

    def detener_movimiento(self):
        super().detener_movimiento()
        self.cuentapasos = 0
        self.step = 'S'
        key = 'S' + self.direccion
        self.image = self.imagen_n(key)

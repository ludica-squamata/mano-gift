from engine.misc.resources import split_spritesheet
from engine.globs import Tiempo
from itertools import cycle
from pygame import Rect


class ModelScreen:
    _step = 'D'
    timer_animacion = 0
    images = None
    char_face = None
    anim_img = None
    face_rect = None
    hidden = False

    def __init__(self, parent):
        self.parent = parent

        # cargar imagenes
        self.faces = cycle(split_spritesheet('mobs/imagenes/pc_face.png', w=89, h=89))
        self.char_face = next(self.faces)
        self.ins_txt = 'Esto es un ejemplo para el modo Modelo'

        self.images = self.cargar_anims('mobs/imagenes/heroe_idle_walk.png')
        self.anim_img = self.images['Sabajo']
        self.anim_rect = Rect(107, 100, 32, 32)
        self.face_rect = self.char_face.get_rect(x=200)
        self.face_rect.centery = self.anim_rect.centery

    @staticmethod
    def cargar_anims(ruta_imgs):
        dicc = {}
        spritesheet = split_spritesheet(ruta_imgs)
        idx = -1
        for L in ['S', 'I', 'D']:
            for D in ['abajo', 'arriba', 'izquierda', 'derecha']:
                key = L + D
                idx += 1
                dicc[key] = spritesheet[idx]

        return dicc

    def animar_sprite(self):
        """Cambia la imagen del sprite para mostrarlo animado"""

        self.timer_animacion += Tiempo.FPS.get_time()
        if self.timer_animacion >= 250:
            self.timer_animacion = 0
            if self._step == 'D':
                self._step = 'I'
            else:
                self._step = 'D'

            key = self._step + 'abajo'
            self.anim_img = self.images[key]

    def update(self):
        self.animar_sprite()
        if not self.hidden:
            self.parent.canvas.blit(self.anim_img, self.anim_rect.topleft)
            self.parent.canvas.blit(self.char_face, self.face_rect.topleft)

    def toggle_hidden(self):
        self.hidden = not self.hidden

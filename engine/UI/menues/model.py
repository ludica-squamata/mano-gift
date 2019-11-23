from engine.globs.event_dispatcher import EventDispatcher
from engine.misc.resources import split_spritesheet
from engine.globs import Tiempo, CANVAS_BG, TEXT_FG
from pygame import font, Rect
from .menu import Menu
from engine.libs import render_textrect
from os import getcwd, path, listdir


class MenuModel(Menu):
    _step = 'D'
    timer_animacion = 0
    images = None
    char_face = None
    anim_img = None

    def __init__(self):
        super().__init__('ModelMenu', 'Avatar')

        self.images = self.cargar_anims('mobs/imagenes/heroe_idle_walk.png')
        self.images2 = self.cargar_anims('mobs/imagenes/green_girl.png')
        self.anim_img = self.images['Sabajo']
        self.anim_img2 = self.images2['Sabajo']
        self.anim_rect = Rect(0, 0, 32, 32)
        self.anim_rect2 = Rect(0, 0, 32, 32)

        x1 = self.rect.w//5
        x2 = x1*3
        n, d, c = 'nombre', 'direcciones', 'comando'
        botones = [
            {n: 'Héroe', d: {'derecha': 'Heroína'}, c: lambda: self.set_model('el'), 'pos': [x1, 250]},
            {n: 'Heroína', d: {'izquierda': 'Héroe'}, c: lambda: self.set_model('ella'), 'pos': [x2, 250]}
        ]

        self.establecer_botones(botones, 3)
        el, ella = self.botones.sprites()
        self.anim_rect.centerx = el.rect.centerx
        self.anim_rect2.centerx = ella.rect.centerx
        self.anim_rect.bottom = el.rect.top-15
        self.anim_rect2.bottom = ella.rect.top-15

        self.print_instructions()

        self.functions = {  # obsérvese que es dict.update()
            'tap': {
                'accion': self.press_button,
                'derecha': lambda: self.select_one('derecha'),
                'izquierda': lambda: self.select_one('izquierda'),

            },
            'hold': {
                'accion': self.mantener_presion,
                'derecha': lambda: self.select_one('derecha'),
                'izquierda': lambda: self.select_one('izquierda'),
            },
            'release': {
                'accion': self.liberar_presion
            }
        }

    def set_model(self, modelo):
        imgs = {'alpha': 'mobs/colisiones/human_walk.png', 'imagenes': {}, 'final': False}
        ruta = path.join(getcwd(), 'data/grafs/mobs/imagenes')
        for filename in listdir(ruta):
            key = ''
            name = filename.rstrip('.png')
            if modelo == 'el':
                if 'heroe' in name or name.startswith('pc'):
                    if 'idle' in name:
                        key = 'idle'
                    elif 'cmb' in name and name.endswith('walk'):
                        key = 'cmb'
                    elif 'cmb' in name and name.endswith('atk'):
                        key = 'atk'
                    elif name.endswith('face'):
                        key = 'diag_face'
                    imgs['imagenes'][key] = 'mobs/imagenes/'+filename

            elif modelo == 'ella':
                if 'girl' in name or name.startswith('npc'):
                    if 'idle' in name:
                        imgs['imagenes']['idle'] = 'mobs/imagenes/'+filename
                    elif 'cmb' in name and name.endswith('walk'):
                        pass  # faltan hacer imagenes para la chica en combate
                    elif 'cmb' in name and name.endswith('atk'):
                        pass  # y para la chica peleando, sea como sea que pelee.
                    elif name.endswith('face'):
                        imgs['imagenes']['diag_face'] = 'mobs/imagenes/'+filename

        self.deregister()
        EventDispatcher.trigger('CharacterCreation', self.nombre, imgs)
        EventDispatcher.trigger('OpenMenu', self.nombre, {'value': 'Ability'})

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
            self.anim_img2 = self.images2[key]

    def print_instructions(self):
        s = 'Elige a continuación el modelo de tu personaje'
        fuente = font.SysFont('Verdana', 14, italic=True)
        rect = Rect(10, 32, 600, 64)
        render = render_textrect(s, fuente, rect, TEXT_FG, CANVAS_BG, justification=1)
        self.canvas.blit(render, rect)

    def update(self):
        self.animar_sprite()
        self.canvas.blit(self.anim_img, self.anim_rect.topleft)
        self.canvas.blit(self.anim_img2, self.anim_rect2.topleft)
        self.botones.update()
        self.botones.draw(self.canvas)

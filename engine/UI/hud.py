from engine.globs import CAPA_OVERLAYS_HUD, FEATURE_SHOW_MINIBARS, FEATURE_FLOATING_NUMBERS
from engine.globs import ANCHO, CUADRO, TEXT_FG, Mob_Group
from engine.globs.event_dispatcher import EventDispatcher
from pygame import Surface, Rect, draw, SRCALPHA, font
from engine.globs.renderer import Renderer
from pygame.sprite import Sprite


class ProgressBar(Sprite):
    """Clase base para las barras, de vida, de maná, etc"""
    focus = None
    maximo = 0
    actual = 0
    divisiones = 0
    colorAct = 0, 0, 0
    colorFnd = 0, 0, 0
    active = True
    x, y, w, h = 0, 0, 0, 0
    draw_area_rect = None
    nombre = 'ProgressBar'
    tracked_stat = ''
    do_subdivision = True

    def __init__(self, maximo, stat, color_actual, color_fondo, x, y, w, h, focus=None):
        super().__init__()

        self.colorAct = color_actual
        self.colorFnd = color_fondo
        self.maximo = maximo
        self.actual = maximo
        self.tracked_stat = stat
        self.divisiones = 1

        self.x, self.y = x, y
        self.w, self.h = w, h
        self.draw_area_rect = Rect(1, 1, self.w - 2, self.h - 2)
        self.image = Surface((self.w, self.h))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        EventDispatcher.register(self.toggle, "TogglePause")
        if focus is not None:
            self.set_focus(focus)

    def _actual(self):
        x, y, w, h = self.draw_area_rect
        return Rect((x, y), ((self.actual / self.maximo) * self.draw_area_rect.w, h))

    def _dibujar_fondo(self):
        img = Surface(self.draw_area_rect.size)
        img.fill(self.colorFnd)
        return img

    def _subdividir(self):
        dw = int(self.w / self.divisiones)
        w = 0
        for i in range(self.divisiones):
            w += dw
            draw.line(self.image, (0, 0, 0), (w, 3), (w, self.h - 3))

    def set_variable(self, **kwargs):
        """Función pública para cambiar las variables en una linea"""
        for var in kwargs:
            if hasattr(self, var):
                setattr(self, var, kwargs[var])

    def event_update(self, event):
        mob = event.data['mob']
        stat = event.data.get('stat', None)
        if mob.nombre == self.focus.nombre and stat == self.tracked_stat:
            self.set_variable(actual=event.data["value"])
            self.actualizar()

    def show(self):
        Renderer.add_overlay(self, CAPA_OVERLAYS_HUD)

    def hide(self):
        Renderer.del_overlay(self)

    def toggle(self, event):
        if event.data['value']:
            self.hide()
        else:
            self.show()

    def set_focus(self, focus):
        self.focus = focus

    def actualizar(self):
        self.image.blit(self._dibujar_fondo(), self.draw_area_rect)
        self.image.fill(self.colorAct, self._actual())
        if self.do_subdivision:
            self._subdividir()


class CharacterName(Sprite):
    active = True
    nombre = 'name'

    def __init__(self, focus, x, y):
        super().__init__()
        self.text = focus.character_name
        self.image = self.generate([255, 255, 255])
        self.rect = self.image.get_rect(topleft=(x, y))
        EventDispatcher.register(self.toggle, "TogglePause")

    def generate(self, fg_color):
        outline = []
        fuente = font.Font('engine/libs/Verdanab.ttf', 16)
        width, height = fuente.size(self.text)
        width += 2 * len(self.text)
        canvas = Surface((width, height), SRCALPHA)

        for character in self.text:
            fondo = fuente.render(character, 1, TEXT_FG)
            frente = fuente.render(character, 1, fg_color)
            w, h = fuente.size(character)
            img = Surface((w + 2, h + 2), SRCALPHA)

            for i in range(1, 8, 2):
                dx, dy = i % 3, i // 3
                img.blit(fondo, (dx, dy))
            img.blit(frente, (1, 1))
            outline.append(img)

        dx, w = 0, 0
        for img in outline:
            dx += w
            canvas.blit(img, (dx, 0))
            w = img.get_width()

        return canvas

    def colorear(self, bg_color):
        self.image = self.generate(bg_color)

    def show(self):
        Renderer.add_overlay(self, CAPA_OVERLAYS_HUD)

    def hide(self):
        Renderer.del_overlay(self)

    def toggle(self, event):
        if event.data['value']:
            self.hide()
        else:
            self.show()


class MiniBar(ProgressBar):
    do_subdivision = False
    run_timer = False

    def __init__(self):
        super().__init__(0, 'Salud', (0, 255, 0), (0, 150, 0), 0, 0, 32, 5)
        EventDispatcher.register(self.event_update, 'MobWounded', 'UsedItem')
        self.timer = 0

    def event_update(self, event):
        mob = event.data['mob']
        stat = event.data.get('stat', None)
        if not mob.has_hud and stat == self.tracked_stat:
            self.set_focus(event.data['mob'])
            self.show()

    def toggle(self, event):
        # hook para evitar un crash. No tocar.
        pass

    def show(self):
        self.maximo = self.focus['SaludMax']
        self.actual = self.focus['Salud']

        self.rect = self.image.get_rect()
        self.actualizar()

        if self.actual > 0:
            Renderer.add_overlay(self, CAPA_OVERLAYS_HUD)
            self.run_timer = True

    def hide(self):
        Renderer.del_overlay(self)
        self.run_timer = False
        self.timer = 0

    def reubicar(self):
        self.rect.centerx = self.focus.rect.centerx
        self.rect.centery = self.focus.rect.y - 5

    def update(self):
        self.reubicar()
        if self.run_timer:
            self.timer += 1
            if self.timer > 30:
                self.hide()


class FloatingNumber(Sprite):
    image = None
    rect = None
    active = True
    timer = 0

    def __init__(self):
        super().__init__()
        self.fuente = font.SysFont('Verdana', 11)
        EventDispatcher.register(self.show, 'MobWounded', 'UsedItem')

    def show(self, event):
        factor = event.data['factor']
        mob_rect = event.data['mob'].rect
        if factor < 0:
            color = 255, 0, 0
        else:
            color = 0, 255, 0

        string = str(factor).lstrip('-')
        self.image = self.fuente.render(string, 1, color)
        self.rect = self.image.get_rect(midbottom=mob_rect.midtop)
        Renderer.add_overlay(self, CAPA_OVERLAYS_HUD)

    def update(self):
        self.timer += 1
        self.rect.centery -= 1
        if self.timer == 15:
            self.timer = 0
            Renderer.del_overlay(self)


class HUD:

    @classmethod
    def init(cls):
        focus = Mob_Group.get_controlled_mob()
        focus.has_hud = True
        _rect = Renderer.camara.rect
        w, h = ANCHO // 4, CUADRO // 4
        dx, dy = _rect.x + 3, _rect.y + 50
        barra_vida = ProgressBar(focus["SaludMax"], 'Salud', (200, 50, 50), (100, 0, 0), dx, dy - 11, w, h, focus)
        barra_mana = ProgressBar(focus['ManaMax'], 'Mana', (125, 0, 255), (75, 0, 100), dx, dy - 1, w, h, focus)
        barra_vida.set_variable(divisiones=4)
        CharacterName(focus, dx, dy - 32)

        EventDispatcher.register(barra_vida.event_update, 'MobWounded', 'UsedItem')
        EventDispatcher.deregister(cls.init, 'LoadGame')

        if FEATURE_SHOW_MINIBARS:
            MiniBar()
        elif FEATURE_FLOATING_NUMBERS:
            FloatingNumber()

        barra_vida.actualizar()
        barra_mana.actualizar()


EventDispatcher.register(lambda e: HUD.init(), 'LoadGame')

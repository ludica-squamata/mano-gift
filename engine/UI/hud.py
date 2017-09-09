from engine.globs import CAPA_OVERLAYS_HUD, ANCHO, CUADRO
from engine.globs.eventDispatcher import EventDispatcher
from pygame import Surface, Rect, draw, SRCALPHA
from engine.globs.renderer import Renderer
from engine.UI.estilo import Estilo
from pygame.sprite import Sprite


class ProgressBar(Sprite):
    """Clase base para las barras, de vida, de maná, etc"""
    maximo = 0
    actual = 0
    divisiones = 0
    colorAct = 0, 0, 0
    colorFnd = 0, 0, 0
    active = True
    x, y, w, h = 0, 0, 0, 0
    draw_area_rect = None

    def __init__(self, focus, maximo, color_actual, color_fondo, x, y, w, h):
        super().__init__()

        self.colorAct = color_actual
        self.colorFnd = color_fondo
        self.maximo = maximo
        self.actual = maximo
        self.focus = focus
        self.divisiones = 1

        self.x, self.y = x, y
        self.w, self.h = w, h
        self.draw_area_rect = Rect(1, 1, self.w - 1, self.h - 2)
        self.image = Surface((self.w, self.h))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def _actual(self):
        x, y, w, h = self.draw_area_rect
        return Rect((x, y), (self.actual / self.maximo * self.w - 3, h))

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
        if mob.nombre == self.focus:
            self.set_variable(actual=mob.salud_act)
            self.actualizar()

    def actualizar(self):
        self.image.blit(self._dibujar_fondo(), self.draw_area_rect)
        self.image.fill(self.colorAct, self._actual())
        self._subdividir()


class CharacterName(Sprite, Estilo):
    active = True

    def __init__(self, focus, x, y):
        super().__init__()
        self.text = focus
        self.image = self.generate([255, 255, 255])
        self.rect = self.image.get_rect(topleft=(x, y))

    def generate(self, fg_color):
        outline = []
        width, height = self.fuente_Mb.size(self.text)
        width += 2 * len(self.text)
        canvas = Surface((width, height), SRCALPHA)

        for character in self.text:
            fondo = self.fuente_Mb.render(character, 1, self.font_none_color)
            frente = self.fuente_Mb.render(character, 1, fg_color)
            w, h = self.fuente_Mb.size(character)
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


class HUD:
    # ya no es clase base. próximamente será una clase que agrupe
    # y registre en el renderer todos los elementos del hud.
    is_shown = False
    BarraVida = None
    BarraMana = None
    screen_name = None

    def __init__(self, focus):
        _rect = Renderer.camara.rect
        w, h = ANCHO // 4, CUADRO // 4
        dx, dy = _rect.x + 3, _rect.y + 50
        self.BarraVida = ProgressBar(focus.nombre, focus.salud_act, (200, 50, 50), (100, 0, 0), dx, dy - 11, w, h)
        self.BarraMana = ProgressBar(focus.nombre, focus.mana, (125, 0, 255), (75, 0, 100), dx, dy - 1, w, h)
        self.BarraVida.set_variable(divisiones=4)
        self.screen_name = CharacterName(focus.nombre, dx, dy - 32)

        EventDispatcher.register(self.BarraVida.event_update, 'MobWounded')
        # EventDispatcher.register(self.BarraMana.event_update,'')
        # EventDispatcher.register(self.BarraVida.event_update,'')

        self.BarraVida.actualizar()
        self.BarraMana.actualizar()

    def show(self):
        if not self.is_shown:
            Renderer.add_overlay(self.BarraVida, CAPA_OVERLAYS_HUD)
            Renderer.add_overlay(self.BarraMana, CAPA_OVERLAYS_HUD)
            Renderer.add_overlay(self.screen_name, CAPA_OVERLAYS_HUD)
            self.is_shown = True

    def hide(self):
        self.is_shown = False
        Renderer.clear_overlays_from_layer(CAPA_OVERLAYS_HUD)

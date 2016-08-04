from pygame import Surface, Rect, draw
from pygame.sprite import Sprite
from engine.globs import EngineData as Ed, CAPA_OVERLAYS_HUD, ANCHO, CUADRO
from engine.globs.renderer import Renderer


class ProgressBar(Sprite):
    """Clase base para las barras, de vida, de maná, etc"""
    maximo = 0
    actual = 0
    divisiones = 0
    colorAct = 0, 0, 0
    colorFnd = 0, 0, 0
    active = True

    def __init__(self, maximo, color_actual, color_fondo, x, y, w, h):
        super().__init__()

        self.colorAct = color_actual
        self.colorFnd = color_fondo
        self.maximo = maximo
        self.actual = maximo
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

    def update(self):
        self.image.blit(self._dibujar_fondo(), self.draw_area_rect)
        self.image.fill(self.colorAct, self._actual())
        self._subdividir()


class HUD:
    # ya no es clase base. próximamente será una clase que agrupe
    # y registre en el renderer todos los elementos del hud.
    def __init__(self):
        _rect = Renderer.camara.rect
        w, h = ANCHO // 4, CUADRO // 4
        dx, dy = _rect.x+3, _rect.y + 33
        self.BarraVida = ProgressBar(Ed.HERO.salud_max, (200, 50, 50), (100, 0, 0), dx, dy - 11, w, h)
        self.BarraMana = ProgressBar(Ed.HERO.mana, (125, 0, 255), (75, 0, 100), dx, dy - 1, w, h)
        self.BarraVida.set_variable(divisiones=4)

    def show(self):
        Renderer.add_overlay(self.BarraVida, CAPA_OVERLAYS_HUD)
        Renderer.add_overlay(self.BarraMana, CAPA_OVERLAYS_HUD)

    @staticmethod
    def hide():
        Renderer.clear_overlays_from_layer(CAPA_OVERLAYS_HUD)

    def update(self):
        self.BarraVida.set_variable(actual=Ed.HERO.salud_act)

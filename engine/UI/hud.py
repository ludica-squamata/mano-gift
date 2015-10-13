from pygame import Surface, Rect, draw
from pygame.sprite import Sprite
from engine.globs import Constants as Cs, EngineData as Ed


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
        self.rect = self.image.get_rect(topleft = (self.x, self.y))

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
        _rect = Ed.RENDERER.camara.rect
        w, h = Cs.ANCHO // 4, Cs.CUADRO // 4
        dx, dy = _rect.centerx, _rect.bottom - 33
        self.BarraVida = ProgressBar(Ed.HERO.salud_max, (200, 50, 50), (100, 0, 0), dx - w - 1, dy - 11, w, h)
        self.BarraMana = ProgressBar(Ed.HERO.mana, (125, 0, 255), (75, 0, 100), dx + 2, dy - 11, w, h)
        self.BarraVida.set_variable(divisiones = 4)
        Ed.RENDERER.addOverlay(self.BarraVida, Cs.CAPA_OVERLAYS_HUD)
        Ed.RENDERER.addOverlay(self.BarraMana, Cs.CAPA_OVERLAYS_HUD)

    def usar_funcion(self, tecla):
        pass

    def update(self):
        self.BarraVida.set_variable(actual = Ed.HERO.salud_act)

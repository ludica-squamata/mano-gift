from engine.IO.menucircular import CircularMenu, BaseElement
from pygame import font, Surface, SRCALPHA
from engine.globs.renderer import Renderer
from engine.globs import EngineData as Ed
from pygame.sprite import Sprite


class LetterElement(BaseElement):
    def __init__(self, parent, nombre):
        super().__init__(parent, nombre)
        self._crear_titulo()

    @staticmethod
    def _crear_base(w, h):
        image = Surface((w, h), SRCALPHA)
        image.fill((0, 0, 0, 255))
        image.fill((125, 125, 125, 200), (1, 1, w - 2, h - 2))

        rect = image.get_rect()
        return image, rect

    def _crear_icono_texto(self, icono, w, h):
        image, _rect = self._crear_base(w, h)

        fuente = font.SysFont('Verdana', 15, bold=True)
        render = fuente.render(icono, 1, (0, 0, 0))
        renderect = render.get_rect(center=_rect.center)
        image.blit(render, renderect)
        return image

    def _crear_titulo(self):
        fuente = font.SysFont('Verdana', 15, bold=True)
        w, h = fuente.size(self.nombre)
        negro = 0, 0, 0
        gris = 125, 125, 125

        self.title = Sprite()
        self.title.active = True
        self.title.image = Surface((w + 6, h + 2))
        self.title.image.fill(gris, (1, 1, w + 4, h))
        self.title.image.blit(fuente.render(self.nombre, 1, negro, gris), (2, 1))
        self.title.rect = self.title.image.get_rect()

    def update(self):
        super().update()
        self.title.rect.center = (self.rect.centerx, self.rect.bottom + 15)


class RenderedCircularMenu(CircularMenu):
    layer = 0

    def __init__(self, cascadas):
        cx, cy = Renderer.camara.rect.center
        super().__init__(cascadas, cx, cy)
        self.last_on_spot = self.check_on_spot()

    def _update_rendered(self):
        self.last_on_spot = self.check_on_spot()
        Renderer.clear_overlays_from_layer(self.layer)
        for cuadro in self.cubos:
            Renderer.add_overlay(cuadro, self.layer)
        if self.last_on_spot is not None:
            Renderer.add_overlay(self.last_on_spot.title, self.layer)

    def _change_cube_list(self):
        super()._change_cube_list()
        self._update_rendered()

    def supress(self):
        super().supress()
        self._update_rendered()

    def _modify_cube_list(self):
        super()._modify_cube_list()
        self._update_rendered()

    def stop_everything(self, on_spot):
        super().stop_everything(on_spot)
        self.last_on_spot = on_spot
        Renderer.add_overlay(on_spot.title, self.layer)

    def turn(self, delta):
        super().turn(delta)
        Renderer.del_overlay(self.last_on_spot.title)

    def show(self):
        Renderer.add_overlay(self.last_on_spot.title, self.layer)
        for cubo in self.cubos:
            Renderer.add_overlay(cubo, self.layer)

    def salir(self):
        if self.cascadaActual == 'inicial':
            Renderer.clear_overlays_from_layer(self.layer)
            Ed.DIALOGO = None
            Ed.MODO = 'Aventura'

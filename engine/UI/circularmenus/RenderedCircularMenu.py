from engine.IO.menucircular import CircularMenu, BaseElement
from pygame import font, Surface, SRCALPHA
from engine.globs.renderer import Renderer
from engine.globs import EngineData as Ed


class LetterElement(BaseElement):

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


class RenderedCircularMenu(CircularMenu):
    layer = 0

    def __init__(self, cascadas):
        cx, cy = Renderer.camara.rect.center
        super().__init__(cascadas, cx, cy)

    def _change_cube_list(self):
        super()._change_cube_list()
        Renderer.clear_overlays_from_layer(self.layer)
        for cuadro in self.cubos:
            Renderer.add_overlay(cuadro, self.layer)

    def supress(self):
        super().supress()
        Renderer.clear_overlays_from_layer(self.layer)
        for cuadro in self.cubos:
            Renderer.add_overlay(cuadro, self.layer)

    def _modify_cube_list(self):
        super()._modify_cube_list()
        Renderer.clear_overlays_from_layer(self.layer)
        for cuadro in self.cubos:
            Renderer.add_overlay(cuadro, self.layer)

    def show(self):
        for cubo in self.cubos:
            Renderer.add_overlay(cubo, self.layer)

    def salir(self):
        if self.cascadaActual == 'inicial':
            Renderer.clear_overlays_from_layer(self.layer)
            Ed.DIALOGO = None
            Ed.MODO = 'Aventura'

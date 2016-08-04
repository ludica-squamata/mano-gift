from engine.IO.menucircular import CircularMenu, BaseElement
from engine.globs.renderer import Renderer
from engine.globs import EngineData as Ed
from pygame import Surface, SRCALPHA
from engine.UI.estilo import Estilo
from pygame.sprite import Sprite


class LetterElement(BaseElement, Estilo):
    def _crear_base(self, w, h):
        image = Surface((w, h), SRCALPHA)
        image.fill(self.font_none_color)
        gris = self.bg_cnvs
        gris.a = 200
        image.fill(gris, (1, 1, w - 2, h - 2))

        rect = image.get_rect()
        return image, rect

    def _crear_icono_texto(self, icono, w, h):
        image, _rect = self._crear_base(w, h)
        render = self.fuente_Ib.render(icono, 1, (0, 0, 0))
        renderect = render.get_rect(center=_rect.center)
        image.blit(render, renderect)
        return image


class Title(Sprite, Estilo):
    active = True

    def __init__(self, parent, nombre):
        super().__init__()
        self.nombre = nombre
        self.parent = parent

        w, h = self.fuente_Ib.size(self.nombre)
        negro = self.font_none_color
        gris = self.bg_cnvs

        self.image = Surface((w + 6, h + 2))
        self.image.fill(gris, (1, 1, w + 4, h))
        self.image.blit(self.fuente_Ib.render(nombre, 1, negro, gris), (2, 1))
        self.rect = self.image.get_rect(center=(self.parent.rect.centerx, self.parent.rect.bottom + 15))

    def center(self, rect):
        self.rect.center = (rect.centerx, rect.bottom + 15)

    def update(self, *args):
        self.center(self.parent.rect)


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
        on_spot.title.update()
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

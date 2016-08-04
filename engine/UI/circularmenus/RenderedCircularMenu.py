from engine.IO.menucircular import CircularMenu
from engine.globs.renderer import Renderer
from engine.globs import EngineData as Ed


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

    def supress_all(self):
        super().supress_all()
        self._update_rendered()

    def _modify_cube_list(self):
        super()._modify_cube_list()
        self._update_rendered()

    def stop_everything(self, on_spot):
        super().stop_everything(on_spot)
        self.last_on_spot = on_spot
        on_spot.title.update()
        if hasattr(on_spot, 'description'):
            Renderer.add_overlay(on_spot.description, self.layer)
        Renderer.add_overlay(on_spot.title, self.layer)

    def turn(self, delta):
        super().turn(delta)
        Renderer.del_overlay(self.last_on_spot.title)
        if hasattr(self.last_on_spot, 'description'):
            Renderer.del_overlay(self.last_on_spot.description)

    def show(self):
        Renderer.add_overlay(self.last_on_spot.title, self.layer)
        for cubo in self.cubos:
            Renderer.add_overlay(cubo, self.layer)

    def salir(self):
        if self.cascadaActual == 'inicial':
            Renderer.clear_overlays_from_layer(self.layer)
            Ed.DIALOGO = None
            Ed.MODO = 'Aventura'

    def update(self):
        # this hook is necesary
        pass

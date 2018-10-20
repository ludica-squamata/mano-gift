from engine.globs.constantes import CAPA_OVERLAYS_CIRCULAR
from engine.globs.eventDispatcher import EventDispatcher
from engine.IO.menucircular import CircularMenu
from engine.globs.renderer import Renderer
from engine.globs import EngineData


class RenderedCircularMenu(CircularMenu):
    layer = CAPA_OVERLAYS_CIRCULAR
    last_on_spot = None

    def __init__(self, cascadas):
        cx, cy = Renderer.camara.rect.center
        super().__init__(cascadas, cx, cy)
        EngineData.MODO = 'Dialogo'
        self._update_rendered()

    def _update_rendered(self, on_spot=None):
        Renderer.clear(layer=self.layer)
        for cuadro in self.cuadros:
            Renderer.add_overlay(cuadro, self.layer)

        if on_spot is None:
            self.last_on_spot = self.check_on_spot()
        else:
            self.last_on_spot = on_spot

        if self.last_on_spot is not None:
            self.last_on_spot.title.update()
            Renderer.add_overlay(self.last_on_spot.title, self.layer)
            if hasattr(self.last_on_spot, 'description'):
                Renderer.add_overlay(self.last_on_spot.description, self.layer)

    def switch_cascades(self):
        super().switch_cascades()
        self._update_rendered()

    def supress_all(self):
        super().supress_all()
        self._update_rendered()

    def stop_everything(self, on_spot):
        super().stop_everything(on_spot)
        self._update_rendered(on_spot)

    def turn(self, delta):
        if self.stopped:
            Renderer.del_overlay(self.last_on_spot.title)
            if hasattr(self.last_on_spot, 'description'):
                Renderer.del_overlay(self.last_on_spot.description)
        super().turn(delta)

    def salir(self):
        if self.cascadaActual == 'inicial':
            for cuadro in self.cuadros:
                cuadro.deregister()
            self.deregister()
            EventDispatcher.trigger('EndDialog', self, {'layer': self.layer})

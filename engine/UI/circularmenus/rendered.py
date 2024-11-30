from engine.globs.constantes import CAPA_OVERLAYS_CIRCULAR
from engine.globs.event_dispatcher import EventDispatcher
from engine.IO.menu_circular import CircularMenu
from engine.globs.renderer import Renderer


class RenderedCircularMenu(CircularMenu):
    layer = CAPA_OVERLAYS_CIRCULAR
    last_on_spot = None
    first = 0

    def __init__(self, cascadas):
        cx, cy = Renderer.camara.rect.center
        self.overwritten = False
        self.set_idxs(cascadas)
        super().__init__(cascadas, cx, cy)
        self._update_rendered()

    def set_idxs(self, cascadas):
        # este loop estaba en el QCM, pero en realidad se aplica a todos los menues circulares.
        for n in cascadas:
            cascada = cascadas[n]
            for element in cascada:
                index = cascada.index(element)  # esto soluciona el tema de recordar la posición del item.
                element.index = index  # aunque me gustaria ponerlo en un onliner.

            if self.first <= len(cascada) - 1:
                for idx, opt in enumerate([cascada[self.first]] + cascada[self.first + 1:] + cascada[:self.first]):
                    opt.idx = idx
            else:
                for idx, opt in enumerate(cascada):
                    opt.idx = idx

        # La diferencia entre idx e index es sutil. Index el el número que corresponde al ID del item, que es asignado
        # "al momento de su creación". idx por otra parte, indica la posición en pantalla que el item debe tomar.

    def _update_rendered(self, on_spot=None):
        Renderer.clear(layer=self.layer)
        for cuadro in self.cuadros:
            Renderer.add_overlay(cuadro, self.layer)

        if on_spot is None:
            self.last_on_spot = self.check_on_spot()
        else:
            self.last_on_spot = on_spot

        if self.last_on_spot is not None:
            if self.last_on_spot.title is not None:
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

    def stop_everything(self, on_spot=None):
        super().stop_everything(on_spot)
        self._update_rendered(on_spot)

    def turn(self, delta):
        if self.stopped:
            Renderer.del_overlay(self.last_on_spot.title)
            if hasattr(self.last_on_spot, 'description'):
                Renderer.del_overlay(self.last_on_spot.description)
        super().turn(delta)

    def salir(self):
        if self.cascadaActual == 'inicial' or self.overwritten:
            for cuadro in self.cuadros:
                cuadro.deregister()
            self.deregister()
            EventDispatcher.trigger('EndDialog', self, {'layer': self.layer})

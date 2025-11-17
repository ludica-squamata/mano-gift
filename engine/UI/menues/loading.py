from engine.globs.event_dispatcher import EventDispatcher
from engine.globs import CAPA_OVERLAYS_MENUS
from pygame import Surface, Rect
from .menu import Menu


class LoadingMenu(Menu):
    def __init__(self, parent):
        super().__init__(parent, 'loading', '')
        EventDispatcher.register(self.toggle, "TogglePause")

        self.progress = Surface([300, 32])
        self.progress.fill([0, 255, 0])
        self.progress_rect = self.progress.get_rect(center=self.rect.center)
        self.canvas.blit(self.progress, self.progress_rect)
        self.functions['tap'].update({'contextual': lambda: None})  # to prevent a crash with the "cancel" key.

    def toggle(self, event):
        if event.data['value']:
            EventDispatcher.trigger('EndDialog', self.nombre, {'layer': CAPA_OVERLAYS_MENUS})
            EventDispatcher.deregister(self.toggle, "TogglePause")

    def actualizar(self, dx):
        paint_rect = Rect([0, 0, int(dx * 300), 32])
        self.progress.fill([255, 0, 0], paint_rect)
        self.canvas.blit(self.progress, self.progress_rect)

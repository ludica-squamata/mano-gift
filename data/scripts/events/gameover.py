from engine.globs.event_dispatcher import EventDispatcher
from engine.globs.azoe_group import AzoeBaseSprite
from engine.globs.renderer import Renderer
from engine.misc.util import salir
from engine.globs import Mob_Group
from pygame import Surface, font


class FadingScreen(AzoeBaseSprite):
    active = True
    a, t, x = 0, 255, 0

    def __init__(self):
        image = Surface((640, 480))
        rect = image.get_rect()
        text = 'Game Over'
        fuente = font.SysFont('verdana', 50)
        self.msg = fuente.render(text, 1, [255, 0, 0])
        self.m_r = self.msg.get_rect(center=rect.center)
        super().__init__(None, text, image, rect)
        self.image.blit(self.msg, self.m_r)

    def update(self):
        self.a += 1
        if self.a <= 255:
            self.image.set_alpha(self.a)
        elif self.a > 600:
            salir('gameover')


def gameover(evento):
    if evento.data['obj'].nombre == Mob_Group.get_controlled_mob().nombre:
        Renderer.add_overlay(FadingScreen(), 50)


EventDispatcher.register(gameover, "MobDeath")

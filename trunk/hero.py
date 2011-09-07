#coding: utf-8
import pygame

from mobs_base import Mob
from gift_util import Globales, cargar_imagen, Grupos

class Hero (Mob):
    ARRIBA, ABAJO, IZQUIERDA, DERECHA = 0, 1, 2, 3
    RANGO_VISION = 10
    variacion_velocidad = 4
    def __init__(self):
        self.images=(cargar_imagen('heroeE.png'),cargar_imagen('heroeF.png'),cargar_imagen('heroeI.png'),cargar_imagen('heroeD.png'))
        self.image=self.images[1]
        super().__init__()
        self.rect.y=8*Globales.TAMANIO_CUADRO
        self.rect.x=8*Globales.TAMANIO_CUADRO
        self.dirty = 1
        self.direccion = 0
    def mover(self,direccion):
        delta = Globales.VELOCIDAD*self.variacion_velocidad
        dx = dy = 0
        if direccion==self.ARRIBA:
            dy = delta
        if direccion==self.ABAJO:
            dy = -delta
        if direccion==self.IZQUIERDA:
            dx = delta
        if direccion==self.DERECHA:
            dx = -delta

        self.image=self.images[direccion]

        colisiona = True
        self.rect.x -= dx
        self.rect.y -= dy
        if pygame.sprite.spritecollideany(self,Grupos.gSolidos) is None:
            colisiona=False
        self.rect.x += dx
        self.rect.y += dy

        if not colisiona:
            Grupos.gMovibles.reubicar(dx,dy)

        self.direccion = direccion
        self.dirty=1

    def accion (self):
        dx = dy = 0
        if self.direccion == Hero.ARRIBA:
            dy = - Hero.RANGO_VISION
        elif self.direccion == Hero.ABAJO:
            dy = Hero.RANGO_VISION
        elif self.direccion == Hero.IZQUIERDA:
            dx = - Hero.RANGO_VISION
        elif self.direccion == Hero.DERECHA:
            dx = Hero.RANGO_VISION

        self.rect.y += dy
        self.rect.x += dx
        enRadio = pygame.sprite.spritecollideany(self,Grupos.gNPC)
        self.rect.y -= dy
        self.rect.x -= dx

        if enRadio is not None:
            enRadio.hablar()
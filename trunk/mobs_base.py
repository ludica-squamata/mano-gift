#coding: utf-8
import pygame
import gift_util

class MobGroup(pygame.sprite.LayeredDirty):
    def __init__(self, *mobs, **kwargs):
        super().__init__(*mobs,**kwargs)
    def reubicar (self,x,y):
        for sprite in self:
            sprite.rect.y += y
            sprite.rect.x += x
            sprite.dirty = 1

class Mob (pygame.sprite.DirtySprite):
    variacion_velocidad = 0
    pos = gift_util.Pos()
    def __init__ (self, *mobgroups):
        super().__init__(mobgroups)
        self.dirty = 1
        self.rect = self.image.get_rect()
    def mover(self):
        pass
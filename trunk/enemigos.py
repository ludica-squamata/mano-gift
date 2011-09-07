#coding: utf-8
import pygame

from mobs_base import Mob
from gift_util import cargar_imagen, Globales, Grupos

class Enemy (Mob):
    variacion_velocidad=10
    def __init__(self):
        self.image=cargar_imagen('Enemy.png')
        super().__init__()
        self.rect.y=70
        self.rect.x=0
        self.pos.x=0
        self.pos.y=70
        self.direccion=1
    def mover(self):
        delta=Globales.VELOCIDAD*self.variacion_velocidad*self.direccion
        self.rect.x += delta
        self.pos.x += delta
        if pygame.sprite.spritecollideany(self,Grupos.gHeroe) == None:
            if (0 >= self.pos.x):
                self.direccion = 1 # Derecha
            elif (self.pos.x >= 200):
                self.direccion = -1 # Izquierda
        else:
            self.direccion *= -1 # Cambiá
            self.rect.x -= delta
            self.pos.x -= delta
        self.dirty=1
#coding: utf-8
from mobs_base import Mob
from gift_util import cargar_imagen

class Vendor (Mob):
    def __init__(self):
        self.image=cargar_imagen('Vendor.png')
        super().__init__()
        self.rect.y=30
        self.rect.x=150
    def interactuar(self):
        print ('Bienvenido')
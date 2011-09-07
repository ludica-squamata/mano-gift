#coding: utf-8
import pygame
import gift_util

class Objeto:
    pass

class Tesoro (pygame.sprite.DirtySprite):
    contenido = list()
    def __init__ (self):
        self.images = gift_util.cargar_imagen('CofreC.png'),gift_util.cargar_imagen('CofreA.png')
        self.image = self.images[0]
        super().__init__()
        self.rect = self.image.get_rect()
    def interactuar (self):
        self.image = self.images[1]
        self.dirty = 1
        if self.contenido == []:
            print ('no hay nada')
        else:
            imprimir = ''
            for elemento in self.contenido:
                imprimir += str(elemento)+', '
                gift_util.Globales.inventario.guardar(elemento)
            imprimir = imprimir.rstrip(', ')+'.'
            print (imprimir)
            self.contenido = []

class Inventario:
    contenido = list()
    def __init__(self):
        self.contenido = list()
    def abrir(self):
        imprimir = ''
        for i in self.contenido:
            imprimir += i+', '
        imprimir = imprimir.rstrip(', ')+'.'
        print(imprimir.title())
    
    def guardar(self,objeto):
        self.contenido.append(objeto)
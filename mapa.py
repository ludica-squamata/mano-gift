import pygame
from pygame import sprite
from misc import Resources as r
from globs import Constants as C
from base import _giftSprite

class Prop (_giftSprite):
    '''Clase para los objetos de ground_items'''

    #basicamente, sprites que no se mueven
    #para las cosas en pantalla que tienen interaccion(tronco de arbol, puerta, piedras, loot)
    #como los árboles de pokemon que se pueden golpear
    #si solo son colisiones, conviene dibujarlo directo en el fondo
    def __init__(self,imagen,x,y):
        super().__init__()
        self.x = x
        self.y = y
        self.image = r.cargar_imagen(imagen)
        self.rect = self.image.get_rect()

class Stage:
    contents = sprite.LayeredDirty()
    mapa = None
    hero = None
    data = {}

    def __init__(self, data, entrada = None):
        self.data = data
        mapa = sprite.DirtySprite()
        mapa.image = r.cargar_imagen(data['capa_background']['fondo'])
        mapa.rect = mapa.image.get_rect()
        mapa.mask = pygame.mask.from_threshold(r.cargar_imagen(data['capa_background']['colisiones']), C.COLOR_COLISION, (1,1,1,255))
        self.mapa = mapa
        self.contents.add(mapa, layer=C.CAPA_BACKGROUND)
        self.cargar_props()

    def cargar_props (self):
        objetos = []
        return

    def cargar_hero(self, hero, entrada = None):
        self.hero = hero
        if entrada != None:
            if entrada in self.data['entradas']:
                hero.ubicar(self.data['entradas'][entrada][0]*C.CUADRO, self.data['entradas'][entrada][1]*C.CUADRO)
        self.contents.add(hero, layer=C.CAPA_GROUND_MOBS)
        self.centrar_camara()

    def mover(self,dx,dy):
        m = self.mapa
        h = self.hero

        dx *= h.velocidad
        dy *= h.velocidad

        #todos los controles contra posicion de hero restan, porque se mueve al reves que la pantalla
        if m.mask.overlap(h.mask,(h.mapX - dx, h.mapY)) is not None:
            dx = 0
        if m.mask.overlap(h.mask,(h.mapX, h.mapY - dy)) is not None:
            dy = 0

        if dx != 0:
            newPos = m.rect.x + dx
            if newPos > 0 or newPos < -(m.rect.w - C.ANCHO) or h.rect.x != h.centroX:
                if C.ANCHO > h.rect.x - dx  >=0:
                    h.reubicar(-dx, 0)
                    h.rect.x -= dx
                dx = 0

        if dy != 0:
            newPos = m.rect.y + dy
            if newPos > 0 or newPos < -(m.rect.h - C.ALTO) or h.rect.y != h.centroY:
                if C.ALTO > h.rect.y - dy  >=0:
                    h.reubicar(0, -dy)
                    h.rect.y -= dy
                dy = 0

        if dx != 0 or dy != 0:
            for spr in self.contents:
                if spr != h:
                    spr.rect.x += dx
                    spr.rect.y += dy
                    if (0 <= spr.rect.x < C.ANCHO and 0 <= spr.rect.y < C.ALTO) or spr == m:
                        spr.dirty = 1
            h.reubicar(-dx, -dy)
        h.dirty = 1

    def centrar_camara(self):
        hero = self.hero
        hero.rect.x = int(C.ANCHO / C.CUADRO / 2) * C.CUADRO
        hero.rect.y = int(C.ALTO / C.CUADRO / 2) * C.CUADRO
        hero.centroX, hero.centroY = hero.rect.topleft
        self.mapa.rect.x = hero.rect.x - hero.mapX
        self.mapa.rect.y = hero.rect.y - hero.mapY
        self.mapa.dirty = 1
        pass

    def render(self,fondo):
        #for spr in self.contents
        return self.contents.draw(fondo)

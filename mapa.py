import pygame
from pygame import sprite,Rect,Surface
from misc import Resources as r
from globs import Constants as C, World as W
from base import _giftSprite
from mobs import NPC,Enemy
from UI import Dialog

class Prop (_giftSprite):
    '''Clase para los objetos de ground_items'''
    propiedades = [] #indica si es agarrable, cortable, movible, etc.
    estado = 0
    def __init__ (self,nombre, imagen, stage, x,y, data = None):
        super().__init__(imagen,stage,x*C.CUADRO,y*C.CUADRO)
        self.nombre = nombre
        self.estado = 0
        if data != None:
            self.propiedades = data['propiedades']

    def interaccion(self):
        if 'agarrable' in self.propiedades:
            return self.agarrame()

        elif 'operable' in self.propiedades:
            if self.estado == 0:
                self.estado = 1
            else:
                self.estado = 0

            self.visible = self.propiedades['operable'][str(self.estado)]['visible']
            self.solido = self.propiedades['operable'][str(self.estado)]['solido']

    def agarrame(self): #añadir al inventario y quitar del mapa
        self.stage.contents.remove(self)
        return self.nombre

    def cambia_estado(self, ): #abrir puerta, por ejemplo
        pass


    #basicamente, sprites que no se mueven
    #para las cosas en pantalla que tienen interaccion(tronco de arbol, puerta, piedras, loot)
    #como los árboles de pokemon que se pueden golpear
    #si solo son colisiones, conviene dibujarlo directo en el fondo

class Stage:
    contents = None
    hero = None
    mapa = None
    data = {}
    dialogs = None
    def __init__(self, data):
        self.data = data
        mapa = sprite.DirtySprite()
        mapa.image = r.cargar_imagen(data['capa_background']['fondo'])
        mapa.rect = mapa.image.get_rect()
        mapa.mask = pygame.mask.from_threshold(r.cargar_imagen(data['capa_background']['colisiones']), C.COLOR_COLISION, (1,1,1,255))
        self.mapa = mapa
        self.contents = sprite.LayeredDirty()
        self.dialogs = sprite.LayeredDirty()
        self.contents.add(mapa, layer=C.CAPA_BACKGROUND)
        self.cargar_props()
        self.cargar_mobs(Enemy)
        self.cargar_mobs(NPC)
        self.cargar_salidas()

    def cargar_props (self):
        imgs = self.data['refs']
        POS_g = self.data['capa_ground']['props']
        POS_t = self.data['capa_top']['props']
        data = r.abrir_json('scripts/props.json')

        for ref in POS_g:
            for x,y in POS_g[ref]:
                if ref in data:
                    prop = Prop(ref,imgs[ref],self,x,y,data[ref])
                else:
                    prop = Prop(ref,imgs[ref],self,x,y)
                self.contents.add(prop, layer=C.CAPA_GROUND_ITEMS)
        for ref in POS_t:
            for x,y in POS_t[ref]:
                if ref in data:
                    prop = Prop(ref,imgs[ref],self,x,y,data[ref])
                else:
                    prop = Prop(ref,imgs[ref],self,x,y)
                self.contents.add(prop, layer=C.CAPA_TOP_ITEMS)

    def cargar_mobs(self,clase):
        if clase == Enemy:
            key = 'enemies'
        elif clase == NPC:
            key = 'npcs'

        imgs = self.data['refs']
        pos = self.data['capa_ground']['mobs'][key]
        data = r.abrir_json('scripts/'+key+'.json')

        for ref in pos:
            for x,y in pos[ref]:
                mob = clase(ref,imgs[ref],self,x,y,data[ref])
                self.contents.add(mob, layer=C.CAPA_GROUND_MOBS)

    def cargar_hero(self, hero, entrada = None):
        self.hero = hero
        if entrada != None:
            if entrada in self.data['entradas']:
                x,y = self.data['entradas'][entrada]
                hero.ubicar(x*C.CUADRO, y*C.CUADRO)

                hero.stage = self
                #hero.nombre = 'heroe'
                self.contents.add(hero,layer=C.CAPA_HERO)
                self.centrar_camara()

    def cargar_salidas(self):
        salidas = self.data['salidas']
        for salida in salidas:
            sld = Salida(salidas[salida])
            self.contents.add(sld,layer=C.CAPA_GROUND_ITEMS)

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

        # chequea el que héroe no atraviese a los props
        for spr in self.contents.get_sprites_from_layer(C.CAPA_GROUND_ITEMS):
            if h.colisiona(spr,-dx,-dy):
                if isinstance(spr,Salida):
                    W.setear_mapa(spr.dest,spr.link)
                if spr.solido:
                    dx,dy = 0,0

        # chequea el que héroe no atraviese a los mobs
        for spr in self.contents.get_sprites_from_layer(C.CAPA_GROUND_MOBS):
            if h.colisiona(spr,-dx,-dy):
                if spr.solido:
                    dx,dy = 0,0

        # congela la camara si el héroe se aproxima mucho a un limite horizontal
        if dx != 0:
            newPos = m.rect.x + dx
            if newPos > 0 or newPos < -(m.rect.w - C.ANCHO) or h.rect.x != h.centroX:
                if C.ANCHO > h.rect.x - dx  >=0:
                    h.reubicar(-dx, 0)
                    h.rect.x -= dx
                dx = 0

        # congela la camara si el héroe se aproxima mucho a un limite vertical
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
        mapa = self.mapa
        hero.rect.x = int(C.ANCHO / C.CUADRO / 2) * C.CUADRO #256
        hero.rect.y = int(C.ALTO / C.CUADRO / 2) * C.CUADRO #256
        hero.centroX, hero.centroY = hero.rect.topleft

        newPos = hero.rect.x - hero.mapX
        if newPos > 0 or newPos < -(mapa.rect.w - C.ANCHO):
            hero.rect.x -= newPos
        else:
            mapa.rect.x = newPos

        newPos = hero.rect.y - hero.mapY
        if newPos > 0 or newPos < -(mapa.rect.h - C.ALTO):
            hero.rect.y -= newPos
        else:
            mapa.rect.y = newPos

        mapa.dirty = 1
        self.ajustar()

    def ajustar(self):
        h = self.hero
        m = self.mapa
        for spr in self.contents:
            if spr != h and spr != m:
                spr.rect.x = m.rect.x + spr.mapX
                spr.rect.y = m.rect.y + spr.mapY

    def render(self,fondo):
        for spr in self.contents.get_sprites_from_layer(C.CAPA_GROUND_MOBS):
            spr.mover()
        ret = self.contents.draw(fondo) + self.dialogs.draw(fondo)
        return ret

    def setDialog(self, texto):
        dg = self.dialogs.get_sprites_from_layer(C.CAPA_OVERLAYS_DIALOGO)
        if len(dg) > 0:
            dg = dg[0]
            dg.setText(texto)
        else:
            dg = Dialog(texto)
            self.dialogs.add(dg, layer=C.CAPA_OVERLAYS_DIALOGO)

    def endDialog(self):
        self.dialogs.remove_sprites_of_layer(C.CAPA_OVERLAYS_DIALOGO)
        self.mapa.dirty = 1


class Salida (_giftSprite):
    def __init__(self,data):
        self.x,self.y,alto,ancho = data['rect']
        self.dest = data['dest']# string, mapa de destino.
        self.link = data['link']# string, nombre de la entrada en dest con la cual conecta
        image = pygame.Surface((alto, ancho))
        image.fill((255,0,0))
        super().__init__(image,self.x,self.y)
        self.ubicar(self.x*C.CUADRO,self.y*C.CUADRO)
        self.mask.fill()
        #self.image.set_colorkey((0,0,0))
        self.solido = False


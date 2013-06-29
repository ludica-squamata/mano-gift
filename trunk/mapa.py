import pygame
from pygame import sprite,Rect,Surface
from misc import Resources as r
from globs import Constants as C, World as W, Tiempo as T
from base import _giftSprite
from mobs import NPC,Enemy
from UI import Dialog,Menu

class Prop (_giftSprite):
    '''Clase para los objetos de ground_items.
    
    
        Estos objetos no se pueden mover por si mismos, pero usualmente tienen
        algún tipo de interacción (agarrar, mover, cortar, etc).'''
        
    propiedades = [] #indica si es agarrable, cortable, movible, etc.
    estado = 0
    def __init__ (self,nombre, imagen, stage, x,y, data = None):
        super().__init__(imagen,stage,x*C.CUADRO,y*C.CUADRO)
        self.nombre = nombre
        self.estado = 0
        if data != None:
            for prop in data['propiedades']:
                if prop == 'operable':
                    for var in data['propiedades'][prop][str(self.estado)]:
                        exec('self.'+var+'=True')
                exec('self.'+prop+'=True')

    def interaccion(self,x=0,y=0):
        if self._eval_prop('agarrable'):
            self.stage.contents.remove(self)
            return self.nombre
        
        elif self._eval_prop('operable'):
            if self.estado == 0:
                self.estado = 1
            else:
                self.estado = 0

            self.visible = not self.visible
            self.solido = not self.solido   

        elif self._eval_prop('empujable'):
            if self._eval_prop('pesado'):
                if x > 0: x -= 10
                elif x < 0: x += 10
    
                if y > 0: y -= 10
                elif y < 0: y += 10
            
            self.reubicar(x,y)
    
    def _eval_prop(self,propiedad):
        try:
            exec('self.'+propiedad)
            return True
            #pero, que ocurre si la propiedad es False?
            
        except AttributeError:
            return False
    
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
            pos = self.data['capa_ground']['mobs']['enemies']
        elif clase == NPC:
            pos = self.data['capa_ground']['mobs']['npcs']
        imgs = self.data['refs']

        for ref in pos:
            data = r.abrir_json('scripts/'+ref+'.mob')
            for x,y in pos[ref]:
                mob = clase(ref,imgs[ref],self,x,y,data)
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
            self.contents.add(sld,layer=C.CAPA_GROUND_SALIDAS)

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
                if spr.solido:
                    dx,dy = 0,0
        
        for spr in self.contents.get_sprites_from_layer(C.CAPA_GROUND_SALIDAS):
            if h.colisiona(spr,-dx,-dy):
                W.setear_mapa(spr.dest,spr.link)

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
    
    def anochecer(self,delay):
        if T.anochece(delay):
            if self.data['ambiente'] == 'exterior':
                T.noche.rect.topleft = 0,0
                self.contents.add(T.noche,layer=C.CAPA_TOP_CIELO)
        else:
            self.contents.remove_sprites_of_layer(C.CAPA_TOP_CIELO)
      
    def setDialog(self, texto):
        diags = self.dialogs.get_sprites_from_layer(C.CAPA_OVERLAYS_DIALOGO)
        if len(diags) > 0:
            dg = diags[0]
            dg.setText(texto)
        else:
            dg = Dialog(texto)
            self.dialogs.add(dg, layer=C.CAPA_OVERLAYS_DIALOGO)
    
    def popMenu (self,titulo):
        botones = r.abrir_json('menus.json')
        if titulo == 'Salir':
            self.endDialog()
            W.onPause = False
        else:
            W.onPause = True
            W.onDialog = True
            W.MENU = Menu(titulo,botones[titulo])
            self.dialogs.add(W.MENU, layer=C.CAPA_OVERLAYS_DIALOGO)
    
    def endDialog(self):
        self.dialogs.remove_sprites_of_layer(C.CAPA_OVERLAYS_DIALOGO)
        W.onDialog = False
        self.mapa.dirty = 1
    
    def update(self,fondo):
        self.anochecer(10)
        self.contents.update()
        ret = self.contents.draw(fondo) + self.dialogs.draw(fondo)
        return ret

class Salida (_giftSprite):
    def __init__(self,data):
        self.x,self.y,alto,ancho = data['rect']
        self.dest = data['dest']# string, mapa de destino.
        self.link = data['link']# string, nombre de la entrada en dest con la cual conecta
        image = pygame.Surface((alto, ancho))
        #image.fill((255,0,0))
        super().__init__(image,self.x,self.y)
        self.ubicar(self.x*C.CUADRO,self.y*C.CUADRO)
        self.mask.fill()
        self.image.set_colorkey((0,0,0))
        self.solido = False


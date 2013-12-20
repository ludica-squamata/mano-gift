from pygame import sprite, mask as MASK
from misc import Resources as r
from globs import Constants as C, World as W, Tiempo as T, QuestManager, MobGroup
from mobs import NPC, Enemy
from UI import *
from mobs.scripts.a_star import generar_grilla
from . import Prop, Salida
    
class Stage:
    contents = None
    properties = None
    hero = None
    mapa = None
    data = {}
    dialogs = None
    quest = None
    
    def __init__(self, data):
        self.data = data
        mapa = sprite.DirtySprite()
        mapa.image = r.cargar_imagen(data['capa_background']['fondo'])
        mapa.rect = mapa.image.get_rect()
        mapa.mask = MASK.from_threshold(r.cargar_imagen(data['capa_background']['colisiones']), C.COLOR_COLISION, (1,1,1,255))
        self.mapa = mapa
        self.grilla = generar_grilla(self.mapa.mask,self.mapa.image)
        self.contents = sprite.LayeredDirty()
        self.dialogs = sprite.LayeredDirty()
        self.properties = sprite.LayeredDirty()
        self.contents.add(mapa)
        self.cargar_props('ground')
        self.cargar_props('top')
        self.cargar_mobs(Enemy)
        self.cargar_mobs(NPC)
        self.cargar_quests()
        self.cargar_salidas()

    def cargar_props (self,capa):
        imgs = self.data['refs']
        POS = self.data['capa_'+capa]['props']
        data = r.abrir_json('scripts/props.json')
        if capa == 'ground':
            _layer = C.CAPA_GROUND_ITEMS
        elif capa == 'top':
            _layer = C.CAPA_TOP_ITEMS
        
        for ref in POS:
            for x,y in POS[ref]:
                if ref in data:
                    if 'image' in data[ref]:
                        imagen = data[ref]['image']
                    else:
                        imagen = imgs[ref]
                    
                    prop = Prop(ref,imagen,self,x,y,data[ref])
                else:
                    prop = Prop(ref,imgs[ref],stage=self,x=x,y=y)
                self.contents.add(prop, layer= prop.rect.bottom)
                self.properties.add(prop,layer = _layer)
                if prop.sombra != None:
                    self.cargar_sombras(prop.sombra,x*C.CUADRO,y*C.CUADRO)
    
    def cargar_sombras(self,imagen,x,y):
        self.mapa.image.blit(imagen,[x,y])

    def cargar_mobs(self,clase):
        if clase == Enemy:
            pos = self.data['capa_ground']['mobs']['enemies']
            act = 'agressive'
        elif clase == NPC:
            pos = self.data['capa_ground']['mobs']['npcs']
            act = 'passive'
        imgs = self.data['refs']

        for ref in pos:
            base = r.abrir_json('scripts/mobs/'+act+'.mob')
            try:
                data = r.abrir_json('scripts/mobs/'+ref+'.mob')
            except IOError:
                data = {}
            base.update(data)
            for x,y in pos[ref]:
                mob = clase(ref,imgs[ref],self,x,y,base)
                self.contents.add(mob, layer=mob.rect.bottom)
                self.properties.add(mob,layer = C.CAPA_GROUND_MOBS)
                MobGroup.add(mob)

    def cargar_hero(self, hero, entrada = None):
        self.hero = hero
        if entrada != None:
            if entrada in self.data['entradas']:
                x,y = self.data['entradas'][entrada]
                hero.ubicar(x*C.CUADRO, y*C.CUADRO)
                
                hero.stage = self
                self.contents.add(hero,layer=hero.rect.bottom)
                self.properties.add(hero,layer = C.CAPA_HERO)
                self.centrar_camara()
    
    def cargar_quests(self):
        if 'quests' in self.data:
            for quest in self.data['quests']:
                QuestManager.add(quest)
            
    def cargar_salidas(self):
        salidas = self.data['salidas']
        for salida in salidas:
            sld = Salida(salidas[salida])
            self.contents.add(sld,layer=sld.rect.bottom)
            self.properties.add(sld,layer=C.CAPA_GROUND_SALIDAS)

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
        for spr in self.properties.get_sprites_from_layer(C.CAPA_GROUND_ITEMS):
            if h.colisiona(spr,-dx,-dy):
                if spr.es('solido'):
                    dx,dy = 0,0
        
        for spr in self.properties.get_sprites_from_layer(C.CAPA_GROUND_SALIDAS):
            if h.colisiona(spr,-dx,-dy):
                W.setear_mapa(spr.dest,spr.link)
                dx,dy = 0,0

        # chequea el que héroe no atraviese a los mobs
        for spr in self.properties.get_sprites_from_layer(C.CAPA_GROUND_MOBS):
            if h.mask.overlap(spr.mask,(spr.mapX-(h.mapX-dx),spr.mapY-(h.mapY-dy)))!=None:
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

        #if dx != 0 or dy != 0:
        for spr in self.contents:
            if spr == m: # el mapa
                m.rect.x += dx
                m.rect.y += dy
                m.dirty = 1
            elif spr != h: # todo el resto de los sprites, excepto el heroe
                spr.rect.x += dx
                spr.rect.y += dy
                self.contents.change_layer(spr, spr.rect.bottom) 
            else: # el héroe
                self.contents.change_layer(spr, spr.rect.bottom) 
                if (0 <= spr.rect.x < C.ANCHO and 0 <= spr.rect.y < C.ALTO):
                    spr.dirty = 1
        h.reubicar(-dx, -dy)
        h.dirty = 1
        
    def centrar_camara(self):
        hero = self.hero
        mapa = self.mapa
        hero.rect.x = int(C.ANCHO / C.CUADRO / 2) * C.CUADRO #224
        hero.rect.y = int(C.ALTO / C.CUADRO / 2) * C.CUADRO #224
        hero.centroX, hero.centroY = hero.rect.topleft

        newPosX = hero.rect.x - hero.mapX
        offsetX = C.ANCHO - newPosX - mapa.rect.w
        if offsetX <= 0:
            if newPosX > 0:
                hero.rect.x -= newPosX
            else:
                mapa.rect.x = newPosX
        else:
            mapa.rect.x = newPosX+offsetX
            hero.rect.x += offsetX
        
        newPosY = hero.rect.y - hero.mapY
        offsetY = C.ALTO - newPosY - mapa.rect.h
        if offsetY <= 0:
            if newPosY > 0:
                hero.rect.y -= newPosY
            else:
                mapa.rect.y = newPosY
        else:
            mapa.rect.y = newPosY+offsetY
            hero.rect.y += offsetY
        
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
                self.contents.move_to_front(T.noche)
      
    def setDialog(self, texto,onSelect=False):
        if W.DIALOG != '':
            W.DIALOG.setText(texto,onSelect)
        else:
            W.DIALOG = Dialog(texto,onSelect)
            self.dialogs.add(W.DIALOG, layer=C.CAPA_OVERLAYS_DIALOGOS)
    
    def popMenu (self,titulo):
        if W.menu_previo == '' and W.menu_previo != titulo:
            W.menu_previo = titulo

        if titulo not in W.MENUS:
            try:
                menu = eval('Menu_'+titulo+'()')
            except Exception as Description:
                print('No se pudo abrir el menu porque:',Description)
                menu = Menu(titulo)
        else:
            menu = W.MENUS[titulo]
            menu.Reset(True)
        
        W.menu_actual = menu
        self.dialogs.add(menu)
        self.dialogs.move_to_front(menu)
            
    def endDialog(self):
        self.dialogs.empty()
        W.DIALOG = ''
        W.MODO = 'Aventura'
        self.mapa.dirty = 1
    
    def actualizar_grilla(self):
        for spr in self.properties.get_sprites_from_layer(C.CAPA_GROUND_ITEMS):
            if spr.es('solido') and not spr.es('empujable'):
                x = int(spr.mapX/32)
                y = int(spr.mapY/32)
                
                self.grilla[x,y].transitable = False
    
    def update(self,fondo):
        self.anochecer(12)
        self.contents.update()
        self.actualizar_grilla()
        self.dialogs.update()
        ret = self.contents.draw(fondo) + self.dialogs.draw(fondo)
        return ret
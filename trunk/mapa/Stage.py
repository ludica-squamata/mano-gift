from pygame.sprite import DirtySprite, LayeredDirty
from pygame import mask as MASK
from misc import Resources as r, Config as cfg
from globs import Constants as C, World as W, Tiempo as T, MobGroup
from quests import QuestManager
from mobs import NPC, Enemy, PC
from mobs.scripts.a_star import generar_grilla
from . import Prop, Salida
    
class Stage:
    properties = None
    mapa = None
    data = {}
    quest = None
    
    def __init__(self, data, entrada):
        self.data = data
        self.mapa = ChunkMap(self.data) # por ahora es uno solo.
        self.grilla = generar_grilla(self.mapa.mask,self.mapa.image)
        self.properties = LayeredDirty()
        self.cargar_hero(entrada)
        self.cargar_props('ground')
        self.cargar_props('top')
        self.cargar_mobs(Enemy)
        self.cargar_mobs(NPC)
        self.cargar_quests()
        self.cargar_salidas()
        self.addProperty(T.noche,C.CAPA_TOP_CIELO)

    def cargar_props (self,capa):
        imgs = self.data['refs']
        POS = self.data['capa_'+capa]['props']
        data = r.abrir_json('data/scripts/props.json')
        if capa == 'ground':
            layer = C.CAPA_GROUND_ITEMS
        elif capa == 'top':
            layer = C.CAPA_TOP_ITEMS
        
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
                self.addProperty(prop,layer)
                if prop.sombra != None:
                    self.mapa.image.blit(prop.sombra,[x*C.CUADRO,y*C.CUADRO])

    def cargar_mobs(self,clase):
        if clase == Enemy:
            pos = self.data['capa_ground']['mobs']['enemies']
            act = 'agressive'
        elif clase == NPC:
            pos = self.data['capa_ground']['mobs']['npcs']
            act = 'passive'
        imgs = self.data['refs']

        for ref in pos:
            base = r.abrir_json('data/mobs/'+act+'.mob')
            try:
                data = r.abrir_json('data/mobs/'+ref+'.mob')
            except IOError:
                data = {}
            base.update(data)
            for x,y in pos[ref]:
                mob = clase(ref,imgs[ref],self,x,y,base)
                self.addProperty(mob,C.CAPA_GROUND_MOBS)
                MobGroup.add(mob)

    def cargar_hero(self, entrada = None):
        W.HERO = PC('heroe',r.abrir_json('data/mobs/hero.mob'),self)
        if entrada != None:
            if entrada in self.data['entradas']:
                x,y = self.data['entradas'][entrada]
                W.HERO.ubicar(x*C.CUADRO, y*C.CUADRO)
                self.addProperty(W.HERO,C.CAPA_HERO)
    
    def cargar_quests(self):
        if 'quests' in self.data:
            for quest in self.data['quests']:
                QuestManager.add(quest)
            
    def cargar_salidas(self):
        salidas = self.data['salidas']
        for salida in salidas:
            sld = Salida(salidas[salida])
            self.properties.add(sld,layer=C.CAPA_GROUND_SALIDAS)
    
    def addProperty(self,obj,_layer):
        self.properties.add(obj,layer =_layer)
    
    def delProperty(self,obj):
        if obj in self.properties:
            self.properties.remove(obj)
        
    def anochecer(self,delay):
        if T.anochece(delay):
            if self.data['ambiente'] == 'exterior':
                T.noche.rect.topleft = 0,0
                W.RENDERER.camara.contents.move_to_front(T.noche)
    
    def actualizar_grilla(self):
        for spr in self.properties.get_sprites_from_layer(C.CAPA_GROUND_ITEMS):
            if spr.es('solido') and not spr.es('empujable'):
                x = int(spr.mapX/32)
                y = int(spr.mapY/32)
                
                self.grilla[x,y].transitable = False
    
    def update(self):
        self.anochecer(12)
        self.actualizar_grilla()
        self.mapa.dirty = 1

class ChunkMap(DirtySprite):
    #chunkmap: la idea es tener 9 de estos al mismo tiempo.
    def __init__(self,data):
        super().__init__()
        self.image = r.cargar_imagen(data['capa_background']['fondo'])
        self.rect = self.image.get_rect()
        self.mask = MASK.from_threshold(r.cargar_imagen(data['capa_background']['colisiones']), C.COLOR_COLISION, (1,1,1,255))

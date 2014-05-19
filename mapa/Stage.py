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
        _loader.setStage(self)
        _loader.loadEverything(entrada)
        self.addProperty(T.noche,C.CAPA_TOP_CIELO)

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

class _loader:
    STAGE = None
    
    @staticmethod
    def setStage(stage):
        _loader.STAGE = stage
    
    @staticmethod
    def loadEverything(entrada):
        _loader.cargar_hero(entrada)
        _loader.cargar_props('ground')
        _loader.cargar_props('top')
        _loader.cargar_mobs(Enemy)
        _loader.cargar_mobs(NPC)
        _loader.cargar_quests()
        _loader.cargar_salidas()
        
    @staticmethod
    def cargar_props (capa):
        imgs = _loader.STAGE.data['refs']
        POS = _loader.STAGE.data['capa_'+capa]['props']
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
                    
                    prop = Prop(ref,imagen,_loader.STAGE,x,y,data[ref])
                else:
                    prop = Prop(ref,imgs[ref],stage=_loader.STAGE,x=x,y=y)
                _loader.STAGE.addProperty(prop,layer)
                if prop.sombra != None:
                    _loader.STAGE.mapa.image.blit(prop.sombra,[x*C.CUADRO,y*C.CUADRO])
    
    @staticmethod
    def cargar_mobs(clase):
        if clase == Enemy:
            pos = _loader.STAGE.data['capa_ground']['mobs']['enemies']
            act = 'agressive'
        elif clase == NPC:
            pos = _loader.STAGE.data['capa_ground']['mobs']['npcs']
            act = 'passive'
        imgs = _loader.STAGE.data['refs']

        for ref in pos:
            base = r.abrir_json('data/mobs/'+act+'.mob')
            try:
                data = r.abrir_json('data/mobs/'+ref+'.mob')
            except IOError:
                data = {}
            base.update(data)
            for x,y in pos[ref]:
                mob = clase(ref,imgs[ref],_loader.STAGE,x,y,base)
                _loader.STAGE.addProperty(mob,C.CAPA_GROUND_MOBS)
                MobGroup.add(mob)
    
    @staticmethod
    def cargar_hero(entrada = None):
        W.HERO = PC('heroe',r.abrir_json('data/mobs/hero.mob'),_loader.STAGE)
        if entrada != None:
            if entrada in _loader.STAGE.data['entradas']:
                x,y = _loader.STAGE.data['entradas'][entrada]
                W.HERO.ubicar(x*C.CUADRO, y*C.CUADRO)
                _loader.STAGE.addProperty(W.HERO,C.CAPA_HERO)
    
    @staticmethod
    def cargar_quests():
        if 'quests' in _loader.STAGE.data:
            for quest in _loader.STAGE.data['quests']:
                QuestManager.add(quest)
    
    @staticmethod  
    def cargar_salidas():
        salidas = _loader.STAGE.data['salidas']
        for salida in salidas:
            sld = Salida(salidas[salida])
            _loader.STAGE.properties.add(sld,layer=C.CAPA_GROUND_SALIDAS)
    
class ChunkMap(DirtySprite):
    #chunkmap: la idea es tener 9 de estos al mismo tiempo.
    def __init__(self,data):
        super().__init__()
        self.image = r.cargar_imagen(data['capa_background']['fondo'])
        self.rect = self.image.get_rect()
        self.mask = MASK.from_threshold(r.cargar_imagen(data['capa_background']['colisiones']), C.COLOR_COLISION, (1,1,1,255))

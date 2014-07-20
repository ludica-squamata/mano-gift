from engine.globs import Constants as C, Tiempo as T, MobGroup
from engine.globs import ModData as MD, EngineData as ED
from engine.mobs.scripts.a_star import generar_grilla
from pygame.sprite import DirtySprite, LayeredDirty
from engine.misc import Resources as r
from .loader import _loader
from pygame import mask

class Stage:
    properties = None
    mapa = None
    data = {}
    quest = None
    
    def __init__(self, mobs_data, nombre, entrada):
        self.data = r.abrir_json(MD.mapas+nombre+'.json')
        self.mapa = ChunkMap(self,self.data) # por ahora es uno solo.
        self.grilla = generar_grilla(self.mapa.mask,self.mapa.image)
        self.properties = LayeredDirty()
        _loader.setStage(self)
        _loader.loadEverything(entrada,mobs_data)
        T.crear_noche(self.mapa.rect.size) #asumiendo que es uno solo...
        self.addProperty(T.noche,C.CAPA_TOP_CIELO)
        ED.RENDERER.setBackground(self.mapa)

    def addProperty(self,obj,_layer):
        obj.stage = self
        self.properties.add(obj,layer =_layer)
        ED.RENDERER.addObj(obj,obj.rect.bottom)
    
    def delProperty(self,obj):
        if obj in self.properties:
            self.properties.remove(obj)

    def anochecer(self):
        if self.data['ambiente'] == 'exterior':
            #transiciones
            if T.hora   == self.data['amanece']:  T.aclarar()
            elif T.hora == self.data['atardece']: T.oscurecer(100)
            elif T.hora == self.data['anochece']: T.oscurecer(230)
            #dia o noche establecidas
            elif self.data['amanece'] <= T.hora < self.data['atardece']:
                T.noche.image.set_alpha(0)
            elif self.data['atardece'] <= T.hora < self.data['anochece']:
                T.noche.image.set_alpha(50)
            elif 0 <= T.hora < self.data['amanece']:
                T.noche.image.set_alpha(230)
               
    def actualizar_grilla(self):
        for spr in self.properties.get_sprites_from_layer(C.CAPA_GROUND_ITEMS):
            if spr.solido:# and not spr.es('empujable'):
                x = int(spr.mapX/32)
                y = int(spr.mapY/32)
                self.grilla[x,y].transitable = False
  
class ChunkMap(DirtySprite):
    #chunkmap: la idea es tener 9 de estos al mismo tiempo.
    def __init__(self,stage,data):
        super().__init__()
        self.stage = stage
        self.image = r.cargar_imagen(data['capa_background']['fondo'])
        self.rect = self.image.get_rect()
        self.mask = mask.from_threshold(r.cargar_imagen(data['capa_background']['colisiones']), C.COLOR_COLISION, (1,1,1,255))
    
    def update(self):
        self.stage.anochecer()
        self.stage.actualizar_grilla()
        self.dirty = 1
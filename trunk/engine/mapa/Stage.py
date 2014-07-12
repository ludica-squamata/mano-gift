from pygame.sprite import DirtySprite, LayeredDirty
from pygame import mask
from engine.misc import Resources as r
from engine.globs import Constants as C, Tiempo as T, MobGroup, ModData as MD
from .loader import _loader
from engine.mobs.scripts.a_star import generar_grilla

class Stage:
    properties = None
    mapa = None
    data = {}
    quest = None
    
    def __init__(self, nombre, entrada):
        self.data = r.abrir_json(MD.mapas+nombre+'.json')
        self.mapa = ChunkMap(self,self.data) # por ahora es uno solo.
        self.grilla = generar_grilla(self.mapa.mask,self.mapa.image)
        self.properties = LayeredDirty()
        _loader.setStage(self)
        _loader.loadEverything(entrada)
        T.crear_noche(self.mapa.rect.size) #asumiendo que es uno solo...
        self.addProperty(T.noche,C.CAPA_TOP_CIELO)

    def addProperty(self,obj,_layer):
        obj.stage = self
        self.properties.add(obj,layer =_layer)
    
    def delProperty(self,obj):
        if obj in self.properties:
            self.properties.remove(obj)
       
    def actualizar_grilla(self):
        for spr in self.properties.get_sprites_from_layer(C.CAPA_GROUND_ITEMS):
            if spr.es('solido') and not spr.es('empujable'):
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
        self.stage.actualizar_grilla()
        self.dirty = 1
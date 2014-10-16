from engine.globs import Constants as C, Tiempo as T, MobGroup
from engine.globs import ModData as MD, EngineData as ED
from engine.mobs.scripts.a_star import generar_grilla
from pygame.sprite import DirtySprite, LayeredDirty
from engine.misc import Resources as r
from .loader import _loader
from pygame import mask

class Stage:
    properties = None
    interactives = []
    mapa = None
    limites = {}
    data = {}
    quest = None
    
    def __init__(self,nombre,mobs_data,entrada):
        self.nombre = nombre
        self.data = r.abrir_json(MD.mapas+nombre+'.json')
        self.mapa = ChunkMap(self,self.data) # por ahora es uno solo.
        self.grilla = generar_grilla(self.mapa.mask,self.mapa.image)
        self.properties = LayeredDirty()
        _loader.setStage(self)
        _loader.loadEverything(entrada,mobs_data)
        T.crear_noche(self.mapa.rect.size) #asumiendo que es uno solo...
        self.addProperty(T.noche,C.CAPA_TOP_CIELO)
        self.register_at_renderer(entrada)
    
    def register_at_renderer(self,entrada):
        ED.RENDERER.setBackground(self.mapa)
        for obj in self.properties:
            obj.stage = self
            ED.RENDERER.addObj(obj,obj.rect.bottom)
            
        ED.HERO.ubicar(*self.data['entradas'][entrada])
    
    def addProperty(self,obj,_layer,addInteractive=False):
        self.properties.add(obj,layer =_layer)
        if addInteractive:
            self.interactives.append(obj)
    
    def delProperty(self,obj):
        if obj in self.properties:
            self.properties.remove(obj)
        if obj in self.interactives:
            self.interactives.remove(obj)
        ED.RENDERER.delObj(obj)
    
    def anochecer(self):
        if self.data['ambiente'] == 'exterior':
            #transiciones
            if T.hora   == self.data['amanece']:  T.aclarar()
            elif T.hora == self.data['atardece']: T.oscurecer(100)
            elif T.hora == self.data['anochece']: T.oscurecer(150)
            #dia o noche establecidas
            elif self.data['amanece'] <= T.hora < self.data['atardece']:
                T.noche.image.set_alpha(0)
            elif self.data['atardece'] <= T.hora < self.data['anochece']:
                T.noche.image.set_alpha(100)
            elif 0 <= T.hora < self.data['amanece']:
                T.noche.image.set_alpha(150)
        elif self.data['ambiente'] == 'interior':
            T.noche.image.set_alpha(0)
               
    def actualizar_grilla(self):
        for spr in self.properties.get_sprites_from_layer(C.CAPA_GROUND_ITEMS):
            if spr.solido:# and not spr.es('empujable'):
                x = int(spr.mapX/32)
                y = int(spr.mapY/32)
                self.grilla[x,y].transitable = False
    
    def __repr__(self):
        return "Stage "+self.nombre+'('+str(self.properties)+')'
  
class ChunkMap(DirtySprite):
    #chunkmap: la idea es tener 9 de estos al mismo tiempo.
    tipo = 'mapa'
    def __init__(self,stage,data):
        super().__init__()
        self.stage = stage
        self.image = r.cargar_imagen(data['capa_background']['fondo'])
        self.rect = self.image.get_rect()
        self.mask = mask.from_threshold(r.cargar_imagen(data['capa_background']['colisiones']), C.COLOR_COLISION, (1,1,1,255))
    
    def ubicar(self, x, y):
        '''Coloca al sprite en pantalla'''
        self.rect.x = x
        self.rect.y = y
        if self.image != None:
            self.dirty = 1
    
    def update(self):
        self.stage.anochecer()
        self.stage.actualizar_grilla()
        self.dirty = 1
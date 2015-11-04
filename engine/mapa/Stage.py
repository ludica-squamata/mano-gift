from engine.globs import Constants as C, Tiempo as T, MobGroup, TimeStamp
from engine.globs import ModData as MD, EngineData as ED
from engine.mobs.scripts.a_star import generar_grilla
from pygame.sprite import Sprite, LayeredUpdates
from engine.globs.renderer import Renderer
from engine.misc import Resources as r
from .loader import _loader
from .LightSource import DayLight, SpotLight
from pygame import mask, Rect

class Stage:
    properties = None
    interactives = []
    mapa = None
    limites = {'sup':None,'supizq':None,'supder':None,
               'inf':None,'infizq':None,'infder':None,
               'izq':None,'der' : None}
    data = {}
    quest = None
    
    def __init__(self,nombre,mobs_data,entrada):
        self.nombre = nombre
        self.data = r.abrir_json(MD.mapas+nombre+'.json')
        self.mapa = ChunkMap(self,self.data,nombre) # por ahora es uno solo.
        self.rect = self.mapa.rect.copy()
        self.grilla = generar_grilla(self.mapa.mask,self.mapa.image)
        self.properties = LayeredUpdates()
        self.salidas = [] #aunque en realidad, las salidas deberian ser del chunk, o no?
        self.cargar_timestamps()
        _loader.setStage(self)
        _loader.loadEverything(entrada,mobs_data)
    
    def register_at_renderer(self,entrada):
        Renderer.camara.set_background(self.mapa)
        T.crear_noche(self.rect.size) #asumiendo que es uno solo...
        T.noche.set_lights(DayLight(1024))
        self.addProperty(T.noche,C.CAPA_TOP_CIELO)
        for obj in self.properties:
            ''':type obj: AzoeSprite'''
            obj.stage = self
            Renderer.camara.add_real(obj)
        
        ED.HERO.ubicar(*self.data['entradas'][entrada])
    
    def addProperty(self,obj,_layer,addInteractive=False):
        if _layer == C.CAPA_GROUND_SALIDAS:
            self.salidas.append(obj)
        else:
            self.properties.add(obj,layer =_layer)
            if addInteractive:
                self.interactives.append(obj)
    
    def delProperty(self,obj):
        if obj in self.properties:
            self.properties.remove(obj)
        if obj in self.interactives:
            self.interactives.remove(obj)
        Renderer.camara.remove_obj(obj)
    
    def cargar_mapa_adyacente(self,ady):
        if type(self.limites[ady]) == str:
            nombre = self.limites[ady]
            data = r.abrir_json(MD.mapas+self.limites[ady]+'.json')
            
            w,h = self.mapa.rect.size
            if   ady == 'sup'   :  x,y =  0,-h
            elif ady == 'supizq':  x,y = -w,-h
            elif ady == 'supder':  x,y =  w,-h
            elif ady == 'inf'   :  x,y =  0, h
            elif ady == 'infizq':  x,y = -w, h
            elif ady == 'infder':  x,y =  w, h
            elif ady == 'izq'   :  x,y = -w, 0
            elif ady == 'der'   :  x,y =  w, 0
            
            mapa = ChunkMap(self,data,nombre,x,y)
           
            self.limites[ady] = mapa
            Renderer.camara.set_background(mapa)
            self.rect.union_ip(mapa.rect)
            return True
        return False
    
    def cargar_timestamps(self):
        if self.data['ambiente'] == 'exterior':
            self.amanece  = TimeStamp(*self.data["amanece"])
            self.atardece = TimeStamp(*self.data["atardece"])
            self.anochece = TimeStamp(*self.data["anochece"])
    
    def anochecer(self,event):
        '''
        :param event:
        :type event:GiftEvent
        :return:
        '''
        print(event)
        if self.data['ambiente'] == 'exterior':
            pass
        elif self.data['ambiente'] == 'interior':
            pass
    
    def actualizar_grilla(self):
        for spr in self.properties.get_sprites_from_layer(C.CAPA_GROUND_ITEMS):
            if spr.solido:# and not spr.es('empujable'):
                x = int(spr.mapX/32)
                y = int(spr.mapY/32)
                self.grilla[x,y].transitable = False
    
    def __repr__(self):
        return "Stage "+self.nombre+' ('+str(len(self.properties.sprites()))+' sprites)'

class ChunkMap(Sprite):
    #chunkmap: la idea es tener 9 de estos al mismo tiempo.
    tipo = 'mapa'
    offsetX = 0
    offsetY = 0
    def __init__(self,stage,data,nombre='',offX=0,offY=0):
        super().__init__()
        self.stage = stage
        self.nombre = nombre
        self.image = r.cargar_imagen(data['capa_background']['fondo'])
        self.rect = self.image.get_rect(topleft=(offX,offY))
        self.mask = mask.from_threshold(r.cargar_imagen(data['capa_background']['colisiones']), C.COLOR_COLISION, (1,1,1,255))
        self.offsetX = offX
        self.offsetY = offY
    
    def __repr__(self):
        return "ChunkMap "+self.nombre 
    
    def ubicar(self, x, y):
        '''Coloca al sprite en pantalla'''
        self.rect.x = x
        self.rect.y = y
    
    def update(self):
        #self.stage.anochecer()
        self.stage.actualizar_grilla()

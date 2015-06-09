from engine.globs import Constants as C, Tiempo as T, MobGroup, timestamp
from engine.globs import ModData as MD, EngineData as ED
from engine.mobs.scripts.a_star import generar_grilla
from pygame.sprite import Sprite, LayeredUpdates
from engine.misc import Resources as r
from .loader import _loader
from pygame import mask, Rect

class Stage:
    properties = None
    interactives = []
    chunks = None
    mapa = None
    data = {}
    quest = None
    
    def __init__(self,nombre,mobs_data,entrada):
        self.chunks = LayeredUpdates()
        self.nombre = nombre
        self.data = r.abrir_json(MD.mapas+nombre+'.json')
        self.chunks.add(ChunkMap(self,self.data,nombre=self.nombre))
        self.mapa  = self.chunks.sprites()[0]
        self.rect = self.mapa.rect.copy()
        self.grilla = generar_grilla(self.mapa.mask,self.mapa.image)
        self.properties = LayeredUpdates()
        self.salidas = [] #aunque en realidad, las salidas deberian ser del chunk, o no?
        self.cargar_timestamps()
        _loader.setStage(self)
        _loader.loadEverything(entrada,mobs_data)
        #self.register_at_renderer(entrada)
    
    def register_at_renderer(self,entrada):
        ED.RENDERER.setBackground(self.mapa)
        T.crear_noche(self.rect.size) #asumiendo que es uno solo...
        self.addProperty(T.noche,C.CAPA_TOP_CIELO)
        for obj in self.properties:
            obj.stage = self
            ED.RENDERER.addObj(obj,obj.rect.bottom)
        
        ED.HERO.ubicar(*self.data['entradas'][entrada])
    
    def addProperty(self,obj,_layer,addInteractive=False):
        if _layer == C.CAPA_GROUND_SALIDAS:
            self.salidas.append(obj)
        else:
            obj._layer_ = _layer
            if _layer == C.CAPA_TOP_CIELO:
                self.properties.remove_sprites_of_layer(C.CAPA_TOP_CIELO)
            self.properties.add(obj,layer =_layer)
            if addInteractive:
                self.interactives.append(obj)
    
    def delProperty(self,obj):
        if obj in self.properties:
            self.properties.remove(obj)
        if obj in self.interactives:
            self.interactives.remove(obj)
        ED.RENDERER.delObj(obj)
    
    def cargar_timestamps(self):
        if self.data['ambiente'] == 'exterior':
            self.amanece  = timestamp(*self.data["amanece"])
            self.atardece = timestamp(*self.data["atardece"])
            self.anochece = timestamp(*self.data["anochece"])
            self.esNoche = False
            self.esTarde = False
    
    def anochecer(self):
        ts = T.clock.timestamp()
        if self.data['ambiente'] == 'exterior':
            #transiciones
            if ts == self.amanece:
                T.aclarar()
                self.esNoche = False
                self.esTarde = False
            elif ts >= self.atardece and not self.esTarde:
                if T.oscurecer(100):
                    self.esTarde = True
            elif ts == self.anochece:
                if T.oscurecer(150):
                    self.esNoche = True
        elif self.data['ambiente'] == 'interior':
            T.noche.image.set_alpha(0)
    
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
    limites = {'sup':None,'supizq':None,'supder':None,
               'inf':None,'infizq':None,'infder':None,
               'izq':None,'der' : None}
    
    def __init__(self,stage,data,cuadrante='cen',nombre='',offX=0,offY=0):
        super().__init__()
        self.stage = stage
        self.nombre = nombre
        self.cuadrante = cuadrante
        self.cargar_limites(data['limites'])
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
    
    def cargar_limites(self,limites):
        for key in limites:
            self.limites[key.lower()] = limites[key]
                
    def checkear_adyacencias(self,claves):
        for clave in claves:
            if clave in self.limites:
                return self.cargar_mapa_adyacente(clave)
            
    def cargar_mapa_adyacente(self,ady):
        if type(self.limites[ady]) is str:
            nmbr = self.limites[ady]
            data = r.abrir_json(MD.mapas+self.limites[ady]+'.json')
            
            w,h = self.rect.size
            x,y = self.rect.topleft
            if   ady == 'sup'   :  dx,dy =  0,-h
            elif ady == 'supizq':  dx,dy = -w,-h
            elif ady == 'supder':  dx,dy =  w,-h
            elif ady == 'inf'   :  dx,dy =  0, h
            elif ady == 'infizq':  dx,dy = -w, h
            elif ady == 'infder':  dx,dy =  w, h
            elif ady == 'izq'   :  dx,dy = -w, 0
            elif ady == 'der'   :  dx,dy =  w, 0
            
            mapa = ChunkMap(self.stage,data,ady,nombre=nmbr,offX=dx,offY=dy)
           
            self.limites[ady] = mapa
            #self.stage.chunks.add(mapa)
            ED.RENDERER.setBackground(mapa)
            self.stage.rect.union_ip(mapa.rect)
            return True
        return False
    
    def update(self):
        self.stage.anochecer()
        self.stage.actualizar_grilla()
from engine.globs import EngineData as ED, Constants as C, MobGroup, ModData as MD
from engine.misc import Resources as r
from engine.mobs import NPCSocial, PC
from engine.quests import QuestManager
from engine.scenery import newProp
from .salida import Salida

class _loader:
    STAGE = None
    
    @classmethod
    def setStage(cls,stage):
        cls.STAGE = stage
    
    @classmethod
    def loadEverything(cls,entrada,mobs_data):
        cls.cargar_hero(entrada)
        cls.cargar_props()
        #cls.cargar_props('top')
        cls.cargar_mobs(mobs_data)
        cls.cargar_quests()
        cls.cargar_salidas()
        #cls.cargar_limites()
        
    @classmethod
    def cargar_props (cls,):
        imgs = cls.STAGE.data['refs']
        POS = cls.STAGE.data['capa_ground']['props']
        
        for ref in POS:
            try:
                data = r.abrir_json(MD.items+ref+'.item')
                imagen = r.cargar_imagen(data['image'])
            except IOError:
                data = False
                imagen = r.cargar_imagen(imgs[ref])
            
            
            for x,y in POS[ref]:
                if data:
                    prop = newProp(ref,imagen,x,y,data)
                    addInteractive = True
                else:
                    prop = newProp(ref,imagen,x,y)
                    addInteractive = False

                cls.STAGE.addProperty(prop,C.CAPA_GROUND_ITEMS,addInteractive)
    
    @classmethod
    def cargar_mobs(cls,extra_data,capa = 'capa_ground'):
        for key in cls.STAGE.data[capa]['mobs']:
            pos = cls.STAGE.data[capa]['mobs'][key]
            if key == 'npcs':
                clase = NPCSocial
    
            
                for ref in pos:
                    data = r.abrir_json(MD.mobs+ref+'.mob')
                    data.update(extra_data[ref])
                    for x,y in pos[ref]:
                        mob = clase(ref,x,y,data)
                        if capa == 'capa_ground':
                            cls.STAGE.addProperty(mob,C.CAPA_GROUND_MOBS)
                        elif capa == 'capa_top':
                            cls.STAGE.addProperty(mob,C.CAPA_TOP_MOBS)
    
    @classmethod
    def cargar_hero(cls,entrada):
        x,y = cls.STAGE.data['entradas'][entrada]
        try:
            pc = MobGroup['heroe']
            ED.HERO = pc
            ED.HERO.ubicar(x,y)
            ED.HERO.mapX = x
            ED.HERO.mapY = y
        except:
            ED.HERO = PC(r.abrir_json(MD.mobs+'hero.mob'),x,y)
        
        _loader.STAGE.addProperty(ED.HERO,C.CAPA_HERO)
    
    @classmethod
    def cargar_quests(cls,):
        if 'quests' in cls.STAGE.data:
            for quest in cls.STAGE.data['quests']:
                QuestManager.add(quest)
    
    @classmethod  
    def cargar_salidas(cls,):
        salidas = cls.STAGE.data['salidas']
        for salida in salidas:
            sld = Salida(salida,salidas[salida])
            _loader.STAGE.addProperty(sld,C.CAPA_GROUND_SALIDAS)

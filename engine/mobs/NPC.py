from engine.globs import ModData as MD
from engine.quests import QuestManager
from engine.misc import Resources as r
from .CompoMob import Sensitivo,Autonomo
from .mob import Mob

class NPC (Mob,Sensitivo,Autonomo):
    quest = None
    iniciativa = 2
    hablando = False
    def __init__(self,nombre,ruta_img,stage,x,y,data):
        self.nombre = nombre
        super().__init__(ruta_img,stage,x,y,data)
        self.establecer_AI(data,x,y)
        self.establecer_sentidos()
        
        self.generar_rasgos()
        self.data = data
    
        if 'quest' in data:
            QuestManager.add(data['quest'])

from engine.globs import ModData as MD
from engine.quests import QuestManager
from engine.misc import Resources as r
from .CompoMob import Autonomo
from .mob import Mob

class NPC (Autonomo,Mob): 
    quest = None
    iniciativa = 2
    hablando = False
    def __init__(self,nombre,x,y,data):
        self.nombre = nombre
        super().__init__(data,x,y)
    
        if 'quest' in data:
            QuestManager.add(data['quest'])

from misc import Resources as r
from globs import Constants as C, World as W, MobGroup

class Quest:
    objetivos = {}
    on_Dialogs = {}
    off_Dialogs = {}
    
    def __init__(self, script):
        self.objetivos = {}
        self.on_Dialogs = {}
        self.off_Dialogs = {}
        # si no lo redefino, pasan cosas raras.
        
        data = r.abrir_json('data/quests/'+script+'.quest')
        self.nombre = script
        for tipo in data['objetivos']:
            self.objetivos[tipo] = data['objetivos'][tipo]
        for mob in data['NPCs']:
            self.on_Dialogs[mob] = data['NPCs'][mob]['on']
            self.off_Dialogs[mob] = data['NPCs'][mob]['off']
    
    def update(self):
        for objetivo in self.objetivos:
            if objetivo == 'kill':
                for mob in self.objetivos[objetivo]:
                    if mob in MobGroup:
                        return False
                self.resolver()
                return True
            
            elif objetivo == 'talk':
                for mob in self.objetivos[objetivo]:
                    if W.HERO.interlocutor!= None:
                        if W.HERO.interlocutor.nombre == mob:
                            if W.HERO.interlocutor.pos_diag == -1:
                                self.resolver()
                                return True
                return False
            
            elif objetivo == 'get':
                for objeto in self.objetivos[objetivo]:
                    if objeto in W.HERO.inventario:
                        self.resolver()
                        return True
                return False
    
    def resolver(self):
        print (self.nombre, "victoria")

    def __repr__(self):
        return 'Quest '+self.nombre+'Object'
    
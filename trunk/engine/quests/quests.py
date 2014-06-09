from engine.misc import Resources as r
from engine.globs import EngineData as ED, MobGroup

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
            if data['NPCs'][mob]['on'] != '':
                self.on_Dialogs[mob] = r.abrir_json('data/dialogs/'+data['NPCs'][mob]['on'])
            else:
                self.on_Dialogs[mob] = ""
            
            if data['NPCs'][mob]['off'] != '':
                self.off_Dialogs[mob] = r.abrir_json('data/dialogs/'+data['NPCs'][mob]['off'])
            else:
                self.off_Dialogs[mob] = ""
    
    def update(self):
        for objetivo in self.objetivos:
            if objetivo == 'kill':
                for mob in self.objetivos[objetivo]:
                    if mob in MobGroup:
                        return False
                self.resolver()
                return True
            
            elif objetivo == 'talk':
                if self.nombre in ED.HERO.conversaciones:
                    self.resolver()
                    return True
                else:
                    return False
            
            elif objetivo == 'get':
                for objeto in self.objetivos[objetivo]:
                    if objeto in ED.HERO.inventario:
                        self.resolver()
                        return True
                return False
    
    def resolver(self):
        print (self.nombre, "victoria")

    def __repr__(self):
        return 'Quest '+self.nombre+' Object'
    
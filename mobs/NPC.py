from . import Mob
from globs import World as W, QuestManager, MobGroup

class NPC (Mob):
    quest = None
    def __init__(self,nombre,ruta_img,stage,x,y,data):
        super().__init__(ruta_img,stage,x,y,data)
        self.data = data
        self.nombre = nombre
        self.dialogos = self.data['dialogo']
        self.pos_diag = -1
        MobGroup.add(self)
        if 'quest' in data:
            QuestManager.add(data['quest'])
        self.generar_rasgos()
    
    def hablar(self, onSelect):
        if len(self.dialogos) == 0:
            self.stage.endDialog()
            return False
        
        elif not onSelect:
            self.pos_diag += 1
        
        if self.pos_diag >= len(self.dialogos):
            self.stage.endDialog()
            self.pos_diag = -1
            return False
        
        else:
            if type(self.dialogos[self.pos_diag]) != dict:
                texto = self.dialogos[self.pos_diag]
                onSelect = False
            
            else:
                if not onSelect:
                    texto = '\n'.join(self.dialogos[self.pos_diag])
                    onSelect = True
                    
                else:
                    sel = list(self.dialogos[self.pos_diag].keys())[onSelect-1]
                    texto = self.dialogos[self.pos_diag][sel]
                    onSelect = False
                
            self.stage.setDialog(texto,onSelect)
            return onSelect
    
    def devolver_seleccion(self,sel):
        op = list(self.dialogos[self.pos_diag].keys())[W.DIALOG.sel-1]
        
        return self.dialogos[self.pos_diag][op]
        
    def mover(self):
        if self.pos_diag == -1:
            super().mover()

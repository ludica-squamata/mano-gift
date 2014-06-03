class Equipado:
    equipo = {'yelmo':None,'aro 1':None,'aro 2':None,'cuello':None,'peto':None,
          'guardabrazos':None,'brazales':None,'faldar':None,'quijotes':None,
          'grebas':None,'mano buena':None,'mano mala':None,'botas':None,'capa':None,
          'cinto':None,'guantes':None,'anillo 1':None,'anillo 2':None}
    inventario = None

    def equipar_item(self,item):
        self.equipo[item.esEquipable] = item
        self.inventario.quitar(item.ID)
        
    def desequipar_item(self,item):
        self.equipo[item.esEquipable] = None
        self.inventario.agregar(item)
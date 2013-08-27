from misc import Resources as r

class Item:
    '''Para cosas que van en el inventario'''
    
    nombre = ''#el nombre para mostrar del ítem en cuestión
    prop_id = None
    esStackable = False
    cantidad = 1
    def __init__(self,nombre,esStackable):
        self.nombre = nombre
        data = r.abrir_json('scripts/items.json')[nombre]
        self.ID = data['ID']
        self.volumen = data['volumen']
        self.peso = data['peso']
        if 'efecto' in data:
            if 'des' in data['efecto']:
                self.efecto_des = data['efecto']['des']
        self.esStackable = esStackable
    
    def __repr__(self):
        return self.nombre+' Mob.Item'
    
    #def __eq__(self,other):
    #    if self.ID == other.ID:
    #        return True
    #    else:
    #        return False
    
    
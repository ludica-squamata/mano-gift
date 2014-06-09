from engine.misc import Resources as r
from engine.globs import ModData as MD

class Item:
    '''Para cosas que van en el inventario'''
    
    nombre = ''#el nombre para mostrar del ítem en cuestión
    prop_id = None
    esStackable = False
    esEquipable = False
    cantidad = 1
    def __init__(self,nombre,esStackable,imagen):
        self.nombre = nombre
        self.image = imagen
        data = r.abrir_json(MD.scripts+'items.json')[nombre]
        self.ID = data['ID']
        self.volumen = data['volumen']
        self.peso = data['peso']
        if 'efecto' in data:
            if 'des' in data['efecto']:
                self.efecto_des = data['efecto']['des']
            if 'equipo' in data['efecto']:
                self.esEquipable = data['efecto']['equipo']
        self.esStackable = esStackable
    
    def __repr__(self):
        return self.nombre+' Mob.Item'
    
    def __eq__(self,other):
        if other.__class__!= self.__class__:
            return False
        elif self.ID == other.ID:
            return True
        else:
            return False
    
    
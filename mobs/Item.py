class Item:
    '''Para cosas que van en el inventario'''
    
    data = ''
    nombre = ''#el nombre para mostrar del ítem en cuestión
    def __init__(self,nombre):
        self.nombre = nombre
    
    def __str__(self):
        return self.nombre.capitalize()
    
    def __eq__(self,other):
        if type(self) == type(other):
            return True

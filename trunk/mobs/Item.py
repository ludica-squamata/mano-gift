class Item:
    '''Para cosas que van en el inventario'''
    
    data = ''
    nombre = ''#el nombre para mostrar del ítem en cuestión
    def __init__(self,nombre):
        self.nombre = nombre
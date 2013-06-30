
class Inventory:
    contenido = {}
    # la mochila
    def __init__ (self):
        self.contenido = []

    def ver (self):
        if len(self.contenido) < 1:
            texto = 'El inventario está vacío'
        else:
            toJoin = []
            existe = []
            for item in self.contenido:
                Item = str(item)
                if Item not in existe:
                    existe.append(Item)
                    toJoin.append(Item+' x'+str(self.contenido.count(item)))
            
            #toJoin = [str(item) for item in self.contenido]
            texto = ', '.join(toJoin)
        
        return texto

    def agregar(self,cosa):
        from . import Item
        self.contenido.append(Item(cosa))

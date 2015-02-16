class Item:
    stackable = False
    slot = '-'
    def __init__(self,nombre,imagen,data):
        self.nombre = nombre
        self.image = imagen
        self.ID = data['ID']
        self.peso = data['peso']
        self.volumen = data['volumen']
        self.efecto_des = data['efecto']['des']
        if 'stackable' in data['propiedades']:
            self.stackable = True
    
    def __eq__(self,other):
        if other.__class__== self.__class__ and self.ID == other.ID:
            return True
        else:
            return False
        
    def __ne__(self,other):
        if other.__class__!= self.__class__:
            return True
        elif self.ID != other.ID:
            return True
        else:
            return False
    
class Equipable(Item):
    def __init__(self,nombre,imagen,data):
        super().__init__(nombre,imagen,data)
        self.tipo = 'equipable'
        self.espacio = data['efecto']['equipo']

class Consumible(Item):
    def __init__(self,nombre,imagen,data):
        super().__init__(nombre,imagen,data)
        self.tipo = 'consumible'
        self.data = data
    
    def usar(self,mob):
        stat = self.data['efecto']['stat']
        mod = self.data['efecto']['mod']
        if stat == 'salud':
            actual = stat+'_act'
            maximo = stat+'_max'
            ValActual = getattr(mob,actual)
            ValMaximo = getattr(mob,maximo)
            
            valor = int((mod*ValMaximo)/100)
            if valor + ValActual > ValMaximo:
                valor = ValMaximo
            else:
                valor += ValActual
            
            setattr(mob,actual,valor)

class Armadura(Equipable):
    def __init__(self,nombre,imagen,data):
        super().__init__(nombre,imagen,data)
        self.subtipo = 'armadura'

class Arma (Equipable):
    def __init__(self,nombre,imagen,data):
        super().__init__(nombre,imagen,data)
        self.subtipo = 'arma'

class Accesorio (Equipable):
    def __init__(self,nombre,imagen,data):
        super().__init__(nombre,imagen,data)
        self.subtipo = 'accesorio'

class Pocion (Consumible):
    def __init__(self,nombre,imagen,data):
        super().__init__(nombre,imagen,data)
        self.subtipo = 'pocion'
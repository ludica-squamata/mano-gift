from .prop import Prop

class Agarrable(Prop):
    def __init__(self,nombre,imagen,x,y,data):
        super().__init__(nombre,imagen,x,y)

class Movible(Prop):
    def __init__(self,nombre,imagen,x,y,data):
        super().__init__(nombre,imagen,x,y)

class Trepable(Prop):
    def __init__(self,nombre,imagen,x,y,data):
        super().__init__(nombre,imagen,x,y)

class Operable(Prop):
    def __init__(self,nombre,imagen,x,y,data):
        super().__init__(nombre,imagen,x,y)

class Destruible(Prop):
    def __init__(self,nombre,imagen,x,y,data):
        super().__init__(nombre,imagen,x,y)
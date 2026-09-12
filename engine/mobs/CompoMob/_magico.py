from ._caracterizado import Caracterizado

class Magico(Caracterizado):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.afinidades = {}
        for i, color in enumerate('azul,rojo,verde,amarillo,cian,magenta'.split(',')):
            self.afinidades[color] = Afinidad(self,color)

class Afinidad:
    def __init__(self, parent, color):
        self.parent = parent
        self.name = color
        self.value = 0

    def incrementar(self):
        self.value += 1 if self.value + 1 <= 10 else 10
        self.parent[self.name] = self.value

    def decrementar(self):
        self.value -= 1 if self.value - 1 >= 0 else 0
        self.parent[self.name] = self.value

    def incrementar_por(self, valor):
        self.value += valor if self.value + valor <= 10 else 10
        self.parent[self.name] = self.value

    def decrementar_por(self, valor):
        self.value -= valor if self.value - valor >= 0 else 0
        self.parent[self.name] = self.value
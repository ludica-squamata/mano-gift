from ._caracterizado import Caracterizado
from engine.libs import randint


class Suertudo(Caracterizado):

    @staticmethod
    def luck():
        return randint(1, 100)

    @staticmethod
    def chance(x, k):
        x = max(0, x)
        k = max(0, k)
        if x + k == 0:
            return 0.5  # neutral absoluto
        return x / (x + k)
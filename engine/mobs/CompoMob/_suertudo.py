from ._caracterizado import Caracterizado
from engine.libs import randint


class Suertudo(Caracterizado):

    @staticmethod
    def luck():
        return randint(1, 100)

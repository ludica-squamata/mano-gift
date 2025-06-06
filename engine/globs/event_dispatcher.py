﻿from collections import deque
from datetime import datetime
from random import randint


class EventDispatcher:
    """
    manejador de eventos
    """
    _oyentes = {}  # {evento1:[funciones],evento2:[funciones]}
    _cola = deque()

    @classmethod
    def register(cls, listener, *events):
        """
        Este método es llamado por los objetos que desean recibir un evento particular
        :param listener:es la referencia a una funcion. la misma debe aceptar como parametro un
                        objeto de tipo AzoeEvent.
        :param events:lista de string con los eventos que desean registrarse.
        :return:None
        """
        for event in events:
            if event not in cls._oyentes:
                cls._oyentes[event] = [listener]
            elif listener not in cls._oyentes[event]:
                cls._oyentes[event].append(listener)

    @classmethod
    def register_many(cls, *pairs):
        for pair in pairs:
            listener = pair[0]
            events = pair[1:]
            cls.register(listener, *events)

    @classmethod
    def deregister(cls, listener, *events):
        """
        Se llama para removerse de la cola de notificaciones (por ejemplo, al morir un mob).
        la funcion pasada debe ser la misma que se usó para registrarse
        :param listener:la funcion que desea borrarse
        :param events:lista de string con los eventos que desean borrarse
        :type listener:(AzoeEvent)->None
        :return:None
        """
        for event in events:
            if event in cls._oyentes:
                if listener in cls._oyentes[event]:
                    cls._oyentes[event].remove(listener)
                if not len(cls._oyentes[event]):
                    del cls._oyentes[event]

    @classmethod
    def trigger(cls, *event_data):
        """
        Este método crea un evento en la cola para ser distribuido, con los datos que
        van a ser distribuidos.
        :param event_data:
        :type event_data:list/AzoeEvent
        :return:None
        """

        if event_data[0] in cls._oyentes:
            event = AzoeEvent(*event_data)
            cls._cola.append(event)

    @classmethod
    def process(cls):
        """
        El método llamado antes del update del renderer para hacer dispatching
        del frame. Para performance solo dispara los eventos generados en este frame.
        Subsiguientes eventos se processan en subsiguientes frames.
        :return:None
        """
        _cola = cls._cola.copy()
        while len(_cola) > 0:
            evento = _cola.popleft()
            cls._cola.remove(evento)
            if evento in cls._oyentes:
                for listener in cls._oyentes[evento]:
                    listener()
            if evento.tipo in cls._oyentes:
                for listener in cls._oyentes[evento.tipo]:
                    listener(evento)

    @classmethod
    def get_queqed(cls):
        print('quequed events:', len(cls._cola))
        for item in cls._cola:
            print('+ ', item)
        print('end queque')

    @classmethod
    def is_quequed(cls, event_name):
        for event in cls._cola:
            if event.tipo == event_name:
                return True
        return False

    @classmethod
    def get_registered(cls):
        for name in sorted(cls._oyentes):
            print(name + ',', 'oyentes:', len(cls._oyentes[name]))


class AzoeEvent:
    """
    representacion de un evento ejecutado por un objeto de juego
    """
    tipo = ''  # type un string con el nombre del evento
    origin = ''  # origin un string identificando el objeto que creó el evento
    data = {}  # data un dict con la información relevante

    def __init__(self, tipo, origin, data):
        """
        :param tipo:
        :param origin:
        :param data:
        :type tipo:str
        :type origin:str
        :type data:dict
        :return:None
        """
        self.tipo = tipo
        self.origin = origin
        self.data = data

        r = randint(0, 99999)
        now = ''.join([char for char in str(datetime.now()) if char not in [' ', '.', ':', '-']])
        self.id = now[0:-5] + '-' + str(r).rjust(5, '0')

    def __repr__(self):
        return 'AzoeEvent-' + str(self.tipo) + '(origin: ' + str(self.origin) + ', data: ' + str(self.data) + ')'

    def __eq__(self, other):
        return self.__repr__() == other.__repr__()

    def __hash__(self):
        return hash((self.tipo, self.origin))


if __name__ == '__main__':
    myEvent1 = AzoeEvent('prueba', 'yo', {})
    myEvent2 = AzoeEvent('BossMuerto', 'yo', {})
    myEvent3 = AzoeEvent('BotonPresionado', 'yo', {})
    EventDispatcher.register(lambda event: print(event, 'respuesta A'), 'prueba')
    EventDispatcher.register(lambda event: print(event, 'respuesta B'), 'prueba', 'BossMuerto')
    EventDispatcher.register(lambda event: print(event, 'respuesta C'), 'BotonPresionado')
    EventDispatcher.deregister(lambda event: print(event, 'respuesta B'), 'prueba')
    EventDispatcher.register(lambda event: print(event, 'respuesta B'), 'BotonPresionado', 'BossMuerto')
    EventDispatcher.trigger(myEvent1)
    EventDispatcher.process()

from collections import deque


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
                        objeto de tipo giftEvent.
        :param events:lista de string con los eventos que desean registrarse.
        :type listener:(GiftEvent)->None
        :type events:tuple
        :return:None
        """
        for event in events:
            if event not in cls._oyentes:
                cls._oyentes[event] = [listener]
            elif listener not in cls._oyentes[event]:
                cls._oyentes[event].append(listener)

    @classmethod
    def deregister(cls, listener, *events):
        """
        Se llama para removerse de la cola de notificaciones (por ejemplo, al morir un mob).
        la funcion pasada debe ser la misma que se usó para registrarse
        :param listener:la funcion que desea borrarse
        :param events:lista de string con los eventos que desean borrarse
        :type listener:(GiftEvent)->None
        :type events:tuple
        :return:None
        """
        for event in events:
            if event in cls._oyentes:
                if listener in cls._oyentes[event]:
                    cls._oyentes[event].remove(listener)
                if not len(cls._oyentes[event]):
                    del cls._oyentes[event]

    @classmethod
    def trigger(cls, event_data):
        """
        Este método crea un evento en la cola para ser distribuido, con los datos que
        van a ser distribuidos.
        :param event_data:
        :type event_data:dict/GiftEvent
        :return:None
        """
        if not type(event_data) is GiftEvent: #else: suponemos list
            event = GiftEvent(*event_data)
        cls._cola.append(event)

    @classmethod
    def process(cls):
        """
        El método llamado antes del update del renderer para hacer dispatching
        del frame. Para performande puede estar limitado a ejecutar una cantidad de
        dispatchs por frame, usando yield o algo asi
        :return:None
        """
        _cola = cls._cola
        l = len(_cola)
        while l > 0:
            evento = _cola.popleft()
            print(evento)
            if evento.type in cls._oyentes:
                for listener in cls._oyentes[evento.type]:
                    listener(evento)
            l -= 1


class GiftEvent:
    """
    representacion de un evento ejecutado por un objeto de juego
    """
    type = ''  # type un string con el nombre del evento
    origin = ''  # origin un string identificando el objeto que creó el evento
    data = {}  # data un dict con la información relevante

    def __init__(self, type, origin, data):
        """
        :param type:
        :param origin:
        :param data:
        :type type:str
        :type origin:str
        :type data:dict
        :return:None
        """
        self.type = type
        self.origin = origin
        self.data = data

    def __repr__(self):
        return 'giftEvent-' + self.type + '(origin: ' + self.origin + ', data: ' + str(self.data) + ')'


if __name__ == '__main__':
    myEvent1 = GiftEvent('prueba', 'yo', {})
    myEvent2 = GiftEvent('BossMuerto', 'yo', {})
    myEvent3 = GiftEvent('BotonPresionado', 'yo', {})
    f1 = lambda event: print(event, 'respuesta A')
    f2 = lambda event: print(event, 'respuesta B')
    f3 = lambda event: print(event, 'respuesta C')
    EventDispatcher.register(f1, 'prueba')
    EventDispatcher.register(f2, 'prueba', 'BossMuerto')
    EventDispatcher.register(f3, 'BotonPresionado')
    EventDispatcher.deregister(f2, 'prueba')
    EventDispatcher.register(f2, 'BotonPresionado', 'BossMuerto')
    EventDispatcher.trigger(myEvent1)
    EventDispatcher.process()

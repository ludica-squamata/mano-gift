class EventDispatcher:
    _oyentes = {} #{evento1:[funciones],evento2:[funciones]}
    _cola = [] #podria ser también un objeto collections.deque, se me ocurre.
    
    @staticmethod
    def register(listener,*events):
        '''events es un string o un list con strings de los eventos que desean registrarse. 
        listener es la referencia a una funcion. la misma debe aceptar como parametro un
        objeto de tipo giftEvent.
        Este método es llamado por los objetos que desean recibir un evento particular'''
        for event in events:
            if event not in EventDispatcher._oyentes:
                EventDispatcher._oyentes[event] = [listener]
            elif listener not in EventDispatcher._oyentes[event]:
                EventDispatcher._oyentes[event].append(listener)
                
    @staticmethod
    def deregister(listener,*events):
        '''events es un string o un list con strings de los eventos que desean borrarse. 
        listener es la referencia a una funcion. Se llama para removerse de la cola de
        notificaciones (por ejemplo, al morir un mob). la funcion pasada debe ser la misma
        que se usó para registrarse'''
        for event in events:
            if event in EventDispatcher._oyentes:
                if listener in EventDispatcher._oyentes[event]:
                    EventDispatcher._oyentes[event].remove(listener)
                if not len(EventDispatcher._oyentes[event]): 
                    del EventDispatcher._oyentes[event]
        
    @staticmethod
    def trigger(eventData):
        '''eventData es un objeto de tipo giftEvent. 
        Este método crea un evento en la cola para ser distribuido, con los datos que
        van a ser distribuidos.'''
        EventDispatcher._cola.append(eventData)
    
    @staticmethod
    def process():
        '''El método llamado antes del update del renderer para hacer dispatching
        del frame. Para performande puede estar limitado a ejecutar una cantidad de
        dispatchs por frame, usando yield o algo asi'''
        
        for evento in EventDispatcher._cola:
            if evento.type in EventDispatcher._oyentes:
                for listener in EventDispatcher._oyentes[evento.type]:
                    listener(evento)
        EventDispatcher._cola.clear()
        
class giftEvent:
    '''  data un dict con la información relevante'''
    type = '' #type un string con el nombre del evento
    origin = '' #origin un string identificando el objeto que creó el evento
    data = {} #data un dict con la información relevante
    def __init__(self,type,origin,data):
        self.type = type
        self.origin = origin
        self.data = data
    def __repr__(self):
        return 'giftEvent-'+self.type+'(origin: '+self.origin+', data: '+str(self.data)+')'

if __name__ == '__main__':
    myEvent1 = giftEvent('prueba','yo',{})
    myEvent2 = giftEvent('BossMuerto','yo',{})
    myEvent3 = giftEvent('BotonPresionado','yo',{})
    f1 = lambda event: print(event,'respuesta A')
    f2 = lambda event: print(event,'respuesta B')
    f3 = lambda event: print(event,'respuesta C')
    EventDispatcher.register(f1,'prueba')
    EventDispatcher.register(f2,'prueba','BossMuerto')
    EventDispatcher.register(f3,'BotonPresionado')
    EventDispatcher.deregister(f2,'prueba')
    EventDispatcher.register(f2,'BotonPresionado','BossMuerto')
    EventDispatcher.trigger(myEvent1)
    EventDispatcher.process()

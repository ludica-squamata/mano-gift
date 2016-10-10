from .eventDispatcher import EventDispatcher


class EventAware:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register()

    def listener(self, event):
        try:
            self.use_function(event.data['type'], event.data['nom'])
        except KeyError:
            pass

    def register(self):
        EventDispatcher.register(self.listener, 'key')

    def deregister(self):
        EventDispatcher.deregister(self.listener, 'key')

    def use_function(self, mode, key):
        pass

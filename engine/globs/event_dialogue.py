from .eventDispatcher import EventDispatcher


class EventDialogue:
    def __init__(self, *args, **kwargs):
        EventDispatcher.register(self.listener, 'key')
        super().__init__(*args, **kwargs)

    def listener(self, event):
        try:
            self.use_function(event.data['type'], event.data['nom'])
        except KeyError:
            pass

    def deregister(self):
        EventDispatcher.deregister(self.listener, 'key')

    def use_function(self, mode, key):
        pass

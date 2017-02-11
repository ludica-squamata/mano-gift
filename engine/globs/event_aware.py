from .eventDispatcher import EventDispatcher


class EventAware:
    registered = False
    functions = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register()

    def listener(self, event):
        try:
            self.use_function(event.data['type'], event.data['nom'])
        except KeyError:
            self.new_key_event(event)

    def new_key_event(self, event):
        pass

    def register(self):
        EventDispatcher.register(self.listener, 'key')
        self.registered = True

    def deregister(self):
        EventDispatcher.deregister(self.listener, 'key')
        self.registered = False

    def use_function(self, mode, key):
        if key in self.functions[mode]:
            self.functions[mode][key]()

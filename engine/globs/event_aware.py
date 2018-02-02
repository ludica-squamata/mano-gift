from .eventDispatcher import EventDispatcher


class EventAware:
    registered = False
    functions = None

    def __init__(self, *args, **kwargs):
        self.functions = {
            'tap': {},
            'hold': {},
            'release': {}
        }
        super().__init__(*args, **kwargs)
        self.register()

    def listener(self, event):
        self.use_function(event.data.get('type', ''), event.data.get('nom', ''))

    def register(self):
        EventDispatcher.register(self.listener, 'Key')
        self.registered = True

    def deregister(self):
        EventDispatcher.deregister(self.listener, 'Key')
        self.registered = False

    def use_function(self, mode, key):
        if mode in self.functions:
            if key in self.functions[mode]:
                self.functions[mode][key]()

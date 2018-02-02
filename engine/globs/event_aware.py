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
        try:
            self.use_function(event.data['type'], event.data['nom'])
        except KeyError:
            print('evitado un crash por un momento de lag')

    def register(self):
        EventDispatcher.register(self.listener, 'Key')
        self.registered = True

    def deregister(self):
        EventDispatcher.deregister(self.listener, 'Key')
        self.registered = False

    def use_function(self, mode, key):
        if key in self.functions[mode]:
            self.functions[mode][key]()

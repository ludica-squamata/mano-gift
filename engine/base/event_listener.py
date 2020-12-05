from engine.globs.event_dispatcher import EventDispatcher
from engine.misc.resources import load_module_from_script
from engine.globs import ModData
import types


class EventListener:
    event_handlers = {}
    data = None

    def add_listeners(self):
        """
        carga los listeners definido en el
        :return:None
        """
        if self.data.get('script') and self.data.get('eventos'):
            # cargar un archivo por ruta
            ruta = ModData.fd_scripts+'events/'+self.data['script']
            m = load_module_from_script(self.data['script'][:-3], ruta)

            for event_name, func_name in self.data['eventos'].items():
                if hasattr(m, func_name):
                    # esto le asigna la instancia actual como self a la función,
                    # así puede acceder a propiedades del sprite
                    method = types.MethodType(getattr(m, func_name), self)
                    self.event_handlers[event_name] = method
                    EventDispatcher.register(method, event_name)

    def remove_listeners(self):
        """
        quitar listeners, como parte de la limpieza de un sprite
        :return:None
        """
        if self.event_handlers:
            for event_name, f in self.event_handlers:
                EventDispatcher.deregister(f, event_name)

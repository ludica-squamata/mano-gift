from engine.globs.eventDispatcher import EventDispatcher
from engine.globs import ModData as MD
from importlib import machinery
import types, sys

class EventListener:

    event_handlers = {}

    def add_listeners(self):
        """
        carga los listeners definido en el
        :return:None
        """
        if self.data.get('script') and self.data.get('eventos'):
            # cargar un archivo por ruta
            loader = machinery.SourceFileLoader("module.name", MD.scripts+self.data['script']+'.py')
            if sys.version_info.minor == 3:
                m = loader.load_module()
            elif sys.version_info.minor == 4:
                # en 3.4 lo cambiaron a exec_module()
                m = loader.exec_module()
            
            for event_name, func_name in self.data['eventos'].items():
                f = getattr(m, func_name)
                if f:
                    # esto le asigna la instancia actual como self a la funcion,
                    # asi puede acceder a propiedades del sprite
                    f = types.MethodType(f, self)
                    self.event_handlers[event_name] = f
                    EventDispatcher.register(f, event_name)

    def remove_listeners(self):
        """
        quitar listeners, como parte de la limpieza de un sprite
        :return:None
        """
        if self.event_handlers:
            for event_name, f in self.event_handlers:
                EventDispatcher.deregister(f, event_name)
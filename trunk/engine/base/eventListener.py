from engine.base import _giftSprite
from engine.globs.engine_data import EngineData as ED


class EventListener(_giftSprite):

    event_handlers = {}

    def add_listeners(self):
        """
        carga los listeners definido en el
        :return:None
        """
        if self.data.get('script') and self.data.get('eventos'):
            from engine.globs.mod_data import ModData as MD
            from importlib import machinery
            import types

            # cargar un archivo por ruta
            loader = machinery.SourceFileLoader("module.name", MD.scripts+self.data['script']+'.py')
            m = loader.load_module()  # en 3.4 lo cambiaron a exec_module()
            for event_name, func_name in self.data['eventos'].items():
                f = getattr(m, func_name)
                if f:
                    # esto le asigna la instancia actual como self a la funcion,
                    # asi puede acceder a propiedades del sprite
                    f = types.MethodType(f, self)
                    self.event_handlers[event_name] = f
                    ED.EVENTS.register(f, event_name)

    def remove_listeners(self):
        """
        quitar listeners, como parte de la limpieza de un sprite
        :return:None
        """
        if self.event_handlers:
            for event_name, f in self.event_handlers:
                ED.EVENTS.deregister(f, event_name)
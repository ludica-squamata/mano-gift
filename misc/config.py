from .resources import Resources as r

class Config:
    # configuraciones
    data = None # {}
    __changed = False
    
    __defaults = {
        "mostrar_intro":True,
        "recordar_menus":True, 
        "resolucion":{
            "ANCHO":480,
            "ALTO":480
        },
        
        "teclas":{
            "arriba":273,
            "abajo":274,
            "derecha":275,
            "izquierda":276,
            
            "accion":120,
            "hablar":115,
            "cancelar":97,
            "inventario":122,
            "posicion":304,
            
            "menu":13,
            "debug":282,
            "salir":27
        }
    }
    
    def cargar():
        if Config.data is None:
            import os
            if os.path.isfile('config.json'):
                Config.data = r.abrir_json('config.json')
            else:
                Config.data = Config.defaults()
                Config.__changed = True
                Config.guardar()
        return Config.data

    def defaults(clave = None):
        dato = Config.__defaults
        if clave is not None:
            if not isinstance(clave, list):
                clave = clave.split('/')
            for x in clave:
                if x in dato:
                    dato = dato[x]
                else:
                    dato = None
        return dato
        
    def dato(clave = None):
        dato = Config.cargar()
        if clave is not None:
            if not isinstance(clave, list):
                clave = clave.split('/')
            for x in clave:
                if x in dato:
                    dato = dato[x]
                else:
                    dato = Config.defaults(clave)
                    break
        return dato
    
    def asignar(clave, valor):
        dato = Config.cargar()
        if not isinstance(clave, list):
                clave = clave.split('/')
        last = clave.pop()
        if len(clave) > 0:
            for x in clave:
                if x in dato:
                    dato = dato[x]
                else:
                    dato[x] = {}
                    dato = dato[x]
        dato[last] = valor
        Config.__changed = True
    
    def guardar():
        if Config.__changed:
            r.guardar_json('config.json',Config.data)
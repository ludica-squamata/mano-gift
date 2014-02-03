from .resources import Resources
class Config:
    # configuraciones
    recordar = False
    intro = True
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
                Config.data = Resources.abrir_json('config.json')
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
        # quiero sacar esto de acá.. pero no sé como evitar la referencia circular
        # from globs.constantes import constants as c
        # from globs.teclas import teclas as t
        # data = {
            # "mostrar_intro":true,"recordar_menus":true, #próximamente cofigurables
            # "resolucion":{"cuadro":c.cuadro,"ancho":c.ancho,"alto":c.alto},
            # "teclas":{"arriba":t.arriba,"abajo":t.abajo,
                      # "derecha":t.derecha,"izquierda":t.izquierda,
                      # "accion":t.accion,"hablar":t.hablar,
                      # "cancelar":t.cancelar_dialogo,"inventario":t.inventario,
                      # "posicion":t.cambiar_posicion,
                      # "menu":t.menu,"debug":t.debug,"salir":t.salir}}
        if Config.__changed:
            Resources.guardar_json('config.json',Config.data)
    
    # def asignar(self,data):
        # # quiero sacar esto de acá.. pero no sé como evitar la referencia circular
        # from globs.constantes import Constants as C
        # from globs.teclas import Teclas as T
        # Config.recordar = data['recordar_menus']
        # Config.intro = data['mostrar_intro']
        # C.CUADRO = data['resolucion']['CUADRO']
        # C.ANCHO = data['resolucion']['ANCHO']
        # C.ALTO = data['resolucion']['ALTO']
        # T.asignar(data['teclas'])
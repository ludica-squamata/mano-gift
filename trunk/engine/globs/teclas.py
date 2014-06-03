
class Teclas:
    ARRIBA, ABAJO, IZQUIERDA, DERECHA = 0,0,0,0
    ACCION, HABLAR,CANCELAR_DIALOGO = 0,0,0
    INVENTARIO, POSICION_COMBATE = 0,0
    MENU, SALIR, DEBUG = 0,0,0
    
    def __init__(self,data):
        '''No es que vaya a haber más de uno,
        pero mirá lo que hacemos en constantes...'''
        
        self.asignar(data)
        # podría ser __init__ en lugar de asignar,
        # pero lo dejo así por las dudas.

    def asignar (self,data):
        '''Usamos este metodo para cargar desde config.json'''
        
        self.ARRIBA = data['arriba']
        self.ABAJO = data['abajo']
        self.IZQUIERDA = data['izquierda']
        self.DERECHA = data['derecha']

        self.ACCION = data['accion']
        self.HABLAR = data['hablar']
        self.CANCELAR_DIALOGO = data['cancelar']
        self.INVENTARIO = data['inventario']
        self.POSICION_COMBATE = data['posicion']
        
        self.MENU = data['menu']
        self.SALIR = data['salir']
        self.DEBUG = data['debug']
from pygame import K_UP, K_DOWN, K_LEFT, K_RIGHT, \
K_x, K_s, K_a, K_z, K_RETURN, K_ESCAPE, K_LSHIFT, K_F1

class Teclas:
    ARRIBA = K_UP
    ABAJO = K_DOWN
    IZQUIERDA= K_LEFT
    DERECHA = K_RIGHT

    ACCION = K_x
    HABLAR = K_s
    CANCELAR_DIALOGO = K_a
    INVENTARIO = K_z
    MENU = K_RETURN
    SALIR = K_ESCAPE
    POSICION_COMBATE = K_LSHIFT
    DEBUG = K_F1


    def asignar (self,data): #porque no estamos usando este metodo para cargar desde un config?
        Teclas.ARRIBA = data['arriba']
        Teclas.ABAJO = data['abajo']
        Teclas.IZQUIERDA = data['izquierda']
        Teclas.DERECHA = data['derecha']

        Teclas.ACCION = data['accion']
        Teclas.INVENTARIO = data['inventario']
        Teclas.MENU = data['menu']
        Teclas.SALIR = data['salir']
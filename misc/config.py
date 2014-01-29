class Config:
    # configuraciones
    recordar = False
    intro = True
    
    def cargar():
        data = Resources.abrir_json('config.json')
        Config.asignar(data)
        
    def guardar():
        # quiero sacar esto de acá.. pero no sé como evitar la referencia circular
        from globs.constantes import Constants as C
        from globs.teclas import Teclas as T
        data = {
            "mostrar_intro":True,"recordar_menus":True, #próximamente cofigurables
            "resolucion":{"CUADRO":C.CUADRO,"ANCHO":C.ANCHO,"ALTO":C.ALTO},
            "teclas":{"arriba":T.ARRIBA,"abajo":T.ABAJO,
                      "derecha":T.DERECHA,"izquierda":T.IZQUIERDA,
                      "accion":T.ACCION,"hablar":T.HABLAR,
                      "cancelar":T.CANCELAR_DIALOGO,"inventario":T.INVENTARIO,
                      "posicion":T.CAMBIAR_POSICION,
                      "menu":T.MENU,"debug":T.DEBUG,"salir":T.SALIR}}
        
        Resources.guardar_json('config.json',data)
    
    def asignar(self,data):
        # quiero sacar esto de acá.. pero no sé como evitar la referencia circular
        from globs.constantes import Constants as C
        from globs.teclas import Teclas as T
        Config.recordar = data['recordar_menus']
        Config.intro = data['mostrar_intro']
        C.CUADRO = data['resolucion']['CUADRO']
        C.ANCHO = data['resolucion']['ANCHO']
        C.ALTO = data['resolucion']['ALTO']
        T.asignar(data['teclas'])
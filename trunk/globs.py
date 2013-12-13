#global information
from pygame import K_UP, K_DOWN, K_LEFT, K_RIGHT, \
K_x, K_s, K_a, K_z, K_RETURN, K_ESCAPE, K_LSHIFT, K_F1, \
Color, time, Surface
from misc import Resources as r
from base import _giftSprite, _giftGroup

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


    def asignar (self,data):
        Teclas.ARRIBA = data['arriba']
        Teclas.ABAJO = data['abajo']
        Teclas.IZQUIERDA = data['izquierda']
        Teclas.DERECHA = data['derecha']

        Teclas.ACCION = data['accion']
        Teclas.INVENTARIO = data['inventario']
        Teclas.MENU = data['menu']
        Teclas.SALIR = data['salir']

class Constants:
    CUADRO = 32
    ALTO = 480
    ANCHO = 480

    CAPA_BACKGROUND = 0
    CAPA_GROUND_ITEMS = 1
    CAPA_GROUND_SALIDAS = 2
    CAPA_GROUND_MOBS = 3
    CAPA_HERO = 4
    CAPA_TOP_ITEMS = 5
    CAPA_TOP_MOBS = 6
    CAPA_TOP_CIELO = 7

    CAPA_OVERLAYS_DIALOGOS = 1 # ocupan un framento de la pantalla
    CAPA_OVERLAYS_MENUS = 2 # ocupan toda o gran parte de la pantalla

    COLOR_COLISION = Color(255,0,255) #Fuchsia #FF00FF

    TECLAS = Teclas()

class World:
    mapas = {}
    MAPA_ACTUAL = ''
    HERO = ''
    menu_actual = ''
    menu_previo = ''
    MENUS = {}
    DIALOG = ''
    MODO = 'Aventura'
    onPause = False
    QUESTS = []
    
    def cargar_hero():
        from mobs import PC
        World.HERO = PC('heroe',r.abrir_json('scripts/mobs/hero.mob'),World.MAPA_ACTUAL)

    def setear_mapa(mapa, entrada):
        from mapa import Stage
        if mapa not in World.mapas:
            World.mapas[mapa] = Stage(r.abrir_json('maps/'+mapa+'.json'))
        World.MAPA_ACTUAL = World.mapas[mapa]
        World.MAPA_ACTUAL.cargar_hero(World.HERO, entrada)
        World.MAPA_ACTUAL.mapa.dirty=1
        World.MAPA_ACTUAL.contents.add(Tiempo.noche)
        World.MAPA_ACTUAL.properties.add(Tiempo.noche,layer=Constants.CAPA_TOP_CIELO)
        
class Tiempo:
    FPS = time.Clock()
    _frames,_segs,_mins = 0,0,0 # valores internos
    hora,dia = 0,0 # valores con efecto en el juego.
    angulo_sol = 0
    esNoche = False
    
    nch_img = Surface((480,480))
    nch_img.set_alpha(125)
    noche = _giftSprite(nch_img)
    noche.ubicar(0,0)
    noche.dirty = 2
    noche.visible = False
        
    def contar_tiempo ():
        Tiempo._frames += 1
        if Tiempo._frames == 60:
            Tiempo._segs += 1
            Tiempo._frames = 0
            if Tiempo._segs == 60:
                Tiempo._mins += 1
                Tiempo.hora += 1
                Tiempo._segs = 0
                if Tiempo.hora < 12:
                    Tiempo.angulo_sol = Tiempo.hora*15
                    # 15 = 90º/6; 6 = 12 horas de luz/2 por el abs de sombra
                if Tiempo.hora == 24:
                    Tiempo.dia += 1
                    Tiempo.hora = 0
    
    def anochece(duracion):
        if not Tiempo.esNoche:
            if Tiempo._mins == duracion:
                Tiempo.esNoche = True
                Tiempo.noche.visible = True
                Tiempo._mins = 0
        else:
            if Tiempo._mins == duracion:
                Tiempo.esNoche = False
                Tiempo.noche.visible = False
                Tiempo._mins = 0
        
        return Tiempo.esNoche

class QuestManager:
    quests = {}
    
    def add(script):
        from quests import Quest
        
        if script not in QuestManager.quests:
            quest = Quest(script)
            QuestManager.quests[script] = quest
            for NPC in quest.on_Dialogs:
                MobGroup[NPC].dialogos = quest.on_Dialogs[NPC]
                
    def remove(quest):    
        nombre = quest.nombre
        if nombre in QuestManager.quests:
            del QuestManager.quests[nombre]
            for NPC in quest.off_Dialogs:
                if NPC in MobGroup:
                    npc = MobGroup[NPC]
                    if quest.off_Dialogs[NPC] != []:
                        npc.dialogos = quest.off_Dialogs[NPC]
                    else:
                        npc.dialogos = npc.data['dialogo']
    
    def update():
        conds = {}
        for quest in QuestManager.quests:
            conds[quest] = QuestManager.quests[quest].update()
            
        for quest in conds:
            if conds[quest]:
                QuestManager.remove(QuestManager.quests[quest])

MobGroup = _giftGroup()
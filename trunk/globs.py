#global information
#import pygame
from pygame import K_UP, K_DOWN, K_LEFT, K_RIGHT
from pygame import K_x, K_s, K_a, K_z, K_RETURN, K_ESCAPE, K_LSHIFT
from pygame import Color, time, Surface

from misc import Resources as r
from base import _giftSprite

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
    DEBUG = pygame.K_F1


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

    CAPA_OVERLAYS_DIALOGO = 1
    CAPA_OVERLAYS_INVENTARIO = 2

    COLOR_COLISION = Color(255,0,255) #Fuchsia #FF00FF

    TECLAS = Teclas()

class World:
    mapas = {}
    MAPA_ACTUAL = ''
    HERO = ''
    menu_actual = ''
    menu_previo = ''
    DIALOG = ''
    onDialog = False
    onSelect = False
    onPause = False
    onVSel = False
    QUESTS = []
    
    def cargar_hero():
        from mobs import PC
        World.HERO = PC('heroe','mobs/heroe_idle_walk.png',World.MAPA_ACTUAL)

    def setear_mapa(mapa, entrada):
        from mapa import Stage
        if mapa not in World.mapas:
            World.mapas[mapa] = Stage(r.abrir_json('maps/'+mapa+'.json'))
        World.MAPA_ACTUAL = World.mapas[mapa]
        World.MAPA_ACTUAL.cargar_hero(World.HERO, entrada)
        World.MAPA_ACTUAL.mapa.dirty=1

class Tiempo:
    FPS = time.Clock()
    frames,segs,mins,dias = 0,0,0,0
    esNoche = False
    
    nch_img = Surface((480,480))
    nch_img.set_alpha(125)
    noche = _giftSprite(nch_img)
    noche.ubicar(0,0)
    noche.dirty = 2

    _i = 10
    while _i > 0:
        FPS.tick(60)
        _i -= 1
        
    def contar_tiempo ():
        Tiempo.frames += 1
        if Tiempo.frames == 60:
            Tiempo.segs += 1
            Tiempo.frames = 0
            if Tiempo.segs == 60:
                Tiempo.mins += 1
                Tiempo.segs = 0
                if Tiempo.mins == 20:
                    Tiempo.dias += 1
    
    def anochece(duracion):
        if not Tiempo.esNoche:
            if Tiempo.mins == duracion:
                Tiempo.esNoche = True
                Tiempo.mins = 0
        else:
            if Tiempo.mins == duracion:
                Tiempo.esNoche = False
                Tiempo.mins = 0
        
        return Tiempo.esNoche

class QuestManager:
    quests = {}
    
    def add(script):
        from quests import Quest
        from mobs.MobGroup import MobGroup
        
        if script not in QuestManager.quests:
            quest = Quest(script)
            QuestManager.quests[script] = quest
            for NPC in quest.on_Dialogs:
                MobGroup.mobs[NPC].dialogos = quest.on_Dialogs[NPC]
                
    def remove(quest):
        from mobs.MobGroup import MobGroup
        
        nombre = quest.nombre
        if nombre in QuestManager.quests:
            del QuestManager.quests[nombre]
            for NPC in quest.off_Dialogs:
                if NPC in MobGroup.mobs:
                    npc = MobGroup.mobs[NPC]
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


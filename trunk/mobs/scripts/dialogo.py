from UI import Dialog
from globs import World as W
from random import randint

class Dialogo:
    txt = str(0)
    _txt = 0
    temas_hablados = []
    tema_actual = None
    temas = {}
    mostrar = ''
    locutor = None
    onSelect = False
    onOptions = False
    frontend = None
    fin_de_tema = False
    eligiendo_tema = False
    cursor_sel_tema = 0
    
    def __init__(self,*participantes): # type (participantes) == list
        self.frontend = Dialog()
        self.temas = {}
        self.txt = str(0)
        self._txt = 0
        self.participantes = participantes
        for p in participantes:
            for t in p.temas_para_hablar:
                self.temas[t] = p.temas_para_hablar[t]
                
        ganador_iniciativa = self.iniciativa(*participantes)
        tema = ganador_iniciativa.tema_preferido
        if tema == '':
            self.eligiendo_tema = True
            tema = self.elegir_tema()
        else:
            self.establecer_tema(tema)
            
    def establecer_tema(self,tema):
        self.tema_actual = self.temas[tema]
        self.nombre_tema_act = tema
        #if self.tema_actual['textos'][self.txt]['type'] == 'Q':
        #    self.onSelect = True
        self.update()
    
    def update(self):
        self.frontend.borrar_todo()
        if self.fin_de_tema:
            self.txt = str(0)
            self._txt = 0
            W.MAPA_ACTUAL.endDialog()
        self.fin_de_tema = self.hablar()
        self.frontend.setLocImg(self.locutor)
        if self.mostrar != None:
            self.frontend.setText(self.mostrar)
        
        if self.fin_de_tema:
            W.HERO.conversaciones.append(self.nombre_tema_act)
            for p in self.participantes:
                if hasattr(p,'hablando'):
                    p.hablando = False
        else:
            return True
        
    def iniciativa (self,*participantes):
        part = None
        high = 0
        for participante in participantes:
            inic = participante.iniciativa+randint(1,21)
            if inic > high:
                part = participante
                high = inic
        return part
    
    def hablar(self):
        tree = self.tema_actual['tree']
        textos = self.tema_actual['textos']
        if textos[self.txt]['type'] == 'E':
            self.mostrar = textos[self.txt]['txt']
            self.locutor = textos[self.txt]['loc']
            return True
        
        if textos[self.txt]['type'] == 'Q':
            if not self.onSelect:
                self.mostrar = textos[self.txt]['txt']
                self.locutor = textos[self.txt]['loc']
                self.onSelect = True
                print('bucle Q consigna')
            else:
                self.elegir_opcion(-1)
                self.locutor = textos[str(tree[str(self.txt)][0])]['loc']
                #chapuza: que pasa si las respuestas se dan por multiples personajes?
                opciones = [textos[str(n)]['txt'] for n in tree[str(self.txt)]]
                self.frontend.setSelMode(opciones)
                self.onOptions = True
                self.mostrar = None
                print('bucle Q opciones')
            
        if textos[self.txt]['type'] == 'A':
            self.txt = str(tree[str(self.txt)])
            self.mostrar = textos[self.txt]['txt']
            self.locutor = textos[self.txt]['loc']
            #self.txt = str(tree[str(self.txt)])
            print('bucle A')
            
        if textos[self.txt]['type'] == 'S':
            self.mostrar = textos[self.txt]['txt']
            self.locutor = textos[self.txt]['loc']
            self.txt = str(tree[str(self.txt)])
            print('bucle S')
    
        return False
        
    def elegir_tema(self):
        temas = list(self.temas.keys())
        self.frontend.setSelMode(temas)
        self.frontend.dirty = 1
    
    def elegir_opcion(self,dy):
        if self.tema_actual != None:
            if self.tema_actual['textos'][self.txt]['type'] != 'E':
                tree = self.tema_actual['tree']
                if type(tree[str(self.txt)]) != int:
                    d = self.frontend.elegir_opcion(dy)-1
                    h = tree[str(self.txt)]
                    self._txt = h[d]
        else:
            self.cursor_sel_tema = self.frontend.elegir_opcion(dy)-1
    
    def usar_funcion(self,dummy):
        if self.tema_actual != None:
            if self.onOptions:
                self.confirmar_seleccion()
            else:
                self.update()
        else:
            temas = list(self.temas.keys())
            tema = temas[self.cursor_sel_tema]
            self.establecer_tema(tema)
    
    def confirmar_seleccion(self):
        self.txt = str(self._txt)
        self._txt = 0
        self.onOptions = False
        self.onSelect = False
        self.update()

from engine.UI import DialogInterface
from engine.globs import EngineData as ED
from random import randint

class _elemento:
    '''Class for the dialog tree elements.'''
    parent = None
    nombre = ''
    hasLeads = False
    tipo = ''
    def __init__(self,tipo,indice,texto,locutor,leads=None):
        self.tipo = tipo
        self.indice = indice
        self.nombre = self.tipo.capitalize()+' #'+str(self.indice)
        self.texto = texto
        self.locutor = locutor
        self.leads = leads
        if type(self.leads) == list:
            self.hasLeads = True
        
    def __repr__(self):
        return self.nombre
    
class _ArboldeDialogo:
    __slots__ = ['_elementos','_actual','onSelect']

    def __init__(self,datos):
        self._elementos = []
        self._actual = -1
        self.onSelect = False

        for i in range(len(datos)):
            idx = str(i)
            data = datos[idx]
            
            tipo = data['type']
            leads = data['leads']
            loc = data['loc']
            txt = data['txt']
            
            obj = _elemento(tipo, idx, txt, loc, leads)

            
            self._elementos.append(obj)
        
        for obj in self._elementos:
            if obj.tipo != 'leaf':
                if type(obj.leads) == list:
                    for lead in obj.leads:
                        obj.leads[obj.leads.index(lead)] = self._elementos[lead]
                else:
                    obj.leads = self._elementos[obj.leads]

    def __len__(self):
        return len(self._elementos)
    
    def __repr__(self):
        return '_Arbol de Dialogo ('+str(len(self._elementos))+' elementos)'
    
    def __getitem__(self,item):
        if type(item) != int:
            raise TypeError('expected int, got'+str(type(item)))
        elif not 0 <= item <=len(self._elementos)-1:
            raise IndexError
        else:
            return self._elementos[item]
    
    def __contains__(self,item):
        if item in self._elementos:
            return True
        return False
    
    def get_lead_of (self, parent_i,lead_i=0):
        if isinstance(parent_i,_elemento):
            parent_i = self._elementos.index(parent_i)
        item = self._elementos[parent_i]
        if item.tipo != 'leaf':
            if item.hasLeads:
                if type(item.leads) == list:
                    return item.leads[lead_i]
            else:
                return item.leads
        else:
            raise TypeError('Leaf element has no lead')
    
    def set_actual(self,idx):
        if isinstance(idx,elemento):
            idx = self._elementos.index(idx)
        if 0 <= idx <= len(self._elementos)-1:
            self._actual = idx
        else:
            raise IndexError
    
    def get_actual(self):
        return self._elementos[self._actual]
    
    def next(self):
        nodo = self.get_actual()
        return nodo.leads
    
    def set_chosen(self, choice):
        nodo = self.get_actual()
        if nodo.hasLeads:
            self.set_actual(nodo.leads[choice])
    
    def update(self):
        _actual = self.get_actual()
        nodo = self.next()
        if type(nodo) != list:
            if _actual.tipo == 'leaf':
                return False
            self.set_actual(nodo)
            
        return nodo

class Dialogo:
    def __init__(self,*participantes):
        self.frontend = DialogInterface()
        self.participantes = participantes
        self.funciones = {
            'hablar':self.hablar,
            'arriba':self.elegir_opcion,
            'abajo':self.elegir_opcion,
            'izquierda':self.elegir_opcion,
            'derecha':self.elegir_opcion,
            'inventario':self.mostrar,
            'cancelar':self.cerrar}
    
    def usar_funcion(self,tecla):
        if tecla in self.funciones:
            if tecla in ['arriba','abajo','izquierda','derecha']:
                self.funciones[tecla](tecla)
            else:
                self.funciones[tecla]()
    
    def hablar(self):
        print(self.participantes)
        
    def elegir_opcion(self,direccion):
        print(direccion)
        
    def mostrar(self):
        print(NotImplemented)
    
    def cerrar(self):
        self.frontend.destruir()
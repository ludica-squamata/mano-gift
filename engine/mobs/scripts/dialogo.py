from engine.UI import DialogInterface

class _elemento:
    '''Class for the dialog tree elements.'''
    parent = None
    nombre = ''
    hasLeads = False
    tipo = ''
    indice = None
    locutor = None
    leads = None
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
    
    def __eq__(self,other):
        if type(self) != type(other):
            return False
        elif self.indice != other.indice:
            return False
        else:
            return True
        
    def __ne__(self,other):
        if type(self) == type(other):
            return False
        elif self.indice == other.indice:
            return False
        else:
            return True
    
class _ArboldeDialogo:
    __slots__ = ['_elementos','_actual']

    def __init__(self,datos):
        self._elementos = []
        self._actual = 0

        self._elementos.extend(self._crear_lista(datos))
        
        for obj in self._elementos:
            if obj.tipo != 'leaf':
                if type(obj.leads) is list:
                    idx = -1
                    for lead in obj.leads:
                        idx += 1
                        #workaround: no sé porque, pero lead queda como _elemento
                        if type(lead) is int: #a partir de la segunda vez que se inicia
                            obj.leads[idx] = self._elementos[lead] # el diálogo.
                        else:
                            obj.leads[idx] = lead
                else:
                    obj.leads = self._elementos[obj.leads]
    
    @staticmethod
    def _crear_lista(datos):
        _elem = []
        for i in range(len(datos)):
            idx = str(i)
            data = datos[idx]
            
            tipo = data['type']
            leads = data['leads']
            loc = data['loc']
            txt = data['txt']
            
            _elem.append(_elemento(tipo, idx, txt, loc, leads))
        return _elem
            
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
        if isinstance(idx,_elemento):
            idx = self._elementos.index(idx)
        if 0 <= idx <= len(self._elementos)-1:
            self._actual = idx
        else:
            raise IndexError
    
    def get_actual(self): return self._elementos[self._actual]
    
    def next(self,nodo):  return nodo.leads
    
    def set_chosen(self, choice):
        self.set_actual(self._actual[choice].leads)
              
    def update(self):
        '''Devuelve el nodo actual, salvo que sea un leaf o branch,
        en cuyo caso devuelve False y None (respectivamente), y
        prepara se prepara para devolver el siguiente nodo'''
        
        if self._actual is not False: #last was leaf; close
            if type(self._actual) is not list: #node or leaf
                actual = self.get_actual()
                if actual.tipo != 'leaf':
                    if type(actual.leads) is not list:
                        self._actual = int(actual.leads.indice)
                    else:
                        self._actual = actual.leads
                else:
                    self._actual = False

                return actual
                
            else: #branch
                return self._actual
            
        else: #last was leaf; close
            return self._actual

class Dialogo:
    SelMode = False
    terminar = False
    sel = 0
    def __init__(self,arbol):
        self.frontend = DialogInterface()
        self.dialogo = _ArboldeDialogo(arbol)
        self.func_lin = {
            'hablar':self.hablar,
            'arriba':lambda:None,
            'abajo':lambda:None,
            'izquierda':lambda:None,
            'derecha':lambda:None,
            'inventario':self.mostrar,
            'cancelar':self.cerrar}
        
        self.func_sel = {
            'hablar':self.confirmar_seleccion,
            'arriba':self.elegir_opcion,
            'abajo':self.elegir_opcion,
            'izquierda':self.elegir_opcion,
            'derecha':self.elegir_opcion,
            'inventario':lambda:None,
            'cancelar':self.cerrar}
        
        #empezar con el primer nodo
        nodo = self.dialogo.get_actual()
        self.mostrar_nodo(nodo)
        self.dialogo.update()
    
    def usar_funcion(self,tecla):
        if self.SelMode:
            if tecla in self.func_sel:
                if tecla in ['arriba','abajo','izquierda','derecha']:
                    self.func_sel[tecla](tecla)
                else:
                    self.func_sel[tecla]()
        elif tecla in self.func_lin:
            self.func_lin[tecla]()
 
    def hablar(self):
        
        actual = self.dialogo.update()
        if type(actual) == list:
            self.SelMode = True
            self.frontend.borrar_todo()
            self.frontend.setLocImg(actual[0].locutor) #misma chapuza
            self.frontend.setSelMode([n.texto for n in actual])
        elif actual:
            self.mostrar_nodo(actual)
        else:
            self.cerrar()
    
    def confirmar_seleccion(self):
        self.dialogo.set_chosen(self.sel)
        self.SelMode = False
        self.hablar()
    
    def mostrar_nodo(self,nodo):
        self.frontend.borrar_todo()
        self.frontend.setLocImg(nodo.locutor)
        self.frontend.setText(nodo.texto)
        
    def elegir_opcion(self,direccion):
        if direccion == 'arriba':
            sel = self.frontend.elegir_opcion(-1)
        elif direccion == 'abajo':
            sel = self.frontend.elegir_opcion(+1)
        self.sel = sel
        
    def mostrar(self):
        print(NotImplemented)
    
    def cerrar(self):
        self.frontend.destruir()

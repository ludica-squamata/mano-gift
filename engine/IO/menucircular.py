from pygame.sprite import Sprite, LayeredUpdates
from math import sin,cos,radians
from random import uniform

class BaseElement (Sprite):
    selected = False
    inplace = False
    cascada = []
    angle = 0
    def __init__(self,nombre):
        self.cascada = []
        super().__init__()
        self.nombre = nombre
        self.check_placement()

    def __repr__(self): 
        return self.nombre
    
    def change_angle(self,angle,centerx,centery):
        self.angle = angle
        self.rect.center = centerx,centery
    
    def check_placement(self):
        if self.angle == 0:
            self.inplace = True
        else:
            self.inplace  = False
        
        return self.inplace
        
    def circular (self,delta):
        self.angle += delta
        self.check_placement()
        if self.angle > 359:
            self.angle = 0
        elif self.angle < 0:
            self.angle += 359
        
    def select(self):
        self.image = self.img_sel
        self.rect = self.rect_sel
        self.selected = True
    
    def deselect(self):
        self.image = self.img_uns
        self.rect = self.rect_uns
        self.selected = False
    
    def update(self,delta,puntos):
        self.circular(delta)
        self.rect_sel.center = puntos[self.angle]
        self.rect_uns.center = puntos[self.angle]

class CircularMenu:
    cubos = None #cascada actualmente visible
    cascadaActual = 'inicial'
    cascadaAnterior = ''
    pressed = False
    hold = False
    actual = None 
    di = 0
    radius = 8
    cascadas = {}
    def __init__(self,cascadas,centerx,centery):
        self.cubos = LayeredUpdates()
        self.cascadas = {}
        self.center = centerx,centery
        self.log = str(int(uniform(0,1)*100000))
        
        for key in cascadas:
            grupo = cascadas[key]
            if len(grupo) > 0:
                radius = self.radius*(len(grupo)+1)
                puntos = [self.get_xy(a,radius,centerx,centery) for a in range(-90,270)]           
                separacion = 360//len(grupo)
                angle = -separacion
                for item in grupo:
                    angle += separacion
                    item.change_angle(angle,*puntos[angle])
                self.cascadas[key] = {'items':cascadas[key],'radius':radius,'puntos':puntos}
        
        self.cubos.add(*self.cascadas['inicial']['items'])
            
        self.functions = {
            'keydown':{
                'left':lambda:self.turn(-1),
                'right':lambda:self.turn(+1),
                'accept':self.accept,
                'back':self.back,
                'del': self.supress
            },
            'keyup':{
                'left':self.stop,
                'right':self.stop
            }
        }
        
    def use_keydown_func(self,key): self.use_function('keydown',key)
    def use_keyup_func(self,key):self.use_function('keyup',key)
    def use_function(self,mode,key):
        if key in self.functions[mode]:
            self.functions[mode][key]()
    
    def change_radius(self,x):
        radius = x*(len(self.cascadas[self.cascadaActual])+1)
        self.puntos = [self.get_xy(a,radius,*self.center) for a in range(-90,270)]
        
    @staticmethod
    def get_xy(a,radius,centerX,centerY):
        x = round(centerX + radius * cos(radians(a)))
        y = round(centerY + radius * sin(radians(a)))
        return x,y
    
    def turn(self,delta): #+1 o -1
        self.pressed = True
        self.di = delta
    
    def stop(self):
        self.pressed = False
        self.hold = False
        
    def accept(self):
        if self.di == 0 and self.actual.nombre in self.cascadas:
            self.cascadaAnterior = self.cascadaActual
            self.cascadaActual = self.actual.nombre
            self._change_cube_list()
            
    def back(self):
        if self.di == 0 and self.cascadaAnterior != '':
            self.cascadaActual = self.cascadaAnterior
            self.cascadaAnterior = ''
            self._change_cube_list()
    
    def supress(self):
        self.cubos.remove(self.actual)
        self.cascadas[self.cascadaActual]['items'].remove(self.actual)
        self._modify_cube_list()
    
    def append(self, obj):
        self.cubos.add(obj)
        self.cascadas[self.cascadaActual]['items'].append(obj)
        self._modify_cube_list()
    
    def _change_cube_list(self):
        self.cubos.empty()
        self.cubos.add(*self.cascadas[self.cascadaActual]['items'])
    
    def _modify_cube_list(self):
        self.change_radius(self.radius)
        separacion = 360//len(self.cubos)
        angulo = -separacion #0°
        for cuadro in self.cubos:
            angulo+=separacion
            cuadro.change_angle(angulo,*self.puntos[angulo])
        self.cubos.update(self.di,self.puntos)
        
    def show_angle(self,fondo):
        import pygame.image
        import os.path
        
        ar = open('log-'+self.log+'.txt','a')
        ar.write('len: '+str(len(self.cubos))+'\n')
        for cubo in self.cubos:
            ar.write(cubo.nombre+': '+str(cubo.angle)+'\n')
        ar.write('----------------------------\n')
        
        i = 1
        name = 'image-'+self.log+'-'+str(i)
        while os.path.exists(name+'.png'):
            i += 1
            name = 'image-'+self.log+'-'+str(i)
                
        pygame.image.save(fondo.copy(),name+'.png')
    
    def draw(self,fondo): return self.cubos.draw(fondo)
    
    def update(self):
        for cuadro in self.cubos:
            if cuadro.check_placement():
                if not self.pressed:
                    self.di = 0
                    cuadro.select()
                    self.actual = cuadro
                    self.cubos.move_to_front(self.actual)
            else:
                cuadro.deselect()
                
        if self.cascadaActual in self.cascadas:
            self.cubos.update(self.di,self.cascadas[self.cascadaActual]['puntos'])
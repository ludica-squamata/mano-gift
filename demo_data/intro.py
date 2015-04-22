# intro.py
# animación de introducción. Créditos.
from pygame import Surface, Rect, QUIT, KEYDOWN
from pygame import display as pantalla, event as EVENT,font
from engine.globs import Tiempo as T, Constants as C
from engine.libs.textrect import render_textrect
from engine.misc import Util

def intro (fondo):
    color = {
        "rojo":(255,0,0),
        "verde":(0,255,0),
        "amarillo":(255,255,0),
        "negro":(0,0,0),
        "blanco":(255,255,255)
        }
    
    placas = [
        {
            "fuente":["Verdana",24,"b"],
            "texto": "Lúdica Squamata",
            "color":"verde",
            "fondo":"negro",
            "center":[320,240]
        },
        {
            "fuente":["Verdana",16,"i"],
            "texto":'Presenta...',
            "color":"amarillo",
            "fondo":"negro",
            "center":[380,260]
        },
        {
            "fuente":["Verdana",16],
            "texto":"una producción de\nZeniel Danaku & Einacio Spiegel",
            "color":"rojo",
            "fondo":"negro",
            "center":[320,250]
        },
        {
            "fuente":["Verdana",30,"b"],
            "texto":"Proyecto\nMano-Gift",
            "color":"negro",
            "fondo":"blanco",
            "center":[320,69]
        },
        {
            "fuente":["Verdana",16],
            "texto":'< Presione una tecla para continuar >',
            "color":"rojo",
            "fondo":"blanco",
            "center":[320,436]
        }
    ]
    
    p = []
    for pan in placas:
        f = pan["fuente"]
        _b = False
        _i = False
        if 'b' in f: _b = True
        if 'i' in f: _i = True
        fuente = font.SysFont(f[0],f[1],bold=_b,italic=_i)
        
        w,h = fuente.size(pan['texto'])
        l = len(pan['texto'].splitlines())
        rect = Rect(0,0,w,h*l+1*l)
        rect.center = pan['center']
        
        render = render_textrect(pan["texto"],fuente,rect,color[pan["color"]],color[pan['fondo']],1)
        
        p.append({"render":render,"rect":rect})

        
    running = True
    timer = 0
    
    #index para la lista "p" 
    n = 0
    
    #contadores de alphas para 3 placas distintas (0, 1 y 2)
    a = 0
    b = 0
    c = 0
    
    #contador para el efecto de parpadeo (placa 4)
    j = 0
    while running is True:
        T.FPS.tick(60)
        
        for event in EVENT.get():
            if event.type == QUIT: running = False
            
            if event.type == KEYDOWN:
                if event.key == C.TECLAS.SALIR:
                    Util.salir()
                else:
                    running = False
        
        timer += 1
        if timer <= 60:
            fondo.fill(color['negro'])
        
        # Lúdica Squamata
        elif 61 <= timer <180:
            n = 0
            a+=1
            p[n]['render'].set_alpha(a)
            fondo.blit(p[n]['render'],p[n]['rect'])
        
        # Presenta...
        elif 181 <= timer < 300:
            n = 1
            b += 1
            p[n]['render'].set_alpha(b)
            fondo.blit(p[n]['render'],p[n]['rect'])
        
        # Una producción de Zeniel Danaku & Einacio Spiegel    
        elif 301 <= timer < 600:
            n = 2
            c += 1
            p[n]['render'].set_alpha(c)
            fondo.blit(p[n]['render'],p[n]['rect'])
        
        # Proyecto Mano-Gift 
        elif 601 <= timer < 661:
            fondo.fill(color['blanco'])
        
        elif 662 <= timer < 900:
            n = 3
            fondo.blit(p[n]['render'],p[n]['rect'])
        
        # <Presione una tecla para continuar>
        elif timer > 1200:
            n = 4
            j += 1            
            if j <= 32:
                fondo.blit(p[n]['render'],p[n]['rect'])
            elif j <= 64:
                fondo.fill(color['blanco'],p[n]['rect'])
            else:
                j = 0
            
        pantalla.flip()
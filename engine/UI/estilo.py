from pygame import Color,font

font.init()

class Estilo:
    __fuente = 'verdana'
    fuente_Mi = font.SysFont(__fuente,16,italic=True)
    fuente_Mb = font.SysFont(__fuente,16,bold=True)
    fuente_M = font.SysFont(__fuente,16)
    fuente_I = font.SysFont(__fuente,15)
    fuente_P = font.SysFont(__fuente,14)
    fuente_Pi = font.SysFont(__fuente,14,italic=True)
    fuente_MP = font.SysFont(__fuente,12)
    
    fuente_Mu = font.SysFont(__fuente,16)
    fuente_Mu.set_underline(True)
    
    font_high_color = Color(255,255,255)
    font_low_color = Color(200,200,200)
    font_none_color = Color(0,0,0)
    bg_cnvs = Color(125,125,125)
    bg_bisel_bg = Color(175,175,175)
    bg_bisel_fg = Color(100,100,100)
#tagloader
from engine.libs.render_tagged_text import tag
from engine.misc.resources import Resources as r
from pygame import font, Color

font.init()
'''
    tagfile:{
        tag-name:string,
        font-name:string,
        font-size:integer,
        bold:bool,
        italic:bool,
        fg:color,
        bg:color
        
        color:[list|string]
    }

'''
'''
    tagarrayfile:{
        tag-identifier:string:{
            tag-name:string,
            font-name:string,
            font-size:integer,
            bold:bool,
            italic:bool,
            fg:color,
            bg:color
            
            color:[list|string]
        },
        ....
    }
'''

def load_tagfile(filename):
    d = r.abrir_json(filename)
    
    nombre = d['tag-name']
    data = {
        'fuente': font.SysFont(d.get('font-name'),d.get('font-size'),
                               bold=d.get('bold',False),
                               italic=d.get('italic',False)),
        'fg': Color(*d.get('fg',Color(0,0,0))),
        'bg': Color(*d.get('bg',Color(255,255,255)))
        }
    
    return tag(nombre,data)
    
def load_tagarrayfile(filename):
    d = r.abrir_json(filename)
    tags = {}
    for key in d:
        td = d[key]
        nombre = td['tag-name']
        data = {
            'fuente': font.SysFont(td.get('font-name'),td.get('font-size'),
                                   bold=td.get('bold',False),
                                   italic=td.get('italic',False)),
            'fg': Color(*td.get('fg',Color(0,0,0))),
            'bg': Color(*td.get('bg',Color(255,255,255)))
            }
            
        tags[nombre] = tag(nombre,data)
    
    return tags
# tagloader
from engine.libs.render_tagged_text import Tag
from engine.misc.resources import abrir_json
from pygame import font, Color

'''
    tagarrayfile.json = {
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


def load_tagarrayfile(filename):
    tagarray = abrir_json(filename)
    tags = {}
    _font = "verdana"
    _size = 16
    _bold = False
    _italic = False
    _fg = (0, 0, 0)
    _bg = (255, 255, 255)

    for key in tagarray:
        tagdata = tagarray[key]

        font_name = tagdata.get('font-name', _font)
        font_size = tagdata.get('font-size', _size)
        bold = tagdata.get('bold', _bold)
        italic = tagdata.get('italic', _italic)
        fg = tagdata.get('fg', _fg)
        bg = tagdata.get('bg', _bg)
        name = tagdata.get("tag-name", key)

        data = {
            'fuente': font.SysFont(font_name, font_size, bold=bold, italic=italic),
            'fg': Color(*fg),
            'bg': Color(*bg)
        }
        tags[name] = Tag(name, data)

    return tags

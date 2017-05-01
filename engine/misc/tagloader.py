# tagloader
from engine.libs.render_tagged_text import Tag
from engine.misc.resources import abrir_json
from pygame import font, Color

font.init()

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

    # crear tag por default
    if "n" not in tagarray:
        data = {
            'fuente': font.SysFont(_font, _size, bold=_bold, italic=_italic),
            'fg': Color(*_fg),
            'bg': Color(*_bg)
        }
        tags['n'] = Tag('n', data)

    # buscar default tag por caracteristicas
    for key in tagarray:
        tagdata = tagarray[key]

        font_name = tagdata.get('font-name', _font)
        font_size = tagdata.get('font-size', _size)
        bold = tagdata.get('bold', _bold)
        italic = tagdata.get('italic', _italic)
        fg = tagdata.get('fg', _fg)
        bg = tagdata.get('bg', _bg)

        if font_name == _font and font_size == _size \
                and bold == _bold and italic == _italic \
                and fg == _fg and bg == _bg:
            name = 'n'
        else:
            name = tagdata.get("tag-name", key)

        data = {
            'fuente': font.SysFont(font_name, font_size, bold=bold, italic=italic),
            'fg': Color(*fg),
            'bg': Color(*bg)
        }
        tags[name] = Tag(name, data)

    return tags

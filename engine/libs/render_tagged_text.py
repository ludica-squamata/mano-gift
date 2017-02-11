from pygame import Surface, Rect


class TaggedTextException(BaseException):
    def __init__(self, message=None):
        self.message = message

    def __str__(self):
        return self.message


class Tag:
    fuente = None
    fg = 0, 0, 0
    bg = 255, 255, 255
    init = ''
    close = ''

    def __init__(self, nombre, data):
        self.nombre = nombre
        self.fuente = data.get('fuente')
        self.h = self.fuente.get_height()
        self.fg = data.get('fg')
        self.bg = data.get('bg')
        self.init = '<' + nombre + '>'
        self.close = '</' + nombre + '>'

    def render(self, string):
        return self.fuente.render(string, 1, self.fg)  # ,self.bg)

    def __repr__(self):
        return 'tag ' + self.init


def render_tagged_text(text, tags, w, h=0, bgcolor=(255, 255, 255), _defaultspace=4, line_spacing=1, justification=0):
    actual_lines = []

    last_tag = tags['n']
    rendered_words = []
    line_rect = Rect(0, 0, 0, 0)
    line_num = -1
    tagged = False
    insertion = False
    for _line in text.splitlines():
        line_num += 1
        line_rect.w = 0
        actual_lines.append([])
        line_words = _line.split(' ')
        wordcount = len(line_words)
        current_word_idx = -1

        while current_word_idx + 1 < wordcount:
            wordcount = len(line_words)
            current_word_idx += 1
            _word = line_words[current_word_idx]
            wordspace = _defaultspace
            if _word != '' and not _word[0].isalnum():
                idx = _word.find('<')
                if idx > 0:
                    line_words.insert(current_word_idx + 1, _word[idx:])
                    _word = _word[:idx]
                    wordspace = 0
            if '<' in _word:
                if not tagged:
                    # si ya había sido aplicada una tag, no hay que volver a calcularla
                    _init = _word.find('<') + 1
                    _end = _word.find('>', _init)
                    tag_name = _word[_init:_end]
                    tag = tags[tag_name]
                    # actual_tag = Tag
                    max_word_h = tag.h
                    # else:
                    # actual_tag = last_tag

                if _word.startswith(tag.init) and _word.endswith(tag.close):
                    # casos como <tag>palabra</tag>
                    actual_word = _word[_end + 1:_word.find(tag.close, _end + 1)]
                    tagged = False

                elif _word.startswith(tag.init) and tag.close not in _word:
                    # casos como <tag>palabra
                    actual_word = _word[_end + 1:]
                    tagged = True

                elif _word.endswith(tag.close) and tag.init not in _word:
                    # casos como palabra</tag>
                    actual_word = _word[:_word.find(tag.close)]
                    tagged = False

                elif _word.startswith(tag.init):
                    # en casos como <tag>pala</tag>bra
                    _WORD = _word.split(tag.close)
                    actual_word = _WORD[0][_end + 1:]
                    line_words.insert(current_word_idx + 1, _WORD[1])
                    wordcount += 1
                    wordspace = 0
                    insertion = True

                elif _word.endswith(tag.close):
                    # en casos como pala<tag>bra</tag>
                    _WORD = _word.split(tag.init)
                    actual_word = _WORD[0]
                    wordspace = 0
                    line_words.insert(current_word_idx + 1, tag.init + _WORD[1])
                    wordcount += 1
                    insertion = True
                    tag = last_tag
                    max_word_h = tag.h

                elif tag.close in _word:
                    # en casos como <tag>palabra</tag>!?
                    _WORD = _word.split(tag.close)
                    actual_word = _WORD[0]
                    wordspace = 0
                    line_words.insert(current_word_idx + 1, _WORD[1])
                    tagged = False
                    wordcount += 1
                else:
                    # en casos como <tag>... palabra ... </tag>
                    wordspace = _defaultspace
                    actual_word = _word[_end + 1:]
                    tagged = True
            else:
                actual_word = _word
                if not tagged:
                    tag = tags['n']
                max_word_h = tag.h
                if insertion:
                    wordspace = _defaultspace
                    insertion = False

            rendered_word = tag.render(actual_word)
            rendered_word_rect = rendered_word.get_rect()
            rendered_word_rect.width += wordspace

            if rendered_word_rect.w >= w:
                raise TaggedTextException("The word " + actual_word + " is longer than the width passed.")

            line_w = line_rect.w + rendered_word_rect.w
            if line_w < w:
                rendered_word_rect.left = line_rect.right
                actual_lines[line_num].append([rendered_word, rendered_word_rect])
            else:
                line_num += 1
                line_rect.w = -wordspace
                actual_lines.append([[rendered_word, rendered_word_rect]])

            line_rect.union_ip(rendered_word_rect)
            rendered_words.append([rendered_word, rendered_word_rect])

    line_num = -1
    totalheight = 0
    finallines = []
    for line in actual_lines:
        line_num += 1
        totalwidth = sum([i[1].w for i in line])
        line_surf = Surface((totalwidth, max_word_h))
        line_surf.fill(bgcolor)
        totalheight += max_word_h + line_spacing
        if totalheight > h != 0:
            raise TaggedTextException("Once word-wrapped, the text string was taller than the height passed.")

        for word, rect in line:
            line_surf.blit(word, rect)

        line_rect = line_surf.get_rect()
        line_rect.y = line_num * (line_rect.h + line_spacing)
        finallines.append([line_surf, line_rect])

    if h:
        final_h = h
    else:
        final_h = totalheight
    finalsurf = Surface((w, final_h))
    finalsurf.fill(bgcolor)
    finalrect = finalsurf.get_rect()
    for l_surf, l_rect in finallines:
        if justification == 0:  # left
            l_rect.left = finalrect.left
        elif justification == 1:  # center
            l_rect.centerx = finalrect.centerx
        elif justification == 2:  # right
            l_rect.right = finalrect.right
        else:
            TaggedTextException("Invalid justification argument")
        finalsurf.blit(l_surf, l_rect)

    return finalsurf

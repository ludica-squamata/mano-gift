from pygame import Color
from .event_dispatcher import EventDispatcher


class Colores:
    __defaults = {
        "CANVAS_BG": Color(125, 125, 125),
        "BISEL_BG": Color(175, 175, 175),
        "BISEL_FG": Color(100, 100, 100),
        "TEXT_FG": Color(0, 0, 0),
        "TEXT_DIS": Color(153, 168, 172),
        "TEXT_SEL": Color(255, 255, 255),
        "BOX_SEL_BACK": Color(255, 255, 255),
        "BOX_SEL_TEXT": Color(255, 255, 255),
        "SLOT_BG": Color(153, 153, 153),
        "MENU_TEXT": Color(0, 0, 0),
        "SCROLL_BG": Color(205, 205, 205),
        "SCROLL_ARROW": Color(70, 70, 70)
    }
    themes = {
        "Light": {
            "CANVAS_BG": Color(240, 240, 240),
            "BISEL_BG": Color(255, 255, 255),
            "BISEL_FG": Color(160, 160, 160),
            "TEXT_FG": Color(0, 0, 0),
            "TEXT_DIS": Color(150, 150, 150),
            "TEXT_SEL": Color(255, 255, 255),
            "BOX_SEL_BACK": Color(0, 120, 215),  # azul tipo Windows moderno
            "BOX_SEL_TEXT": Color(255, 255, 255),
            "SLOT_BG": Color(250, 250, 250),
            "MENU_TEXT": Color(0, 0, 0),
            "SCROLL_BG": Color(230, 230, 230),
            "SCROLL_ARROW": Color(90, 90, 90)
        },

        "Dark": {
            "CANVAS_BG": Color(40, 40, 40),
            "BISEL_BG": Color(70, 70, 70),
            "BISEL_FG": Color(20, 20, 20),
            "TEXT_FG": Color(220, 220, 220),
            "TEXT_DIS": Color(120, 120, 120),
            "TEXT_SEL": Color(255, 255, 255),
            "BOX_SEL_BACK": Color(90, 150, 255),
            "BOX_SEL_TEXT": Color(255, 255, 255),
            "SLOT_BG": Color(50, 50, 50),
            "MENU_TEXT": Color(230, 230, 230),
            "SCROLL_BG": Color(70, 70, 70),
            "SCROLL_ARROW": Color(200, 200, 200)
        },
        "Contrast": {
            "CANVAS_BG": Color(0, 0, 0),
            "BISEL_BG": Color(0, 0, 0),
            "BISEL_FG": Color(255, 255, 255),
            "TEXT_FG": Color(255, 255, 0),
            "TEXT_DIS": Color(255, 150, 150),
            "TEXT_SEL": Color(255, 255, 255),
            "BOX_SEL_BACK": Color(255, 255, 0),
            "BOX_SEL_TEXT": Color(255, 0, 0),
            "SLOT_BG": Color(255, 0, 0),
            "MENU_TEXT": Color(255, 255, 0),
            "SCROLL_BG": Color(255, 0, 0),
            "SCROLL_ARROW": Color(255, 255, 255)
        },
        "Retro": {
            "CANVAS_BG": Color(20, 15, 0),
            "BISEL_BG": Color(60, 45, 0),
            "BISEL_FG": Color(10, 8, 0),
            "TEXT_FG": Color(255, 200, 80),
            "TEXT_DIS": Color(120, 90, 40),
            "TEXT_SEL": Color(0, 0, 0),
            "BOX_SEL_BACK": Color(255, 200, 80),
            "BOX_SEL_TEXT": Color(0, 0, 0),
            "SLOT_BG": Color(30, 20, 0),
            "MENU_TEXT": Color(255, 200, 80),
            "SCROLL_BG": Color(50, 35, 0),
            "SCROLL_ARROW": Color(255, 200, 80)
        },
        "Terminal": {
            "CANVAS_BG": Color(0, 20, 0),
            "BISEL_BG": Color(0, 60, 0),
            "BISEL_FG": Color(0, 10, 0),
            "TEXT_FG": Color(120, 255, 120),
            "TEXT_DIS": Color(60, 120, 60),
            "TEXT_SEL": Color(0, 0, 0),
            "BOX_SEL_BACK": Color(120, 255, 120),
            "BOX_SEL_TEXT": Color(0, 0, 0),
            "SLOT_BG": Color(0, 30, 0),
            "MENU_TEXT": Color(120, 255, 120),
            "SCROLL_BG": Color(0, 50, 0),
            "SCROLL_ARROW": Color(120, 255, 120)},

        "RPG parchment": {
            "CANVAS_BG": Color(230, 220, 180),
            "BISEL_BG": Color(255, 245, 210),
            "BISEL_FG": Color(140, 120, 70),
            "TEXT_FG": Color(40, 30, 10),
            "TEXT_DIS": Color(150, 130, 90),
            "TEXT_SEL": Color(255, 255, 255),
            "BOX_SEL_BACK": Color(120, 90, 40),
            "BOX_SEL_TEXT": Color(255, 255, 255),
            "SLOT_BG": Color(240, 230, 190),
            "MENU_TEXT": Color(40, 30, 10),
            "SCROLL_BG": Color(210, 200, 160),
            "SCROLL_ARROW": Color(80, 60, 30)
        },
        "Blue UI": {
            "CANVAS_BG": Color(20, 40, 80),
            "BISEL_BG": Color(50, 80, 140),
            "BISEL_FG": Color(10, 20, 40),
            "TEXT_FG": Color(230, 240, 255),
            "TEXT_DIS": Color(130, 150, 180),
            "TEXT_SEL": Color(255, 255, 255),
            "BOX_SEL_BACK": Color(255, 255, 255),
            "BOX_SEL_TEXT": Color(255, 255, 255),
            "SLOT_BG": Color(30, 60, 110),
            "MENU_TEXT": Color(230, 240, 255),
            "SCROLL_BG": Color(60, 90, 150),
            "SCROLL_ARROW": Color(230, 240, 255)
        },
        "Minimal Dark": {
            "CANVAS_BG": Color(30, 30, 30),
            "BISEL_BG": Color(55, 55, 55),
            "BISEL_FG": Color(10, 10, 10),
            "TEXT_FG": Color(220, 220, 220),
            "TEXT_DIS": Color(120, 120, 120),
            "TEXT_SEL": Color(255, 255, 255),
            "BOX_SEL_BACK": Color(0, 160, 255),
            "BOX_SEL_TEXT": Color(255, 255, 255),
            "SLOT_BG": Color(40, 40, 40),
            "MENU_TEXT": Color(220, 220, 220),
            "SCROLL_BG": Color(60, 60, 60),
            "SCROLL_ARROW": Color(200, 200, 200)
        }
    }
    _changed = {}
    _active_theme = None

    CANVAS_BG = Color(125, 125, 125)
    BISEL_BG = Color(175, 175, 175)
    BISEL_FG = Color(100, 100, 100)

    TEXT_FG = Color(0, 0, 0)
    TEXT_DIS = Color(153, 168, 172)
    TEXT_SEL = Color(255, 255, 255)

    BOX_SEL_BACK = Color(255, 255, 255)
    BOX_SEL_TEXT = Color(255, 255, 255)

    SLOT_BG = Color(153, 153, 153)
    MENU_TEXT = Color(0, 0, 0)

    # estos colores son escenciales del engine, no son solamente estéticos.
    COLOR_COLISION = Color(255, 0, 255)
    COLOR_IGNORADO = Color(1, 1, 1, 0)
    COLOR_SOMBRA = Color(0, 0, 0, 150)

    SCROLL_BG = Color(205, 205, 205)
    SCROLL_ARROW = Color(70, 70, 70)

    @classmethod
    def set_color(cls, key, color, reason=None):
        if hasattr(cls, key):
            if reason not in ['default', 'theme']:
                cls._changed[key] = color.hex
            setattr(cls, key, color)

    @classmethod
    def restore_defaults(cls):
        cls._active_theme = None
        for key in cls.__defaults:
            value = cls.__defaults[key]
            cls.set_color(key, value, reason='default')
            EventDispatcher.trigger('AlterColor', 'Colors', {'name': key, 'color': value})

    @classmethod
    def set_theme(cls, theme):
        cls._active_theme = theme
        for key in cls.themes[theme]:
            value = cls.themes[theme][key]
            cls.set_color(key, value, reason='theme')
            EventDispatcher.trigger('AlterColor', 'Colors', {'name': key, 'color': value})

    @classmethod
    def save(cls, event):
        data = {'colores': {'theme': cls._active_theme, 'changes': cls._changed}}
        EventDispatcher.trigger(event.tipo + 'Data', 'Colores', data)

    @staticmethod
    def _hex_to_rgb(hexa):
        # from: https://stackoverflow.com/questions/29643352/converting-hex-to-rgb-value-in-python
        return tuple(int(hexa[i:i + 2], 16) for i in (0, 2, 4))

    @classmethod
    def load(cls, event):
        data = event.data['savegame']['colores']
        if 'theme' in data:
            cls.set_theme(data['theme'])

        for color_name in data['changes']:
            color = data['changes'][color_name]
            cls.set_color(color_name, Color(cls._hex_to_rgb(color[1:])))


EventDispatcher.register(Colores.save, 'Save')
EventDispatcher.register(Colores.load, 'NewGame')
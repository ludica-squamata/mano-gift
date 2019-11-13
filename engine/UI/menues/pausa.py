from engine.globs import CUADRO, EngineData, FEATURE_MENUS_ADICIONALES, TEXT_FG, CANVAS_BG, Mob_Group, ModData
from engine.globs.event_dispatcher import EventDispatcher
from engine.libs import render_textrect
from engine.misc import Config as Cfg
from pygame.font import SysFont
from engine.UI.hud import HUD
from pygame import Rect
from .menu import Menu


class MenuPausa(Menu):
    nombres = None

    def __init__(self):
        super().__init__("Pausa")
        self.entity = Mob_Group.get_controlled_mob()
        self.timer_animacion = 0
        self.frame_animacion = 1000 / 6

        x = self.canvas.get_width() - (CUADRO * 6) - 14  # 460-192-14 = 254

        names = []
        from . import pause_menus
        for menu_name in pause_menus + (list(ModData.custommenus.keys())):
            # los menúes por default, más los menúes custom declarados en mod.json
            button_name = menu_name[4:]
            if button_name not in names:
                names.append(button_name)

        a, b = 'arriba', 'abajo'
        # expandí un poco las keys para hacer el array más legible
        buttons = []
        for j, nombre in enumerate(names):
            buttons.append({'nombre': nombre, 'direcciones': {a: names[j - 1], b: names[j - (len(names) - 1)]}})

        if FEATURE_MENUS_ADICIONALES:
            buttons[0]['direcciones'][b] = "Status"
            buttons.insert(1, {'nombre': "Status", 'direcciones': {a: "Equipo", b: "Grupo"}})
            buttons.insert(2, {'nombre': "Grupo", 'direcciones': {a: "Status", b: "Opciones"}})
            buttons[3]['direcciones'][a] = "Grupo"

        for i in range(len(buttons)):
            buttons[i]['pos'] = [x, 39 * i + 100]
            buttons[i]['comando'] = self.new_menu

        self.establecer_botones(buttons, 6)
        self.update_charname_display()
        self.functions['tap'].update({
            'accion': self.press_button,
            'arriba': lambda: self.select_one('arriba'),
            'abajo': lambda: self.select_one('abajo')})
        self.functions['hold'].update({
            'accion': self.mantener_presion,
            'arriba': lambda: self.select_one('arriba'),
            'abajo': lambda: self.select_one('abajo')})
        self.functions['release'].update({
            'accion': self.liberar_presion})

    def update_charname_display(self):
        r = self.canvas.blit(self.entity.diag_face[0], (6, 100))
        fuente = SysFont('Verdana', 22)
        w = self.canvas.get_width() - r.right - CUADRO * 6 - 20
        h = fuente.size(self.entity.nombre)[1]
        rect = Rect(r.right + 2, 0, w, h + 1)
        rect.centery = r.centery - 10
        render = render_textrect(self.entity.character_name, fuente, rect, TEXT_FG, CANVAS_BG)
        self.canvas.blit(render, rect)

        self.canvas.blit(HUD.BarraVida.image, (r.right + 2, r.centery + 4))
        self.canvas.blit(HUD.BarraMana.image, (r.right + 2, r.centery + 16))

    def cancelar(self):
        EngineData.acceso_menues.clear()
        self.deregister()
        EventDispatcher.trigger('EndDialog', self, {'layer': self.layer})

    def new_menu(self):
        self.deregister()
        EventDispatcher.trigger('OpenMenu', self.nombre, {'value': self.current.nombre})

    def reset(self):
        """Reseta el presionado de todos los botones, y deja seleccionado
        el que haya sido elegido anteriormente."""
        self.deselect_all(self.botones)
        if not Cfg.dato("recordar_menus"):
            self.cur_btn = 0
        selected = self.botones.get_sprite(self.cur_btn)
        selected.ser_elegido()
        self.current = selected
        self.update_charname_display()

        self.active = True

    def update(self):
        self.botones.update()
        self.botones.draw(self.canvas)

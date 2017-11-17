from engine.globs.eventDispatcher import EventDispatcher
from engine.globs import CUADRO, EngineData, FEATURE_MENUS_ADICIONALES, TEXT_FG, CANVAS_BG
from engine.libs import render_textrect
from engine.misc import Config as Cfg
from pygame.font import SysFont
from pygame import Rect
from .menu import Menu


class MenuPausa(Menu):
    def __init__(self):
        super().__init__("Pausa")
        x = self.canvas.get_width() - (CUADRO * 6) - 14  # 460-192-14 = 254
        m, k = 'nombre', 'direcciones'
        a, b = 'arriba', 'abajo'

        botones = [
            {m: "Equipo", k: {a: "Cargar", b: "Opciones"}},
            {m: "Opciones", k: {a: "Equipo", b: "Cargar"}},
            {m: "Cargar", k: {a: "Opciones", b: "Custom"}},
        ]

        if FEATURE_MENUS_ADICIONALES:
            botones[0][k][b] = "Status"
            botones.insert(1, {m: "Status", k: {a: "Equipo", b: "Grupo"}})
            botones.insert(2, {m: "Grupo", k: {a: "Status", b: "Opciones"}})
            botones[3][k][a] = "Grupo"

        for i in range(len(botones)):
            botones[i]['pos'] = [x, 39 * i + 100],
            botones[i]['comando'] = self.new_menu

        self.establecer_botones(botones, 6)
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
        r = self.canvas.blit(EngineData.HERO.diag_face, (6, 100))
        fuente = SysFont('Verdana', 22)
        w = self.canvas.get_width() - r.right - CUADRO * 6 - 20
        h = fuente.size(EngineData.char_name)[1]
        rect = Rect(r.right + 2, 0, w, h + 1)
        rect.centery = r.centery-10
        render = render_textrect(EngineData.char_name, fuente, rect, TEXT_FG, CANVAS_BG)
        self.canvas.blit(render, rect)

        self.canvas.blit(EngineData.HUD.BarraVida.image, (r.right + 2, r.centery + 4))
        self.canvas.blit(EngineData.HUD.BarraMana.image, (r.right + 2, r.centery + 16))

    def cancelar(self):
        EngineData.acceso_menues.clear()
        self.deregister()
        EngineData.end_dialog(self.layer)

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

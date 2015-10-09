from .menu import Menu
from engine.globs import Constants as Cs
from engine.misc import Config as Cfg
from engine.UI.widgets import Boton


class MenuPausa(Menu):
    def __init__(self):
        super().__init__("Pausa")
        x = self.canvas.get_width() - (Cs.CUADRO * 6) - 14  # 460-192-14 = 254
        m, k, p, c = 'nombre', 'direcciones', 'pos', 'comando'
        a, b, i, d = 'arriba', 'abajo', 'izquierda', 'derecha'

        botones = [
            {m: "Items", p: [x, 93], k: {b: "Equipo"}, c: self.press_one},
            {m: "Equipo", p: [x, 132], k: {a: "Items", b: "Status"}, c: self.press_one},
            {m: "Status", p: [x, 171], k: {a: "Equipo", b: "Grupo"}, c: self.press_one},
            {m: "Grupo", p: [x, 210], k: {a: "Status", b: "Opciones"}, c: self.press_one},
            {m: "Opciones", p: [x, 249], k: {a: "Grupo", b: "Debug"}, c: self.press_one},
            {m: "Debug", p: [x, 288], k: {a: 'Opciones'}, c: self.press_one}]

        self.establecer_botones(botones, 6)
        self.select_one('arriba')
        self.funciones = {
            "arriba": self.select_one,
            "abajo": self.select_one,
            "izquierda": self.select_one,
            "derecha": self.select_one,
            "hablar": self.current.comando}

    def establecer_botones(self, botones, ancho_mod):
        for btn in botones:
            boton = Boton(btn['nombre'], ancho_mod, btn['comando'], btn['pos'])
            for direccion in ['arriba', 'abajo', 'izquierda', 'derecha']:
                if direccion in btn['direcciones']:
                    boton.direcciones[direccion] = btn['direcciones'][direccion]

            self.botones.add(boton)

        self.cur_btn = 0
        self.reset()

    def select_one(self, direccion):
        self.deselect_all(self.botones)
        if len(self.botones) > 0:
            self.current = self.botones.get_sprite(self.cur_btn)
            if direccion in self.current.direcciones:
                selected = self.current.direcciones[direccion]
            else:
                selected = self.current.nombre

            for i in range(len(self.botones)):
                boton = self.botones.get_sprite(i)
                if boton.nombre == selected:
                    boton.ser_elegido()
                    self.mover_cursor(boton)
                    break

            self.botones.draw(self.canvas)

    def cancelar(self):
        return False

    def press_one(self):
        from engine.IO.modos import Modo
        super().press_button()
        Modo.newMenu = True

    def reset(self):
        """Reseta el presionado de todos los botones, y deja seleccionado
        el que haya sido elegido anteriormente."""
        self.deselect_all(self.botones)
        if not Cfg.dato("recordar_menus"):
            self.cur_btn = 0
        selected = self.botones.get_sprite(self.cur_btn)
        selected.ser_elegido()
        self.current = selected
        self.botones.draw(self.canvas)
        self.active = True

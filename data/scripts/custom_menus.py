from engine.UI.menues import Menu


class MenuCustom(Menu):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print('anda!')

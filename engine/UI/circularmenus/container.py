from .rendered import RenderedCircularMenu
from .elements import ContainedInventoryElement


class ContainerCircularMenu(RenderedCircularMenu):
    first = 0

    def __init__(self, parent):
        self.entity = parent
        self.parent = parent
        cascadas = {
            'inicial': [
                ContainedInventoryElement(self, item) for item in parent.inventario.uniques()
            ]
        }

        super().__init__(cascadas)

        self.functions['tap'].update({'contextual': self.salir})
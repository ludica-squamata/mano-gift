from engine.globs import Item_Group, Deleted_Items
from .rendered import RenderedCircularMenu
from .elements import BranchElement


class DialogCircularMenu(RenderedCircularMenu):
    locutores = None

    def __init__(self, *locutores):
        self.locutores = locutores
        self.change_radius = False
        self.radius = 60
        self.nombre = 'Dialog'

        super().__init__({'inicial': []})
        self.deregister()

    def create_elements(self, parent, opciones):
        self.supress_all()
        cascada = []
        for i in range(len(sorted(opciones, key=lambda o: o.indice))):
            opt = opciones[i]
            name = str(opt.leads)
            if opt.reqs is not None and 'objects' in opt.reqs:
                objeto = opt.reqs['objects'][0]
                # la alternativa a este embrollo es que el branch especifique nombre e icono
                item = None
                existing_items = Item_Group + Deleted_Items
                if objeto in existing_items:
                    item = existing_items[objeto]

                icon = item.image
                name = item.nombre

            else:
                icon = parent.request_icon()

            cascada.append(BranchElement(parent, {'idx': i + 1, 'icon': icon, 'name': name, 'item': opciones[i]}))

        self.add_cascades({'inicial': cascada})
        self.switch_cascades()
        self.actual = self.check_on_spot()

    def cerrar(self):
        for mob in self.locutores:
            mob.hablando = False
        self.salir()

    def salir(self):
        self.cascadaActual = 'inicial'
        super().salir()

    def back(self):
        if self.cascadaActual == 'inicial':
            self.cerrar()
        else:
            super().backward()

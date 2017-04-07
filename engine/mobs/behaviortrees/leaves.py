from .status import Running
from types import MethodType
from .node import Node

__all__ = ['Leaf', 'CallingLeaf']


class Leaf(Node):
    type = 'Leaf'
    process = None
    data = None
    process_name = ''

    def __init__(self, tree, idx, process_name):
        # leaves are incapable of having any children
        super().__init__(tree, idx)
        self.process_name = process_name

    def __repr__(self):
        return self.type + ' #' + str(self.idx) + ' (' + self.process_name + ')'

    def set_process(self, process):
        self.process = None
        self.process = MethodType(process, self)

    def update(self):
        status = self.process()
        if status is None:
            status = Running

        self.parent.get_child_status(status)


class CallingLeaf(Node):
    def __init__(self, tree, idx):
        # these leves can call another tree with existing shared context
        super().__init__(tree, idx)

from .status import Running
from types import MethodType


class Node:
    idx = None
    parent = None
    type = ''

    def __init__(self, tree, idx):
        self.idx = idx
        self.tree = tree

    def set_parent(self, parent):
        self.parent = parent

    def get_entity(self):
        return self.tree.entity

    def reset(self):
        pass


class Leaf(Node):
    type = 'Leaf'
    process = None
    data = None

    def __init__(self, tree, idx, data, process_name):
        # leaves are incapable of having any children
        super().__init__(tree, idx)
        self.data = data
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

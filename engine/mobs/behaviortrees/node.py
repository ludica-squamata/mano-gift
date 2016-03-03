from .status import Running
from types import MethodType


class Node:
    idx = None
    parent = None
    entity = None
    type = ''

    def __init__(self, tree, idx, entity):
        self.idx = idx
        self.tree = tree
        self.entity = entity

    def set_parent(self, parent):
        self.parent = parent

        
class Leaf(Node):
    type = 'Leaf'
    process = None
    tick = 0

    def __init__(self, tree, idx, entity, data, process_name):
        # leaves are incapable of having any children
        super().__init__(tree, idx, entity)
        self.data = data
        self.process_name = process_name

    def __repr__(self):
        return self.type + ' #' + str(self.idx) + ' (' + self.process_name + ')'

    def set_process(self, process):
        self.process = MethodType(process, self)

    def update(self):
        status = self.process(*self.data)
        if status is None:
            status = Running

        self.parent.get_child_status(status)

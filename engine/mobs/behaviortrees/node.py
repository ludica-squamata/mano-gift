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

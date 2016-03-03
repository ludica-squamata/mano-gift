from collections import OrderedDict
from .composites import *
from .decorators import *
from .node import Leaf
from types import FunctionType, MethodType


class BehaviourTree:
    # this is a container.
    nodes = []
    tree_structure = None
    to_check = None

    def __init__(self, entity, tree_data, scripts):
        self.tree_structure = OrderedDict()
        for key in [str(i) for i in range(len(tree_data))]:
            node = None
            data = tree_data[key]
            idx = int(key)
            self.tree_structure[idx] = []

            name = data['name']
            if 'children' in data:  # composite
                self.tree_structure[idx].extend(data['children'])
                if name == 'Selector':
                    node = Selector(self, idx, entity, data['children'])
                elif name == 'Secuence':
                    node = Secuence(self, idx, entity, data['children'])

            elif 'child' in data:  # decorator
                self.tree_structure[idx].append(int(data['child']))
                if name == 'Repeater':
                    node = Repeater(self, idx, entity, data['child'], data.get('context', 0))
                elif name == 'UntilFail':
                    node = UntilFail(self, idx, entity, data['child'])
                elif name == 'Succeeder':
                    node = Succeeder(self, idx, entity, data['child'])
                elif name == 'Inverter':
                    node = Inverter(self, idx, entity, data['child'])

            else:  # leaf
                process = None
                if name in globals():
                    process = globals()[name]

                elif hasattr(scripts, name):
                    process = getattr(scripts, name)

                if isinstance(process, FunctionType):
                    node = Leaf(self, idx, entity, data['context'], name)
                    node.set_process(process)

                elif issubclass(process, Leaf):
                    node = process(self, idx, entity, data['context'], name)

            self.nodes.append(node)

        self.set_parents()
        self.set_children()
        self.to_check = self.nodes[0]

    def __repr__(self):
        return 'BehaviourTree: current node #' + str(self.to_check.idx)

    def set_parents(self):
        for idx in self.tree_structure.keys():
            if len(self.tree_structure[idx]):
                node = self.nodes[idx]
                for idxn in self.tree_structure[idx]:
                    self.nodes[idxn].set_parent(node)

    def set_children(self):
        for idx in self.tree_structure.keys():
            if len(self.tree_structure[idx]):
                if hasattr(self.nodes[idx], 'children'):
                    for idxn in self.nodes[idx].children:
                        node = self.nodes[idxn]
                        index = self.nodes[idx].children.index(idxn)
                        self.nodes[idx].children[index] = node

                elif hasattr(self.nodes[idx], 'child'):
                    idxn = self.tree_structure[idx][0]
                    node = self.nodes[idxn]
                    self.nodes[idx].child = node

    def set_to_check(self, node):
        self.to_check = node

    def reset_to_check(self):
        self.to_check = None

    def update(self):
        if self.to_check is not None:
            self.to_check.update()
        else:
            return True

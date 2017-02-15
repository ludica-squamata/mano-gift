from collections import OrderedDict
from types import FunctionType
from engine.globs import ModData
from engine.misc import Resources
from .status import Success
from .composites import *
from .decorators import *
from .leaves import Leaf


class BehaviourTree:
    # this is a container.
    nodes = []
    tree_structure = None
    to_check = None
    node_set = False
    shared_context = {}
    status = None
    entity = None

    def __init__(self, entity, tree_data):
        if self.tree_structure is not None:
            self.tree_structure.clear()
        self.nodes = []
        self.shared_context = {}

        loaded_functions = {}
        head = tree_data.pop('head')
        for script in head['script']:
            module = Resources.load_module_from_script(script)
            for name in head['script'][script]:
                if hasattr(module, name):
                    loaded_functions[name] = getattr(module, name)

        self.tree_structure = OrderedDict()
        self.entity = entity
        tree_data = self.analyze_tree(tree_data['body'])
        for key in [str(i) for i in range(len(tree_data))]:
            node = None
            process = None
            data = tree_data[key]
            idx = int(key)
            self.tree_structure[idx] = []

            name = data['name']
            if 'children' in data:  # composite
                self.tree_structure[idx].extend(data['children'])
                if name == 'Selector':
                    node = Selector(self, idx, data['children'])
                elif name == 'Sequence':
                    node = Sequence(self, idx, data['children'])

            elif 'child' in data:  # decorator
                self.tree_structure[idx].append(int(data['child']))
                if name == 'Repeater':
                    times = 0
                    if head['special']['Repeater']['ID'] == idx:
                        times = head['special']['Repeater']['times']
                    node = Repeater(self, idx, data['child'], times=times)
                elif name == 'UntilFail':
                    node = UntilFail(self, idx, data['child'])
                elif name == 'Succeeder':
                    node = Succeeder(self, idx, data['child'])
                elif name == 'Inverter':
                    node = Inverter(self, idx, data['child'])

            else:  # leaf
                if name in globals():
                    process = globals()[name]

                elif name in loaded_functions:
                    process = loaded_functions[name]

                arg = data.get('arg', None)
                if isinstance(process, FunctionType):
                    node = Leaf(self, idx, name, arg)
                    node.set_process(process)

                elif issubclass(process, Leaf):
                    node = process(self, idx, name, arg)

            self.nodes.append(node)

        self.set_parents()
        self.set_children()
        self.to_check = self.nodes[0]

    def __repr__(self):
        return 'BehaviourTree: current node #' + str(self.to_check.idx)

    def analyze_tree(self, tree_data):
        key = None
        new_tree = None

        for key in [str(i) for i in range(len(tree_data))]:
            idx = int(key)
            name = tree_data[key]['name']
            if name == 'ExtenderLeaf':
                an_tree = tree_data[key]['tree']
                new_tree = self.extend_tree(an_tree, idx)
                Resources.load_module_from_script(an_tree)
                break

        if new_tree:
            del tree_data[key]
            tree_data.update(new_tree)
        return tree_data

    @staticmethod
    def extend_tree(an_tree_data, idx):
        tree_extension = Resources.abrir_json(ModData.mobs + 'behaviours/' + an_tree_data + '.json')
        new_tree = {}
        for kex in tree_extension:
            if 'children' in tree_extension[kex]:
                for i in range(len(tree_extension[kex]['children'])):
                    tree_extension[kex]['children'][i] += idx
            elif 'child' in tree_extension[kex]:
                tree_extension[kex]['child'] += idx
            idy = str(int(kex) + idx)
            new_tree[idy] = tree_extension[kex]
        return new_tree

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
        if self.node_set is False:
            self.to_check = node
            self.node_set = True

    def set_context(self, key, value):
        self.shared_context[key] = value

    def get_context(self, key):
        return self.shared_context[key]

    def clear_context(self):
        self.shared_context.clear()

    def reset(self):
        self.status = None
        self.to_check = self.nodes[0]
        for node in self.nodes:
            node.reset()

    def update(self):
        if self.status is not Success:
            self.to_check.update()
            self.node_set = False
        else:
            return self.status

from importlib import import_module
from collections import OrderedDict
from engine.misc import abrir_json
from engine.globs import ModData
from types import FunctionType
from .r_composites import *
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

    _loaded_functions = None

    def __init__(self, entity, tree_data):
        if self.tree_structure is not None:
            self.tree_structure.clear()
        self.nodes = []
        self.shared_context = {}
        self._loaded_functions = {}

        special = tree_data['head'].pop('special')
        self.load_script_information(tree_data['head'].pop('script'))
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
                elif name == 'Parallel':
                    sucess_value, failure_value = 0, 0
                    parallel = special.get('Parallel', False)
                    if parallel and parallel['ID'] == idx:
                        sucess_value = special['Parallel'].get('Sucess_value', 0)
                        failure_value = special['Parallel'].get('Failure_value', 0)
                    node = Parallel(self, idx, data['children'], sucess_value, failure_value)
                elif name == 'RSelector':
                    node = RandomSelector(self, idx, data['children'])
                elif name == 'RSequence':
                    node = RandomSequence(self, idx, data['children'])

            elif 'child' in data:  # decorator
                self.tree_structure[idx].append(int(data['child']))
                if name == 'Repeater':
                    times = 0
                    repeater = special.get('Repeater', False)
                    if repeater and repeater['ID'] == idx:
                        times = special['Repeater']['times']
                    node = Repeater(self, idx, data['child'], times=times)
                elif name == 'UntilFail':
                    node = UntilFail(self, idx, data['child'])
                elif name == 'Succeeder':
                    node = Succeeder(self, idx, data['child'])
                elif name == 'Inverter':
                    node = Inverter(self, idx, data['child'])
                elif name == 'Failer':
                    node = Failer(self, idx, data['child'])
                elif name == 'UntilSuccess':
                    node = UntilSuccess(self, idx, data['child'])

            else:  # leaf
                if name in globals():
                    process = globals()[name]

                elif name in self._loaded_functions:
                    process = self._loaded_functions[name]

                if isinstance(process, FunctionType):
                    node = Leaf(self, idx, name)
                    node.set_process(process)

                elif issubclass(process, Leaf):
                    node = process(self, idx, name)

            self.nodes.append(node)

        self.set_parents()
        self.set_children()
        self.to_check = [self.nodes[0]]

    def __repr__(self):
        return 'BehaviourTree'

    def unload(self):
        # this is just a hook that does nothing. Don't delete it.
        pass

    def load_script_information(self, head_data):
        for script in head_data:
            ruta = ModData.pkg_scripts.replace('.', '/') + '/' + script
            modulo = import_module('.'.join([ModData.pkg_scripts, script.replace('/', '.')]), ruta)
            for name in head_data[script]:
                if hasattr(modulo, name):
                    self._loaded_functions[name] = getattr(modulo, name)

    def analyze_tree(self, tree_data):
        key = None
        new_tree = None

        for key in [str(i) for i in range(len(tree_data))]:
            idx = int(key)
            name = tree_data[key]['name']
            if name == 'ExtenderLeaf':
                extension = abrir_json(ModData.mobs + 'behaviours/' + tree_data[key]['tree'] + '.json')
                head = extension.pop('head')
                body = extension.pop('body')
                new_tree = self.extend_tree(body, idx)
                self.load_script_information(head)
                break

        if new_tree:
            del tree_data[key]
            tree_data.update(new_tree)
        return tree_data

    @staticmethod
    def extend_tree(new_body, idx):
        new_tree = {}
        for kex in new_body:
            if 'children' in new_body[kex]:
                for i in range(len(new_body[kex]['children'])):
                    new_body[kex]['children'][i] += idx
            elif 'child' in new_body[kex]:
                new_body[kex]['child'] += idx
            idy = str(int(kex) + idx)
            new_tree[idy] = new_body[kex]
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

    def set_to_check(self, *nodes):
        if self.node_set is False:
            self.to_check = [*nodes]
            self.node_set = True

    def set_context(self, key, value):
        self.shared_context[key] = value

    def get_context(self, key, default_value=False):
        if key in self.shared_context:
            return self.shared_context[key]
        else:
            return default_value

    def clear_context(self):
        self.shared_context.clear()

    def erase_keys(self, *keys):
        """
        This method erases the indicated keys from the shared context. It works as clear_context(), but selectively.
        """
        for key in keys:
            if key in self.shared_context:
                del self.shared_context[key]

    def preserve_keys(self, *keys):
        """
        This method erases all keys from the shared conext, except those which are preserved.
        """
        preserved = {}
        for key in keys:
            preserved[key] = self.shared_context[key]

        self.clear_context()
        for key in preserved:
            self.set_context(key, preserved[key])

    def set_status(self, status):
        """"
        Sets the status of the entire tree. Otherwise, the status is None.
        """
        self.status = status

    def reset(self):
        self.status = None
        self.to_check = self.nodes[0]
        self.clear_context()
        for node in self.nodes:
            node.reset()

    def update(self):
        if self.status is None:
            for node in self.to_check:
                node.update()
            self.node_set = False
        else:
            return self.status

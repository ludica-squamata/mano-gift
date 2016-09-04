from random import choice, randint
from .composites import *
from .status import *


class RandomComposite(Composite):
    explored_children = []

    def __init___(self, tree, idx, children):
        super().__init__(tree, idx, children)
        self.current_id = randint(0, len(children))
        self.explored_children.append(self.children[self.current_id])


class RandomSequence(Sequence):
    explored_children = []

    def get_child_status(self, status):
        if status is Success:
            idx = choice(self.children)
            while idx in self.explored_children:
                idx = choice(self.children)

            self.explored_children.append(idx)
            self.current_id = idx

            if not len(self.explored_children) == len(self.children):
                status = Running
        
        if status is Running:
            self.tree.set_to_check(self.children[self.current_id])
        
        if self.parent is not None:
            self.parent.get_child_status(status)

        elif status is Success:
            self.tree.reset_to_check()


class RandomSelector(Selector):
    explored_children = []

    def get_child_status(self, status):
        if status is Failure:
            idx = choice(self.children)
            while idx in self.explored_children:
                idx = choice(self.children)

            self.explored_children.append(idx)
            self.current_id = idx

            if not len(self.explored_children) == len(self.children):
                status = Running

        if status is Running:
            self.tree.set_to_check(self.children[self.current_id])
        
        if self.parent is not None:
            self.parent.get_child_status(status)

        elif status is Success:
            self.tree.reset_to_check()

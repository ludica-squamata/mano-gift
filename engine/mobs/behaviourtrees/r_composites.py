from engine.libs import choice, randint
from .composites import *
from .status import *

__all__ = ['RandomSequence', 'RandomSelector']


class RandomComposite(Composite):
    explored_children = None
    type = "RandomComposite"

    def __init__(self, tree, idx, children):
        super().__init__(tree, idx, children)
        self.current_id = randint(0, len(children))
        self.explored_children = []
        self.explored_children.append(self.children[self.current_id])


class RandomSequence(RandomComposite):
    name = "RandomSequence"

    def get_child_status(self, status):
        if status is Success:
            idx = choice(self.children)
            while idx in self.explored_children:
                idx = choice(self.children)

            self.explored_children.append(idx)
            self.current_id = idx

            if not len(self.explored_children) == len(self.children):
                status = Running
            else:
                self.reset()

        if status is Running:
            self.tree.set_to_check(self.children[self.current_id])

        if self.parent is not None:
            self.parent.get_child_status(status)
        else:
            self.tree.set_status(status)


class RandomSelector(RandomComposite):
    name = "RandomSelector"

    def get_child_status(self, status):
        if status is Failure:
            idx = choice(self.children)
            while idx in self.explored_children:
                idx = choice(self.children)

            self.explored_children.append(idx)
            self.current_id = idx

            if not len(self.explored_children) == len(self.children):
                status = Running
            else:
                self.reset()

        if status is Running:
            self.tree.set_to_check(self.children[self.current_id])

        if self.parent is not None:
            self.parent.get_child_status(status)
        else:
            self.tree.set_status(status)

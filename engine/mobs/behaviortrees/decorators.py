from .node import Node
from .status import *


class Decorator(Node):
    type = 'Decorator'
    child = None

    def __init__(self, tree, idx, child):
        # these nodes can only point to one child
        super().__init__(tree, idx)
        self.child_idx = child
    
    def update(self):
        self.child.update()

        
class Repeater(Decorator):
    name = 'Repeater'
    current_time = -1

    def __init__(self, tree, idx, child, times=None):
        super().__init__(tree, idx, child)
        if times is not None and times > 0:
            self.amount_of_times = times
        else:
            self.amount_of_times = None

    def __repr__(self):
        return self.type + ' #' + str(self.idx) + ' ' + self.name
        
    def get_child_status(self, status):
        if self.amount_of_times is None:
            self.tree.set_to_check(self.child)

        elif self.current_time <= self.amount_of_times:
            self.tree.set_to_check(self.child)

        else:
            self.parent.get_child_status(status)

    def update(self):
        self.current_time += 1
        super().update()

        
class UntilFail(Decorator):
    name = 'UntilFail'

    def __repr__(self):
        return self.type + ' #' + str(self.idx) + ' ' + self.name

    def get_child_status(self, status):
        if status is Failure:
            self.parent.get_child_status(Success)
        
        else:
            self.tree.set_to_check(self.child)

        
class Succeeder(Decorator):
    name = 'Succeeder'

    def __repr__(self):
        return self.type + ' #' + str(self.idx) + ' ' + self.name

    def get_child_status(self, status):
        del status  # PyCharm me obliga a hacer algo con el parámetro
        self.parent.get_child_status(Success)


class Inverter(Decorator):
    name = 'Inverter'

    def __repr__(self):
        return self.type + ' #' + str(self.idx) + ' ' + self.name

    def get_child_status(self, status):
        if status is Success:
            status = Failure
        
        elif status is Failure:
            status = Success

        self.parent.get_child_status(status)

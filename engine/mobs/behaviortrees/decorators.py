from .node import Node
from .status import *


class Decorator(Node):
    type = 'Decorator'
    child = None
    name = ''

    def __init__(self, tree, idx, child):
        # these nodes can only point to one child
        super().__init__(tree, idx)
        self.child_idx = child

    def __repr__(self):
        return self.type + ' #' + str(self.idx) + ' ' + self.name
    
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

    def get_child_status(self, status):
        if status is Failure:
            self.parent.get_child_status(Success)
        
        else:
            self.tree.set_to_check(self.child)

        
class Succeeder(Decorator):
    name = 'Succeeder'

    def get_child_status(self, status):
        del status  # PyCharm me obliga a hacer algo con el parámetro
        self.parent.get_child_status(Success)


class Inverter(Decorator):
    name = 'Inverter'

    def get_child_status(self, status):
        if status is Success:
            status = Failure
        
        elif status is Failure:
            status = Success

        self.parent.get_child_status(status)


# New Decorators based on http://guineashots.com/2014/08/10/an-introduction-to-behavior-trees-part-3
class Failer(Decorator):
    name = 'Failer'

    def get_child_status(self, status):
        del status  # PyCharm me obliga a hacer algo con el parámetro
        self.parent.get_child_status(Failure)


class UntilSuccess(Decorator):
    name = 'UntilSuccess'

    def get_child_status(self, status):
        if status is Success:
            self.parent.get_child_status(Success)

        else:
            self.tree.set_to_check(self.child)


class Limiter(Decorator):
    # This decorator imposes a maximum number of calls its child can have within the whole execution of the Behavior
    # Tree, i.e., after a certain number of calls, its child will never be called again.
    name = 'Limiter'


class MaxTime(Decorator):
    # This decorator limits the maximum time its child can be running. If the child does not complete its execution
    # before the maximum time, the child task is terminated and a failure is returned.
    name = 'MaxTime'

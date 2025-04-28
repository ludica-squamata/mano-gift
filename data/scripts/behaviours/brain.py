from engine.mobs.behaviourtrees import Leaf, Success, Failure


class BePassive(Leaf):
    def process(self):
        e = self.get_entity()
        hates = self.tree.get_context('hates')
        if hates is False:
            e.switch_behaviour('ai')
            return Success
        else:
            return Failure


class BeAgressive(Leaf):
    def process(self):
        e = self.get_entity()
        e.switch_behaviour('agressive')

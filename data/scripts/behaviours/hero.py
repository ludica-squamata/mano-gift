from engine.mobs.behaviourtrees import Leaf
from engine.mobs.behaviourtrees import Success, Failure
from engine.mobs.controllableai import ControllableAI
from math import sqrt


class IsBaseAISet(Leaf):
    def process(self):
        if self.tree.get_context('base_ai_set'):
            return Success
        else:
            return Failure


class SetBaseAI(Leaf):
    def process(self):
        entity = self.get_entity()
        ai = ControllableAI(entity)
        self.tree.set_context('base_ai_set', ai)
        return Success


class ClearContext(Leaf):
    def process(self):
        # self.tree.erase_keys('perceived_props', "perceived_mobs", "close")
        return Success


class UpdateAI(Leaf):
    def process(self):
        ai = self.tree.get_context('base_ai_set')
        if type(ai) is not bool:
            ai.update()
            return Success
        else:
            return Failure

class IsHeSeeingAProp(Leaf):
    def process(self):
        entity = self.get_entity()
        preception = entity.perceived
        sprites = set(preception['seen'])
        perceived_props = []
        for sprite in sprites:
            if sprite.tipo == 'Prop':
                perceived_props.append(sprite)

        if len(perceived_props) > 0:
            self.tree.set_context('perceived_props', perceived_props)
            return Success
        else:
            return Failure


class IsPropAgarrable(Leaf):
    def process(self):
        props = [prop for prop in self.tree.get_context('perceived_props') if prop.prop_type == "Agarrable"]
        if len(props) > 0:
            self.tree.set_context('perceived_props', props)
            return Success
        else:
            return Failure


class IsPropOperable(Leaf):
    def process(self):
        props = [prop for prop in self.tree.get_context('perceived_props') if prop.prop_type == "Operable"]
        if len(props) > 0:
            self.tree.set_context('perceived_props', props)
            return Success
        else:
            return Failure


class IsPropScenery(Leaf):
    def process(self):
        interactive = ["Agarrable", "Operable"]
        props = [prop for prop in self.tree.get_context('perceived_props') if prop.prop_type not in interactive]
        if len(props) > 0:
            self.tree.set_context('perceived_props', props)
            return Success
        else:
            return Failure


class IsHeSeeingaMob(Leaf):
    def process(self):
        entity = self.get_entity()
        preception = entity.perceived
        sprites = set(preception['seen'])
        perceived_mobs = []
        for sprite in sprites:
            if sprite.tipo == 'Mob':
                perceived_mobs.append(sprite)

        if len(perceived_mobs) > 0:
            self.tree.set_context('perceived_mobs', perceived_mobs)
            return Success
        else:
            return Failure


class IsHeInCombatPosition(Leaf):
    def process(self):
        entity = self.get_entity()
        if entity.estado == 'cmb':
            return Success
        else:
            return Failure


class HasSomethingToSay(Leaf):
    def process(self):
        return Success


class IsTargetClose(Leaf):
    def process(self):
        entity = self.get_entity()
        props, mobs = 'perceived_props', 'perceived_mobs'
        context = self.tree.get_context
        targets = [prop for prop in context(props, default_value=[])] + [mob for mob in context(mobs, default_value=[])]
        ex, ey = entity.rect.center
        close = [[q, sqrt((q.rect.x - ex) ** 2 + (q.rect.y - ey) ** 2)] for q in targets]
        if len(close):
            distances = [i[1] for i in close]
            close_targets = [i[0] for i in close]
            dist_idx = distances.index(min(distances))
            sprite = close_targets[dist_idx]
            self.tree.set_context('close', sprite)
            return Success
        else:
            return Failure


class SetTarget(Leaf):
    def process(self):
        target = self.tree.get_context('close')
        ai = self.tree.get_context('base_ai_set')
        ai.set_target(target)
        return Success
"""
The SkillDecisionTree class for A2.

You are to implement the pick_skill() method in SkillDecisionTree, as well as
implement create_default_tree() such that it returns the example tree used in
a2.pdf.

This tree will be used during the gameplay of a2_game, but we may test your
SkillDecisionTree with other examples.
"""
from typing import Callable, List
from a2_skills import MageAttack, MageSpecial, RogueAttack, RogueSpecial


class SkillDecisionTree:
    """
    A class representing the SkillDecisionTree used by Sorcerer's in A2.
    
    value - the skill that this SkillDecisionTree contains.
    condition - the function that this SkillDecisionTree will check.
    priority - the priority number of this SkillDecisionTree.
               You may assume priority numbers are unique (i.e. no two
               SkillDecisionTrees will have the same number.)
    children - the subtrees of this SkillDecisionTree.
    """
    value: 'Skill'
    condition: Callable[['Character', 'Character'], bool]
    priority: int
    children: List['SkillDecisionTree']
    
    def __init__(self, value: 'Skill', 
                 condition: Callable[['Character', 'Character'], bool],
                 priority: int,
                 children: List['SkillDecisionTree'] = None)-> None:
        """
        Initialize this SkillDecisionTree with the value value, condition
        function condition, priority number priority, and the children in
        children, if provided.
        
        >>> from a2_skills import MageAttack
        >>> def f(caster, target):
        ...     return caster.hp > 50
        >>> t = SkillDecisionTree(MageAttack(), f, 1)
        >>> t.priority
        1
        >>> type(t.value) == MageAttack
        True
        """
        self.value = value
        self.condition = condition
        self.priority = priority
        self.children = children[:] if children else []
    
    # Implement a method called pick_skill which takes in a caster and target
    # and returns a skill.
    def pick_skill_helper(self, caster: 'Character', target: 'Character')\
            -> List:
        """
        return list of skills for the character caster
        :param caster:The character using the skill return
        :param target:The character the skill is applied to.
        :return: returns a tuple of options for usable skills
        >>> from a2_characters import Mage, Rogue
        >>> from a2_battle_queue import BattleQueue
        >>> from a2_playstyle import *
        >>> from a2_skills import Skill
        >>> bq = BattleQueue()
        >>> ps = ManualPlaystyle(bq)
        >>> r = Rogue('r', bq, ps)
        >>> m = Mage('m', bq, ps)
        >>> m.enemy, r.enemy = r, m
        >>> m.set_hp(100)
        >>> m.set_sp(40)
        >>> r.set_hp(50)
        >>> r.set_sp(30)
        >>> tree = create_default_tree()
        >>> picked_skills = tree.pick_skill_helper(m, r)
        >>> all([isinstance(item, SkillDecisionTree) for item in tree.pick_skill_helper(r, m)])
        True
        """
        if not self.condition(caster, target) or self.children == []:
            return [self]
        return sum([child.pick_skill_helper(caster, target) for child in
                    self.children], [])

    def pick_skill(self, caster: 'Character', target: 'Character')-> 'Skill':
        """
        return a skill with lowest priority for character caster
        :param caster: The character using the returned skill
        :param target: The character the damage of the skill is applied to
        :return: return a skill for character caster
        >>> from a2_characters import Mage, Rogue
        >>> from a2_battle_queue import BattleQueue
        >>> from a2_playstyle import *
        >>> from a2_skills import Skill
        >>> bq = BattleQueue()
        >>> ps = ManualPlaystyle(bq)
        >>> r = Rogue('r', bq, ps)
        >>> m = Mage('m', bq, ps)
        >>> m.enemy, r.enemy = r, m
        >>> m.set_hp(100)
        >>> m.set_sp(40)
        >>> r.set_hp(50)
        >>> r.set_sp(30)
        >>> tree = create_default_tree()
        >>> picked_skill = tree.pick_skill(m, r)
        >>> isinstance(picked_skill, Skill)
        True
        """
        first_skill = self.pick_skill_helper(caster, target)[0]
        for skill in self.pick_skill_helper(caster, target):
            if skill.priority < first_skill.priority:
                first_skill = skill
        return first_skill.value




def create_default_tree() -> 'SkillDecisionTree':
    """
    Return a SkillDecisionTree that matches the one described in a2.pdf.
    
    >>> tree = create_default_tree()
    >>> from a2_characters import Mage, Rogue
    >>> from a2_battle_queue import BattleQueue
    >>> from a2_playstyle import *
    >>> from a2_skills import *
    >>> bq = BattleQueue()
    >>> ps = ManualPlaystyle(bq)
    >>> r = Rogue('r', bq, ps)
    >>> m = Mage('m', bq, ps)
    >>> m.enemy, r.enemy = r, m
    >>> m.set_hp(100)
    >>> m.set_sp(40)
    >>> r.set_hp(50)
    >>> r.set_sp(30)
    >>> tree = create_default_tree()
    >>> picked_skill = tree.pick_skill(m, r)
    >>> isinstance(picked_skill, MageSpecial)
    True
    >>> m.set_hp(80)
    >>> m.set_sp(40)
    >>> r.set_hp(20)
    >>> r.set_sp(50)
    >>> picked_skill = tree.pick_skill(m, r)
    >>> isinstance(picked_skill, RogueAttack)
    True
    """
    # TODO: Return a SkillDecisionTree that matches the one in a2.pdf.
    t6 = SkillDecisionTree(RogueAttack(), f6, 8)
    t7 = SkillDecisionTree(RogueSpecial(), f6, 7)
    t4 = SkillDecisionTree(RogueAttack(), f4, 1, [t7])
    t8 = SkillDecisionTree(RogueAttack(), f6, 6)
    t5 = SkillDecisionTree(RogueSpecial(), f5, 4, [t8])
    t3 = SkillDecisionTree(MageSpecial(), f3, 2, [t6])
    t2 = SkillDecisionTree(MageAttack(), f2, 3, [t5])
    t9 = SkillDecisionTree(MageAttack(), f1, 5, [t2, t3, t4])
    return t9


def f1(caster: 'Character', _: 'Character')-> bool:
    """
    return True if caster's hp > 50
    :param caster: The caster of the skill in pick skill
    :param _: The target of the skill
    :return: return True or False
    >>> from a2_characters import Mage, Rogue
    >>> from a2_battle_queue import BattleQueue
    >>> from a2_playstyle import *
    >>> bq = BattleQueue()
    >>> ps = ManualPlaystyle(bq)
    >>> r = Rogue('r', bq, ps)
    >>> m = Mage('m', bq, ps)
    >>> m.enemy, r.enemy = r, m
    >>> m.set_hp(10)
    >>> m.set_sp(40)
    >>> r.set_hp(50)
    >>> r.set_sp(30)
    >>> f1(m, r)
    False
    """
    return caster.get_hp() > 50


def f2(caster: 'Character', _: 'Character')-> bool:
    """
    return True if caster's SP > 20
    :param caster: The caster of the skill in pick skill
    :param _: The target of the skill
    :return: return True or False
    >>> from a2_characters import Mage, Rogue
    >>> from a2_battle_queue import BattleQueue
    >>> from a2_playstyle import *
    >>> bq = BattleQueue()
    >>> ps = ManualPlaystyle(bq)
    >>> r = Rogue('r', bq, ps)
    >>> m = Mage('m', bq, ps)
    >>> m.enemy, r.enemy = r, m
    >>> m.set_hp(100)
    >>> m.set_sp(40)
    >>> r.set_hp(50)
    >>> r.set_sp(30)
    >>> f2(m, r)
    True
    """
    return caster.get_sp() > 20


def f3(_: 'Character', target: 'Character')-> bool:
    """
    return True if target's SP > 40
    :param _: The caster of the skill in pick skill
    :param target: The target of the skill
    :return: return True or False
    >>> from a2_characters import Mage, Rogue
    >>> from a2_battle_queue import BattleQueue
    >>> from a2_playstyle import *
    >>> bq = BattleQueue()
    >>> ps = ManualPlaystyle(bq)
    >>> r = Rogue('r', bq, ps)
    >>> m = Mage('m', bq, ps)
    >>> m.enemy, r.enemy = r, m
    >>> m.set_hp(100)
    >>> m.set_sp(40)
    >>> r.set_hp(40)
    >>> r.set_sp(30)
    >>> f3(m, r)
    False
    """
    return target.get_sp() > 40


def f4(caster: 'Character', _: 'Character')-> bool:
    """
    return True if caster's HP > 90
    :param caster: The caster of the returned skill
    :param _: The target of the skill returned
    :return: return True or False
    >>> from a2_characters import Mage, Rogue
    >>> from a2_battle_queue import BattleQueue
    >>> from a2_playstyle import *
    >>> bq = BattleQueue()
    >>> ps = ManualPlaystyle(bq)
    >>> r = Rogue('r', bq, ps)
    >>> m = Mage('m', bq, ps)
    >>> m.enemy, r.enemy = r, m
    >>> m.set_hp(100)
    >>> m.set_sp(40)
    >>> r.set_hp(50)
    >>> r.set_sp(30)
    >>> f4(m, r)
    True
    """
    return caster.get_hp() > 90


def f5(_: 'Character', target: 'Character')-> bool:
    """
    return True if target's HP < 30
    :param _: The caster of the returned skill
    :param target: The target of the skill returned
    :return: Return True or False
    >>> from a2_characters import Mage, Rogue
    >>> from a2_battle_queue import BattleQueue
    >>> from a2_playstyle import *
    >>> bq = BattleQueue()
    >>> ps = ManualPlaystyle(bq)
    >>> r = Rogue('r', bq, ps)
    >>> m = Mage('m', bq, ps)
    >>> m.enemy, r.enemy = r, m
    >>> m.set_hp(100)
    >>> m.set_sp(40)
    >>> r.set_hp(20)
    >>> r.set_sp(30)
    >>> f5(m, r)
    True
    """
    return target.get_hp() < 30


def f6(_: 'Character', __: 'Character')-> bool:
    """
    return False
    :param _: The caster of the skill
    :param __: The Target of the skill
    :return: return False
    >>> from a2_characters import Mage, Rogue
    >>> from a2_battle_queue import BattleQueue
    >>> from a2_playstyle import *
    >>> bq = BattleQueue()
    >>> ps = ManualPlaystyle(bq)
    >>> r = Rogue('r', bq, ps)
    >>> m = Mage('m', bq, ps)
    >>> m.enemy, r.enemy = r, m
    >>> m.set_hp(100)
    >>> m.set_sp(40)
    >>> r.set_hp(50)
    >>> r.set_sp(30)
    >>> f6(r, m)
    False
    """
    return False


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config='a2_pyta.txt')
    from doctest import testmod
    testmod()

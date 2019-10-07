"""
The Playstyle classes for A2.
Docstring examples are not required for Playstyles.

You are responsible for implementing the get_state_score function, as well as
creating classes for both Iterative Minimax and Recursive Minimax.
"""
from typing import Any, Union
import random


class Playstyle:
    """
    The Playstyle superclass.

    is_manual - Whether the class is a manual Playstyle or not.
    battle_queue - The BattleQueue corresponding to the game this Playstyle is
                   being used in.
    """
    is_manual: bool
    battle_queue: 'BattleQueue'

    def __init__(self, battle_queue: 'BattleQueue') -> None:
        """
        Initialize this Playstyle with BattleQueue as its battle queue.
        """
        self.battle_queue = battle_queue
        self.is_manual = True

    def select_attack(self, parameter: Any = None) -> str:
        """
        Return the attack for the next character in this Playstyle's
        battle_queue to perform.

        Return 'X' if a valid move cannot be found.
        """
        raise NotImplementedError

    def copy(self, new_battle_queue: 'BattleQueue') -> 'Playstyle':
        """
        Return a copy of this Playstyle which uses the BattleQueue
        new_battle_queue.
        """
        raise NotImplementedError


class ManualPlaystyle(Playstyle):
    """
    The ManualPlaystyle. Inherits from Playstyle.
    """

    def select_attack(self, parameter: Any = None) -> str:
        """
        Return the attack for the next character in this Playstyle's
        battle_queue to perform.

        parameter represents a key pressed by a player.

        Return 'X' if a valid move cannot be found.
        """
        if parameter in ['A', 'S']:
            return parameter

        return 'X'

    def copy(self, new_battle_queue: 'BattleQueue') -> 'Playstyle':
        """
        Return a copy of this ManualPlaystyle which uses the
        BattleQueue new_battle_queue.
        """
        return ManualPlaystyle(new_battle_queue)


class RandomPlaystyle(Playstyle):
    """
    The Random playstyle. Inherits from Playstyle.
    """
    def __init__(self, battle_queue: 'BattleQueue') -> None:
        """
        Initialize this RandomPlaystyle with BattleQueue as its battle queue.
        """
        super().__init__(battle_queue)
        self.is_manual = False

    def select_attack(self, parameter: Any = None) -> str:
        """
        Return the attack for the next character in this Playstyle's
        battle_queue to perform.

        Return 'X' if a valid move cannot be found.
        """
        actions = self.battle_queue.peek().get_available_actions()

        if not actions:
            return 'X'

        return random.choice(actions)

    def copy(self, new_battle_queue: 'BattleQueue') -> 'Playstyle':
        """
        Return a copy of this RandomPlaystyle which uses the
        BattleQueue new_battle_queue.
        """
        return RandomPlaystyle(new_battle_queue)


def get_state_score(battle_queue: 'BattleQueue') -> int:
    """
    Return an int corresponding to the highest score that the next player in
    battle_queue can guarantee.

    For a state that's over, the score is the HP of the character who still has
    HP if the next player who was supposed to act is the winner. If the next
    player who was supposed to act is the loser, then the score is -1 * the
    HP of the character who still has HP. If there is no winner (i.e. there's
    a tie) then the score is 0.

    >>> from a2_battle_queue import BattleQueue
    >>> from a2_characters import Rogue, Mage
    >>> bq = BattleQueue()
    >>> r = Rogue("r", bq, ManualPlaystyle(bq))
    >>> m = Mage("m", bq, ManualPlaystyle(bq))
    >>> r.enemy = m
    >>> m.enemy = r
    >>> bq.add(r)
    >>> bq.add(m)
    >>> m.set_hp(3)
    >>> get_state_score(bq)
    100
    >>> r.set_hp(40)
    >>> get_state_score(bq)
    40
    >>> bq.remove()
    r (Rogue): 40/100
    >>> bq.add(r)
    >>> get_state_score(bq)
    -10
    """
    if battle_queue.is_over():
        if battle_queue.get_winner():
            return battle_queue.peek().get_hp() \
                if battle_queue.get_winner() == battle_queue.peek()\
                else -1 * battle_queue.get_winner().get_hp()
        return 0
    else:
        bq_copy1 = battle_queue.copy()
        bq_copy2 = battle_queue.copy()
        copy1_score = -42423232424
        copy2_score = -64545353434

        copy1_player = bq_copy1.peek()
        if bq_copy1.peek().is_valid_action('S'):
            bq_copy1.peek().special_attack()
            if bq_copy1.peek().get_available_actions() != []:
                bq_copy1.remove()
            player = bq_copy1.peek()
            copy1_score = get_state_score(bq_copy1) \
                if copy1_player == player else -1 * get_state_score(bq_copy1)

        copy2_player = bq_copy2.peek()
        if bq_copy2.peek().is_valid_action('A'):
            bq_copy2.peek().attack()
            if bq_copy2.peek().get_available_actions() != []:
                bq_copy2.remove()
            player2 = bq_copy2.peek()
            copy2_score = get_state_score(bq_copy2) if copy2_player == player2 \
                else -1 * get_state_score(bq_copy2)

        return max(copy2_score, copy1_score)


class RecursiveMinimax(Playstyle):
    """
    A class representing a recursive minimax class
    batte_queue: the battle_queue used in this RecursiveMinimax
    """
    battle_queue: 'BattleQueue'

    def __init__(self, battle_queue: 'BattleQueue')-> None:
        """
        Initialize this RecursiveMinimax
        :param battle_queue: the battle_queue for this minimax
        >>> from a2_battle_queue import BattleQueue
        >>> from a2_characters import Rogue, Mage
        >>> bq = BattleQueue()
        >>> r = Rogue("r", bq, RecursiveMinimax(bq))
        >>> m = Mage("m", bq, RecursiveMinimax(bq))
        >>> r.enemy = m
        >>> m.enemy = r
        >>> bq.add(r)
        >>> bq.add(m)
        >>> m.set_hp(3)
        >>> mr = RecursiveMinimax(bq)
        >>> mr.battle_queue
        r (Rogue): 100/100 -> m (Mage): 3/100
        """
        super().__init__(battle_queue)
        self.is_manual = False

    def select_attack(self, parameter: Any = None)-> str:
        """
        Return move corresponding to the one that guarantees the highest
        score that the next player in battle_queue of self.
        :param parameter: the key pressed by user
        :return: return an attack
        :rtype: str
        >>> from a2_battle_queue import BattleQueue
        >>> from a2_characters import Rogue, Mage
        >>> bq = BattleQueue()
        >>> r = Rogue("r", bq, RecursiveMinimax(bq))
        >>> m = Mage("m", bq, RecursiveMinimax(bq))
        >>> r.enemy = m
        >>> m.enemy = r
        >>> bq.add(r)
        >>> bq.add(m)
        >>> m.set_hp(3)
        >>> m.playstyle.select_attack()
        'A'
        >>> r.set_hp(40)
        >>> bq.remove()
        r (Rogue): 40/100
        >>> bq.add(r)
        >>> r.playstyle.select_attack()
        'S'
        """
        copy1 = self.battle_queue.copy()
        copy2 = self.battle_queue.copy()
        copy1_score = -5445543
        copy2_score = -6476444

        player = copy1.peek()
        if copy1.peek().is_valid_action('A'):
            copy1.peek().attack()
            if copy1.peek().get_available_actions() != []:
                copy1.remove()
            current_player = copy1.peek()
            copy1_score = get_state_score(copy1) if \
                player == current_player else -1 * get_state_score(copy1)

        player2 = copy2.peek()
        if copy2.peek().is_valid_action('S'):
            copy2.peek().special_attack()
            if copy2.peek().get_available_actions() != []:
                copy2.remove()
            current_player2 = copy2.peek()
            copy2_score = get_state_score(copy2) if \
                player2 == current_player2 else -1 * get_state_score(copy2)
        best_score = max(copy2_score, copy1_score)
        return 'A' if best_score == copy1_score else \
            'S' if best_score == copy2_score else 'X'

    def copy(self, new_battle_queue: 'BattleQueue') -> 'Playstyle':
        """
        Return a copy of this RecursiveMinimax which uses the
        BattleQueue new_battle_queue.
        >>> from a2_battle_queue import BattleQueue
        >>> from a2_characters import Rogue, Mage
        >>> bq = BattleQueue()
        >>> r = Rogue("r", bq, IterativeMinimax(bq))
        >>> m = Mage("m", bq, IterativeMinimax(bq))
        >>> r.enemy = m
        >>> m.enemy = r
        >>> bq.add(r)
        >>> bq.add(m)
        >>> mr = RecursiveMinimax(bq)
        >>> mr.battle_queue
        r (Rogue): 100/100 -> m (Mage): 100/100
        >>> bq_copy = bq.copy()
        >>> mr_copy = mr.copy(bq_copy)
        >>> mr.battle_queue
        r (Rogue): 100/100 -> m (Mage): 100/100
        """
        return RecursiveMinimax(new_battle_queue)


class Tree:
    """
    a class representing a tree
    state - the state of the battle_queue of this tree
    score - score of the game of this tree
    children - children reached from the state of this tree
    """
    state: int
    children: Union[None, 'Tree']
    score: Union[None, int]

    def __init__(self, state, children: Union[None, 'Tree'] = None,
                 score: Union[None, int] = None)-> None:
        """
        Initialize this Tree
        :param state: The battle_queue of this tree
        :param children: The trees reachable from this tree
        :param score: the score of this tree
        >>> from a2_battle_queue import BattleQueue
        >>> from a2_characters import Mage, Rogue
        >>> bq = BattleQueue()
        >>> ps = ManualPlaystyle(bq)
        >>> r = Rogue('r', bq, ps)
        >>> m = Mage('m', bq, ps)
        >>> m.enemy, r.enemy = r, m
        >>> bq.add(m)
        >>> bq.add(r)
        >>> tree = Tree(bq)
        >>> tree.score is None
        True
        >>> tree.children is None
        True
        >>> tree.state
        m (Mage): 100/100 -> r (Rogue): 100/100
        """
        self.state = state
        self.children = children
        self.score = score

# helper function created due too many nested if statements


def removed_helper(removed: 'Tree')-> 'Tree':
    """
    return removed with its children filled out
    :param removed: a tree containing a state with with possible actions
    :return: return removed with its children filled out
    >>> from a2_battle_queue import BattleQueue
    >>> bq = BattleQueue()
    >>> from a2_characters import Mage, Rogue
    >>> ps = ManualPlaystyle(bq)
    >>> r = Rogue('r', bq, ps)
    >>> m = Mage('m', bq, ps)
    >>> m.enemy, r.enemy = r, m
    >>> bq.add(r)
    >>> bq.add(m)
    >>> tree = Tree(bq)
    >>> tree.score is None and tree.children is None
    True
    >>> tree = removed_helper(tree)
    >>> tree.children is None
    False
    """
    removed.children = []
    if removed.state.peek().is_valid_action('A'):
        copy1 = Tree(removed.state.copy())
        copy1.state.peek().attack()
        if copy1.state.peek().get_available_actions() != []:
            copy1.state.remove()
        removed.children.append(copy1)

    if removed.state.peek().is_valid_action('S'):
        copy2 = Tree(removed.state.copy())
        copy2.state.peek().special_attack()
        if copy2.state.peek().get_available_actions() != []:
            copy2.state.remove()
        removed.children.append(copy2)
    return removed


def iterative_get_score(battle_queue: 'BattleQueue')-> int:
    """
    Return an int corresponding to the highest score that the next player in
    battle_queue can guarantee.

    For a state that's over, the score is the HP of the character who still has
    HP if the next player who was supposed to act is the winner. If the next
    player who was supposed to act is the loser, then the score is -1 * the
    HP of the character who still has HP. If there is no winner (i.e. there's
    a tie) then the score is 0.

    >>> from a2_battle_queue import BattleQueue
    >>> from a2_characters import Rogue, Mage
    >>> bq = BattleQueue()
    >>> r = Rogue("r", bq, ManualPlaystyle(bq))
    >>> m = Mage("m", bq, ManualPlaystyle(bq))
    >>> r.enemy = m
    >>> m.enemy = r
    >>> bq.add(r)
    >>> bq.add(m)
    >>> m.set_hp(3)
    >>> iterative_get_score(bq)
    100
    >>> r.set_hp(40)
    >>> iterative_get_score(bq)
    40
    >>> bq.remove()
    r (Rogue): 40/100
    >>> bq.add(r)
    >>> iterative_get_score(bq)
    -10
    """
    state = Tree(battle_queue.copy())
    stack = [state]

    while stack:
        removed = stack.pop()
        if removed.state.is_over():
            if removed.state.get_winner():
                removed.score = removed.state.peek().get_hp() if\
                    removed.state.get_winner() == removed.state.peek() else \
                    -1 * removed.state.get_winner().get_hp()
            else:
                removed.score = 0
        elif not removed.children:
            removed = removed_helper(removed)
            stack.append(removed)
            for child in removed.children:
                stack.append(child)
        else:
            player = removed.state.peek()
            removed.score = max([child.score if type(child.state.peek())
                                 == type(player) else -1 * child.score for
                                 child in removed.children])
    return state.score


class IterativeMinimax(Playstyle):
    """
    class for an IterativeMinimax playstyle.
    battle_queue: battle_queue used in this playstyle
    """
    battle_queue: 'BattleQueue'
    def __init__(self, battle_queue: 'BattleQueue')-> None:
        """
        Initialize this IterativeMinimax
        :param battle_queue: the battle_queue for this minimax
        >>> from a2_battle_queue import BattleQueue
        >>> from a2_characters import Rogue, Mage
        >>> bq = BattleQueue()
        >>> r = Rogue("r", bq, IterativeMinimax(bq))
        >>> m = Mage("m", bq, IterativeMinimax(bq))
        >>> r.enemy = m
        >>> m.enemy = r
        >>> bq.add(r)
        >>> bq.add(m)
        >>> m.set_hp(3)
        >>> mi = IterativeMinimax(bq)
        >>> mi.battle_queue
        r (Rogue): 100/100 -> m (Mage): 3/100
        """
        super().__init__(battle_queue)
        self.is_manual = False

    def select_attack(self, parameter: Any = None)-> str:
        """
        Return move corresponding to the one that guarantees the highest
        score that the next player in battle_queue of self.
        :param parameter: the key pressed by user
        :return: return an attack
        :rtype: str
        >>> from a2_battle_queue import BattleQueue
        >>> from a2_characters import Rogue, Mage
        >>> bq = BattleQueue()
        >>> r = Rogue("r", bq, IterativeMinimax(bq))
        >>> m = Mage("m", bq, IterativeMinimax(bq))
        >>> r.enemy = m
        >>> m.enemy = r
        >>> bq.add(r)
        >>> bq.add(m)
        >>> m.set_hp(3)
        >>> m.playstyle.select_attack()
        'A'
        >>> r.set_hp(40)
        >>> bq.remove()
        r (Rogue): 40/100
        >>> bq.add(r)
        >>> r.playstyle.select_attack()
        'S'
        """
        copy1 = self.battle_queue.copy()
        copy2 = self.battle_queue.copy()
        copy1_score = -5445543
        copy2_score = -6476444

        player = copy1.peek()
        if copy1.peek().is_valid_action('A'):
            copy1.peek().attack()
            if copy1.peek().get_available_actions() != []:
                copy1.remove()
            current_player = copy1.peek()
            copy1_score = iterative_get_score(copy1) if \
                player == current_player else -1 * iterative_get_score(copy1)

        player2 = copy2.peek()
        if copy2.peek().is_valid_action('S'):
            copy2.peek().special_attack()
            if copy2.peek().get_available_actions() != []:
                copy2.remove()
            current_player2 = copy2.peek()
            copy2_score = iterative_get_score(copy2) if\
                player2 == current_player2 else -1 * iterative_get_score(copy2)
        best_score = max(copy2_score, copy1_score)
        return 'A' if  best_score == copy1_score else \
            'S' if best_score == copy2_score else 'X'

    def copy(self, new_battle_queue: 'BattleQueue')-> 'BattleQueue':
        """
        return a copy of this IterativeMinimax which uses this
        new_battle_queue as its battle_queue.
        >>> from a2_battle_queue import BattleQueue
        >>> from a2_characters import Rogue, Mage
        >>> bq = BattleQueue()
        >>> r = Rogue("r", bq, IterativeMinimax(bq))
        >>> m = Mage("m", bq, IterativeMinimax(bq))
        >>> r.enemy = m
        >>> m.enemy = r
        >>> bq.add(r)
        >>> bq.add(m)
        >>> mi = IterativeMinimax(bq)
        >>> mi.battle_queue
        r (Rogue): 100/100 -> m (Mage): 100/100
        >>> bq_copy = bq.copy()
        >>> mi_copy = mi.copy(bq_copy)
        >>> mi.battle_queue
        r (Rogue): 100/100 -> m (Mage): 100/100
        """
        return IterativeMinimax(new_battle_queue)


if __name__ == '__main__':
    from doctest import testmod
    testmod()
    import python_ta
    python_ta.check_all(config='a2_pyta.txt')

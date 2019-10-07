"""
The BattleQueue classes for A2.

A BattleQueue is a queue that lets our game know in what order various 
characters are going to attack.

BattleQueue has been completed for you, and the class header for 
RestrictedBattleQueue has been provided. You must implement
RestrictedBattleQueue and document it accordingly.
"""
from typing import Union

class BattleQueue:
    """
    A class representing a BattleQueue.
    """
    
    def __init__(self) -> None:
        """
        Initialize this BattleQueue.
        
        >>> bq = BattleQueue()
        >>> bq.is_empty()
        True
        """
        self._content = []
        self._p1 = None
        self._p2 = None
    
    def _clean_queue(self) -> None:
        """
        Remove all characters from the front of the Queue that don't have
        any actions available to them.
        
        >>> bq = BattleQueue()
        >>> from a2_characters import Rogue
        >>> from a2_playstyle import ManualPlaystyle
        >>> c = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c2 = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> bq.add(c)
        >>> bq.add(c2)
        >>> bq.is_empty()
        False
        """
        while self._content and self._content[0].get_available_actions() == []:
            self._content.pop(0)
    
    def add(self, character: 'Character') -> None:
        """
        Add character to this BattleQueue.
        
        >>> bq = BattleQueue()
        >>> from a2_characters import Rogue
        >>> from a2_playstyle import ManualPlaystyle
        >>> c = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c2 = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> bq.add(c)
        >>> bq.is_empty()
        False
        """
        self._content.append(character)
        
        if not self._p1:
            self._p1 = character
            self._p2 = character.enemy

    def remove(self) -> 'Character':
        """
        Remove and return the character at the front of this BattleQueue.

        >>> bq = BattleQueue()
        >>> from a2_characters import Rogue
        >>> from a2_playstyle import ManualPlaystyle
        >>> c = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c2 = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> bq.add(c)
        >>> bq.remove()
        Sophia (Rogue): 100/100
        >>> bq.is_empty()
        True
        """
        self._clean_queue()

        return self._content.pop(0)

    def is_empty(self) -> bool:
        """
        Return whether this BattleQueue is empty (i.e. has no players or
        has no players that can perform any actions).

        >>> bq = BattleQueue()
        >>> bq.is_empty()
        True
        """
        self._clean_queue()

        return self._content == []

    def peek(self) -> 'Character':
        """
        Return the character at the front of this BattleQueue but does not
        remove them.

        If this BattleQueue is empty, returns the first player who was added
        to this BattleQueue.

        >>> bq = BattleQueue()
        >>> from a2_characters import Rogue
        >>> from a2_playstyle import ManualPlaystyle
        >>> c = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c2 = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> bq.add(c)
        >>> bq.peek()
        Sophia (Rogue): 100/100
        >>> bq.is_empty()
        False
        """
        self._clean_queue()

        if self._content:
            return self._content[0]

        return self._p1

    def is_over(self) -> bool:
        """
        Return whether the game being carried out in this BattleQueue is over
        or not.

        A game is considered over if:
            - Both players have no skills that they can use.
            - One player has 0 HP
            or
            - The BattleQueue is empty.

        >>> bq = BattleQueue()
        >>> bq.is_over()
        True

        >>> from a2_characters import Rogue
        >>> from a2_playstyle import ManualPlaystyle
        >>> c = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c2 = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> bq.add(c)
        >>> bq.is_over()
        False
        """
        if self.is_empty():
            return True

        if self._p1.get_hp() == 0 or self._p2.get_hp() == 0:
            return True

        return False

    def get_winner(self) -> Union['Character', None]:
        """
        Return the winner of the game being carried out in this BattleQueue
        if the game is over. Otherwise, return None.

        >>> bq = BattleQueue()
        >>> from a2_characters import Rogue
        >>> from a2_playstyle import ManualPlaystyle
        >>> c = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c2 = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> bq.add(c)
        >>> bq.get_winner()
        """
        if not self.is_over():
            return None

        if self._p1.get_hp() == 0:
            return self._p2
        elif self._p2.get_hp() == 0:
            return self._p1

        return None

    def copy(self) -> 'BattleQueue':
        """
        Return a copy of this BattleQueue. The copy contains copies of the
        characters inside this BattleQueue, so any changes that rely on
        the copy do not affect this BattleQueue.

        >>> bq = BattleQueue()
        >>> from a2_characters import Rogue
        >>> from a2_playstyle import ManualPlaystyle
        >>> c = Rogue("r", bq, ManualPlaystyle(bq))
        >>> c2 = Rogue("r2", bq, ManualPlaystyle(bq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> bq.add(c)
        >>> bq.add(c2)
        >>> new_bq = bq.copy()
        >>> new_bq.peek().attack()
        >>> new_bq
        r (Rogue): 100/97 -> r2 (Rogue): 95/100 -> r (Rogue): 100/97
        >>> bq
        r (Rogue): 100/100 -> r2 (Rogue): 100/100
        """
        new_battle_queue = BattleQueue()

        p1_copy = self._p1.copy(new_battle_queue)
        p2_copy = self._p2.copy(new_battle_queue)
        p1_copy.enemy = p2_copy
        p2_copy.enemy = p1_copy

        new_battle_queue.add(p1_copy)
        if not new_battle_queue.is_empty():
            new_battle_queue.remove()
        
        for character in self._content:
            if character == self._p1:
                new_battle_queue.add(p1_copy)
            else:
                new_battle_queue.add(p2_copy)
        
        return new_battle_queue
    
    def __repr__(self) -> str:
        """
        Return a representation of this BattleQueue.
        
        >>> bq = BattleQueue()
        >>> from a2_characters import Rogue
        >>> from a2_playstyle import ManualPlaystyle
        >>> c = Rogue("r", bq, ManualPlaystyle(bq))
        >>> c2 = Rogue("r2", bq, ManualPlaystyle(bq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> bq.add(c)
        >>> bq.add(c2)
        >>> bq
        r (Rogue): 100/100 -> r2 (Rogue): 100/100
        """
        return " -> ".join([repr(character) for character in self._content])


class RestrictedBattleQueue(BattleQueue):
    """
    A class representing a RestrictedBattleQueue.
    
    Rules for a RestrictedBattleQueue:
    - The first time each character is added to the RestrictedBattleQueue,
      they're able to add.
      
    For the below, you may assume that the character at the front of the
    RestrictedBattleQueue is the one adding:
    - Characters that are added to the RestrictedBattleQueue by a character
      other than themselves cannot add.
      i.e. if the RestrictedBattleQueue looks like:
      Character order: A -> B
      Able to add:     Y    Y
      
      Then if A tried to add B to the RestrictedBattleQueue, it would look like:
      Character order: A -> B -> B
      Able to add:     Y    Y    N
    - Characters that have 2 copies of themselves in the RestrictedBattleQueue
      already that can add cannot add.
      i.e. if the RestrictedBattleQueue looks like:
      Character order: A -> A -> B
      Able to add:     Y    Y    Y
      
      Then if A tried to add themselves in, the RestrictedBattleQueue would
      look like:
      Character order: A -> A -> B -> A
      Able to add:     Y    Y    Y    N
      
      If we removed from the RestrictedBattleQueue and tried to add A in again,
      then it would look like:
      Character order: A -> B -> A -> A
      Able to add:     YS    Y    N    Y
    """
    # TODO: Implement the RestrictedBattleQueue class
    def __init__(self):
        """
        Initialize this RestrictedBattleQueue.

        >>> bq = RestrictedBattleQueue()
        >>> bq.is_empty()
        True
        """
        super().__init__()
        self._can_add = []

    def add(self, character: 'Character')-> None:
        """
        add character to the restricted battle queue self
        Remove and return the character at the front of this BattleQueue.

        >>> bq = RestrictedBattleQueue()
        >>> from a2_characters import Rogue
        >>> from a2_playstyle import ManualPlaystyle
        >>> c = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c2 = Rogue("Jen", bq, ManualPlaystyle(bq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> bq.add(c)
        >>> bq.add(c2)
        >>> bq
        Sophia (Rogue): 100/100 -> Jen (Rogue): 100/100
        >>> c.attack()
        >>> bq
        Sophia (Rogue): 100/97 -> Jen (Rogue): 95/100 -> Sophia (Rogue): 100/97
        >>> c.attack()
        >>> bq
        Sophia (Rogue): 100/94 -> Jen (Rogue): 90/100 -> Sophia (Rogue): 100/94 -> Sophia (Rogue): 100/94
        >>> bq.remove()
        Sophia (Rogue): 100/94
        >>> bq.remove()
        Jen (Rogue): 90/100
        >>> bq
        Sophia (Rogue): 100/94 -> Sophia (Rogue): 100/94
        >>> c.attack()
        >>> bq
        Sophia (Rogue): 100/91 -> Sophia (Rogue): 100/91 -> Sophia (Rogue): 100/91
        >>> bq.remove()
        Sophia (Rogue): 100/91
        >>> bq
        Sophia (Rogue): 100/91 -> Sophia (Rogue): 100/91
        >>> #we should not be able to add to bq at this point but the SP and/or HP changes
        >>> c.attack()
        >>> bq
        Sophia (Rogue): 100/88 -> Sophia (Rogue): 100/88
        """

        added_yes_count = 0
        for i in range(len(self._content)):

            if self._content[i] == character:
                if self._can_add[i] == 'yes':
                    added_yes_count += 1

        if self._content == []:
            super().add(character)
            self._can_add.append('yes')
        elif self._can_add[0] == 'no':
            pass
        elif character not in self._content:
            super().add(character)
            self._can_add.append('yes')
        elif character == self._content[0] and added_yes_count != 2:
            super().add(character)
            self._can_add.append('yes')
        else:
            super().add(character)
            self._can_add.append('no')

        if not self._p1:
            self._p1 = character
            self._p2 = character.enemy

    def remove(self)-> 'Character':
        """
        Remove and return the character at the front of this BattleQueue.

        >>> bq = RestrictedBattleQueue()
        >>> from a2_characters import Rogue
        >>> from a2_playstyle import ManualPlaystyle
        >>> c = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c2 = Rogue("Sophia", bq, ManualPlaystyle(bq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> bq.add(c)
        >>> bq.remove()
        Sophia (Rogue): 100/100
        >>> bq.is_empty()
        True
        """
        self._clean_queue()
        len_ = len(self._content)
        start = 1 + (len(self._can_add) - len_)
        self._can_add = self._can_add[start:]
        return super().remove()

    def copy(self)-> 'RestrictedBattleQueue':
        """
        Return a copy of this BattleQueue. The copy contains copies of the
        characters inside this BattleQueue, so any changes that rely on
        the copy do not affect this BattleQueue.

        >>> bq = RestrictedBattleQueue()
        >>> from a2_characters import Rogue
        >>> from a2_playstyle import ManualPlaystyle
        >>> c = Rogue("r", bq, ManualPlaystyle(bq))
        >>> c2 = Rogue("r2", bq, ManualPlaystyle(bq))
        >>> c.enemy = c2
        >>> c2.enemy = c
        >>> bq.add(c)
        >>> bq.add(c2)
        >>> new_bq = bq.copy()
        >>> new_bq.peek().attack()
        >>> new_bq
        r (Rogue): 100/97 -> r2 (Rogue): 95/100 -> r (Rogue): 100/97
        >>> bq
        r (Rogue): 100/100 -> r2 (Rogue): 100/100
        """
        new_battle_queue = RestrictedBattleQueue()
        p1_copy = self._p1.copy(new_battle_queue)
        p2_copy = self._p2.copy(new_battle_queue)
        p1_copy.enemy = p2_copy
        p2_copy.enemy = p1_copy
        new_battle_queue._p1 = p1_copy
        new_battle_queue._p2 = p2_copy
        our_list = []
        our_can_add = []

        for character in self._content:
            if character == self._p1:
                our_list.append(p1_copy)
            else:
                our_list.append(p2_copy)
        for can in self._can_add:
            our_can_add.append(can)
        new_battle_queue._content = our_list
        new_battle_queue._can_add = our_can_add

        return new_battle_queue


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config='a2_pyta.txt')
    from doctest import testmod
    testmod()

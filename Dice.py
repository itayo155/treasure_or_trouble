from enum import Enum
import numpy.random as rnd


class Dice_Values(Enum):
    SKULL = 0
    COIN = 1
    DIAMOND = 2
    PARROT = 3
    MONKEY = 4
    SWORD = 5


class Dices():
    def __init__(self, count=8):
        self.dice_count = count
        self.dice_values = [None] * count
        self.skulls_rerolled = 0

        self._all_dice_vals = [d for d in Dice_Values]

    def get_current(self):
        # return a copy
        return [x for x in self.dice_values]

    def get_current_as_str(self):
        # return a copy
        return [x.name for x in self.dice_values]

    def roll(self, indexes=None):
        if (indexes is None):
            indexes = range(self.dice_count)

        for idx in indexes:
            if (self.dice_values[idx] == Dice_Values.SKULL):
                self.skulls_rerolled += 1

            v = self._single_roll()
            self.dice_values[idx] = v

        return self

    def _single_roll(self):
        return self._all_dice_vals[rnd.choice(6)]

    def to_string(self):
        return '%s' % (str([x.name for x in self.get_current()]))

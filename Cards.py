from enum import Enum
from Dice import Dice_Values


class Card_Values(Enum):
    SORCERESS = 0
    PARROTS_AND_MONKEYS = 1
    CAPTAIN = 2
    SEA_BATTLE = 3
    COIN = 4
    DIAMOND = 5
    SKULL = 6
    TWO_SKULLS = 6
    CHEST = 7


class Cards():
    def __init__(self):
        self.card_to_dice = {Card_Values.COIN: [Dice_Values.COIN],
                             Card_Values.DIAMOND: [Dice_Values.DIAMOND],
                             Card_Values.SKULL: [Dice_Values.SKULL],
                             Card_Values.TWO_SKULLS: [Dice_Values.SKULL, Dice_Values.SKULL]}

    def to_dice_array(self, card):
        return self.card_to_dice.get(card, [])

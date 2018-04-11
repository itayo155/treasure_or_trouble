from Player import Player
import collections
from Dice import Dice_Values
from Cards import Card_Values, Cards

class Basic_Player(Player):
    def __init__(self, verbose=False):
        Player.__init__(self)
        
        self.dice_values = None
        self.effective_dice_values = None
        self.card = None
        self._verbose = verbose
        
    def init(self, current_dices, card):
        self.dice_values = current_dices
        self.card = card
        effective_dice_values = self.dice_values + Cards().to_dice_array(self.card)
        if (self.card == Card_Values.PARROTS_AND_MONKEYS):
            effective_dice_values = [Dice_Values.MONKEY if x == Dice_Values.PARROT else x for x in effective_dice_values]
        
        self.effective_dice_values = effective_dice_values
    
    def _valid_reroll(self, reroll):
        #ToDo: incorporate soreceress
        return len(reroll) != 1
    
    #return Noneor empty array to end turn
    def get_dices_to_roll(self, game_state):
        self.init(game_state.dice_values, game_state.card)
        reroll = []

        counts = collections.Counter(self.effective_dice_values)
        if (self._verbose):
            print('dbg: counts=%s' % (str(counts)))
        
        th = 3
        #ToDo: sorceress
        if (counts.get(Dice_Values.SKULL, 0) < 2):
            ungrouped = {k for k,v in counts.items() if v < th}
            if (self._verbose):
                print('dbg: ungrouped=%s' % (str(ungrouped)))
            reroll = [i for i,v in enumerate(self.dice_values) if ((v in ungrouped) and (v != Dice_Values.SKULL))]
        #else, 2 (or more...) skulls: don't reroll
        
        if (not self._valid_reroll(reroll)):
            reroll = []
        
        return reroll    

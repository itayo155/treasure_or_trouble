from Player import Player
from Dice import Dice_Values
import numpy.random as rnd


class Random_Player(Player):
    def __init__(self):
        Player.__init__(self)
        
        self._p_end_turn = 0.3
        self._p_reroll = 0.33
        return
    
    #return Noneor empty array to end turn
    def get_dices_to_roll(self, game_state):
        if (rnd.rand() < self._p_end_turn):
            return None
        
        valid_reroll = False
        while (not valid_reroll):
            reroll = [i for i,v in enumerate(game_state.dice_values) if ((v != Dice_Values.SKULL) and (rnd.rand() < self._p_reroll))]
            valid_reroll = True if (len(reroll) != 1) else False               
        
        return reroll
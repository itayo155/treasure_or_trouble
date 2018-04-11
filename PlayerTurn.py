from Scoring import Scoring
import collections
from Dice import Dice_Values
from Cards import Card_Values, Cards
from GameState import Game_State

class Player_Turn():
    def __init__(self, game, player_idx, verbose=False):
        self.game = game
        self.player = game.players[player_idx]
        self.card = game.get_card_from_deck()
        self.rolls = 0
        self._skull_rerolls_remaining = self.get_allowed_skull_rerolls()
        self._skulls_to_end_of_turn = 3
        self._verbose = verbose
        
        self.dice_history = []
        
    def get_allowed_skull_rerolls(self):
        if (self.card == Card_Values.SORCERESS):
            return 1
        
        return 0
    
    #i.e. with card
    def get_effective_dice_values(self):        
        return self.game.dices.get_current() + Cards().to_dice_array(self.card)
            
    def has_turn_ended(self):
        dice_values = self.get_effective_dice_values()
        dice_counts = collections.Counter(dice_values)
        
        if (dice_counts.get(Dice_Values.SKULL, 0) - self._skull_rerolls_remaining > self._skulls_to_end_of_turn):
            return True
        
        return False
        
    def count_reroll_skulls(self, to_reroll):
        dices = [x for i,x in enumerate(self.game.dices.get_current()) if i in to_reroll]
        return (collections.Counter(dices)).get(Dice_Values.SKULL, 0)
    
    #ToDo
    def is_valid_reroll(self, to_reroll):
        if ((to_reroll is None) or (len(to_reroll) == 0)):
            return True
        
        return ((len(to_reroll) != 1) and (self.count_reroll_skulls(to_reroll) <= self._skull_rerolls_remaining))
    
    def play(self):
        self.game.dices.roll()
        
        self.dice_history.append(self.game.dices.get_current_as_str())
        if (self._verbose):
            print("dice=%s" % (self.game.dices.get_current_as_str()))
        
        #ToDo: handle island-of-the-dead
        turn_ended = self.has_turn_ended()
        
        while (not turn_ended):
            if (self._verbose):
                print('dbg: roll %d' % (self.rolls))
            game_state = Game_State(self.game.dices.get_current(), self.card)
            to_reroll = self.player.get_dices_to_roll(game_state)
            
            if ((to_reroll is None) or (len(to_reroll) == 0)):
                if (self._verbose):
                    print('dbg: endo of turn by player')
                turn_ended = True
            if (self.is_valid_reroll(to_reroll)):
                self.game.dices.roll(to_reroll)
                self.dice_history.append(self.game.dices.get_current_as_str())
                if (self._verbose):
                    print("reroll=%s, dice=%s" % (str(to_reroll), self.game.dices.get_current_as_str()))
                self.rolls += 1
            else:
                if (self._verbose):
                    print('dbg: error: invalid request to reroll (%s), ending turn' % (str(to_reroll)))
                turn_ended = True
                
        #turn ended
        score = Scoring(self.game.dices.get_current(), self.card).score()
        
        return score
        
    
    def to_string(self):
        return 'card=%s, rolls = %d, history=%s' % (self.card.name, self.rolls, self.dice_history)
        
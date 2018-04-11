from Cards import Card_Values, Cards
from Dice import Dice_Values
import collections


class Scoring():
    def __init__(self, dice_values, card = None, dice_count = 8):
        
        self.dice_values = self._convert_dices_to_enum(dice_values)
        self.card = self._convert_card_to_enum(card)
        self._dice_count = dice_count
        
        self._scores_by_count = {3: 100, 4: 200, 5: 500, 6: 1000, 7: 2000, 8: 4000}
        self._full_chest = 500
        self._valuables = {Dice_Values.COIN: 100, Dice_Values.DIAMOND: 100}
        self._dice_used = set() #used for full-chest scoring
    
    def _convert_dices_to_enum(self, dice_values):
        return [x if x in Dice_Values else Dice_Values[x.upper()] for x in dice_values]
    
    def _convert_card_to_enum(self, card):
        if (card is None):
            return None
        
        return card if card in Card_Values else Card_Values[card.upper()]
        
    def _add_card_to_dice(self):
        return self.dice_values + Cards().to_dice_array(self.card)
        
    def is_disqualified(self):
        return len([x for x in self.dice_values if x == Dice_Values.SKULL]) >= 3
        
    def score(self):
        self.dice_values = self._add_card_to_dice()
        
        if (self.is_disqualified()):
            return 0
            
        score = self._score_by_groups() \
                + self._score_by_valuables() \
                + self._score_by_full_chest() \
                + self._score_by_sea_battle()
                
        
        coef = 2. if (self.card == Card_Values.CAPTAIN) else 1.
        
        return coef * score
    
    def _score_by_valuables(self):
        dice_used = {i for i,v in enumerate(self.dice_values) if v in self._valuables}
        self._dice_used |= dice_used
        
        return sum([self._valuables.get(x, 0) for x in self.dice_values])
    
    def _score_by_groups(self):
        
        if (self.card == Card_Values.PARROTS_AND_MONKEYS):
            self.dice_values = [Dice_Values.MONKEY if x == Dice_Values.PARROT else x for x in self.dice_values]
                    
        counts = collections.Counter(self.dice_values)
        groups_used = {k: v for k,v in counts.items() if v >= 3}
        dice_used = {i for i,v in enumerate(self.dice_values) if v in groups_used}
        self._dice_used |= dice_used        
        
        return sum([self._scores_by_count.get(v, 0) for k,v in counts.items()])
    
    #must be called after other scoring methods
    def _score_by_full_chest(self):
        if (len(self._dice_used) >= self._dice_count):
            return self._full_chest
        
        return 0
    
    #should be here? not sure.
    def _score_by_sea_battle(self):
        #ToDo
        return 0
        
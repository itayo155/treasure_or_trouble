from Cards import Card_Values
from Dice import Dices
from RandomPlayer import Random_Player
from Basic_Player import Basic_Player
import numpy.random as rnd


class Game():
    def __init__(self, players = 2, player_type='random'):        
        self._dice_count = 8
        
        self.player_count = players
        self.scores = [0] * players
        self.turn = 0
                
        self.dices = Dices(self._dice_count)
        self.players = self.create_players(players, player_type)
        
        self._goal = 8000
        self._current_player_rolls = 0
        
    def create_players(self, count, player_type):
        #ToDo: Factory
        #ToDo: different players
        if (player_type == 'random'):
            return [Random_Player() for x in range(count)]
        elif (player_type == 'basic'):
            return [Basic_Player() for x in range(count)]
        
    def get_card_from_deck(self):
        #ToDo: make it better
        card_values = [x for x in Card_Values]
        return card_values[rnd.choice(len(card_values))]
    
    def roll(self, indexes = None):
        return self.dices.roll(indexes)
    
    def to_string(self):
        return 'turns: %d, scores: %s' % (self.turn, self.scores)
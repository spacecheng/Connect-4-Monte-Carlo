'''
This is where all the bot stuff like the 
tables and choosing action will be defined
'''
import environment
import random
from environment import help_check_win

class rand_bot:
    name = "random"
    def act(board,heights,moveset):
        r = random.random
        move = moveset[int(r() * len(moveset))]
        return move
    
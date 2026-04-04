'''
This is where all the bot stuff like the 
tables and choosing action will be defined
'''
import environment
import random
from environment import help_check_win

class Node:
    def __init__(self, state, parent = None, move = None ):
        self.state = state
        self.parent = parent
        self.move = move
        self.children = []
        self.moves_left = state.valid_moves()
        

class rand_bot:
    name = "random"
    def act(board,heights,moveset):
        r = random.random
        move = moveset[int(r() * len(moveset))]
        return move
    
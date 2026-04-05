'''
This is where all the bot stuff like the 
tables and choosing action will be defined
'''
import environment
import random
from environment import help_check_win as check_win

class Node:
    def __init__(self, state, parent = None, move = None ):
        self.state = state
        self.parent = parent
        self.move = move
        self.children = []
        self.moves_left = state.valid_moves()
        

class rand_bot:
    name = "random"
    def __init__(self,game):
        self.game = game
    def act(self,state,heights,moveset):
        r = random.random
        move = moveset[int(r() * len(moveset))]
        return move
    
class smart_rand:
    name = "random+check"
    def __init__(self,game):
        self.game = game
    def act(self,state,heights,moveset):
        board, _, move_idx, _ = state
        win_cond = self.game.win_cond
        h = self.game.rows
        w = self.game.cols
        r = random.random
        for move in moveset:
            print(f"checking {move}")
            new_height =heights[move]
            move_idx = new_height*w + move
            print(f"mvidx = {move_idx}")
            res = check_win(win_cond,w,h,board,moveset,1,move,move_idx,new_height)
            print(f"result{res}")
            if res == 1:
                print("found win")
                return move
            res = check_win(win_cond,w,h,board,moveset,-1,move,move_idx,new_height)
            if res == 1:
                print("found loss")
                return move
        move = moveset[int(r() * len(moveset))]
        return move
    
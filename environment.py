'''
This is where game rules are defined. 
We will use a state machine like structure 
that returns the next state given 
current state and action taken
'''
class connect_4_game:
    def __init__(self, rows = 6, cols = 7, win_cond = 4):
        self.rows = rows
        self.cols = cols
        self.win_cond = win_cond
    def init_state(self, who_turn = 1):
        board = (0,) * self.rows * self.cols
        
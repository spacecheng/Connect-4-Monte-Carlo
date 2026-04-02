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
        cols = self.cols
        rows = self.rows
        board = (0,) * rows * cols
        heights = (0,) * cols
        last_move = None
        return board, heights, last_move, who_turn

    def display_board(self, board):
        r = self.rows
        c = self.cols
        #equivalent to len(boardlist) - col, -1, -col to loop reverse
        print(list(range(c)))
        for i in range(r*c - c, -1, -c):
            print(board[i:i+c])
    
    def move(self,board,mark,col):
        height = self.heights[col]
        move_ind = height*self.cols + col
        new_board = board[:move_ind] + mark + board[move_ind+1:]
        new_height = height[:col] + (height+1) + height[col+1:]
        return new_board, new_height
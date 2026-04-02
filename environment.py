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
    
    def move(self,board,heights,mark,col):
        height = heights[col]
        move_idx = height*self.cols + col
        new_board = board[:move_idx] + mark + board[move_idx+1:]
        col_height = height+1
        new_heights = heights[:col] + (col_height) + heights[col+1:]
        return new_board, new_heights, move_idx, col_height
    
    def check_win(self, board, heights, mv_mark, mv_col, mv_idx, mv_ht):
        win_cond = self.win_cond
        width = self.cols
        max_right = width - mv_col -1
        max_left = mv_col
        #vertical check
        if mv_ht >= win_cond:
            for i in range(1,win_cond):
                if(board[mv_idx - (i * width)] != mv_mark):
                    break
            else: #if no loop break
                return True
            
        #horizontal check
        aligned = 1
        for skew in range(1,min(win_cond,max_right+1)): #right check
            if board[mv_idx + skew] == mv_mark:
                aligned +=1
                if aligned >= win_cond:
                    return True
            else:
                break
        for skew in range(1,min(win_cond,max_left+1)):
            if board[mv_idx - skew] == mv_mark:
                aligned +=1
                if aligned >= win_cond:
                    return True
            else:
                break

        
                        
        
                 



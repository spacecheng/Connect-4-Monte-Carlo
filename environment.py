'''
This is where game rules are defined. 
We will use a state machine like structure 
that returns the next state given 
current state and action taken
'''
def help_check_win(win_cond, width, height, board, mv_mark, mv_col, mv_idx, mv_ht):
    max_right = width - mv_col
    max_left = mv_col + 1
    max_up =  height - mv_ht
    max_down = mv_ht + 1
    #vertical check
    if mv_ht >= win_cond:
        for i in range(1,win_cond):
            if(board[mv_idx - (i * width)] != mv_mark):
                break
        else: #if no loop break
            return True
        
    #horizontal check
    aligned = 1
    for skew in range(1,max_right): #right check
        if board[mv_idx + skew] == mv_mark:
            aligned +=1
        else: #no match
            break
    if aligned >= win_cond: #win found
        return True
    for skew in range(1,max_left):
        if board[mv_idx - skew] == mv_mark:
            aligned +=1
            if aligned >= win_cond: #win found before end of loop
                return True
        else: #no match
            break
    #diagonal checks
    aligned = 1
    #up-right check
    ur_lim = max_up if max_up < max_right else max_right
    for skew in range(1,ur_lim):
        if board[mv_idx + (skew * (width+1))] == mv_mark:
            aligned +=1
        else: #no match
            break
    #down-left check
    dl_lim = max_down if max_down < max_left else max_left
    for skew in range(1,dl_lim):
        if board[mv_idx - (skew * (width+1))] == mv_mark:
            aligned +=1
            if aligned >= win_cond: #win found before end of loop
                return True
        else: #no match
            break
    aligned = 1
    #up-left check
    ul_lim = max_up if max_up < max_left else max_left
    for skew in range(1,ul_lim):
        if board[mv_idx + (skew *width -1)] == mv_mark:
            aligned +=1
        else: # no match
            break
    if aligned >= win_cond:
        return True
    dr_lim = max_down if max_down < max_right else max_right
    for skew in range(1,dr_lim):
        if board[mv_idx - (skew * width -1)] ==mv_mark:
            aligned +=1
            if aligned >= win_cond:
                return True
        else: #no match
            break
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
        pad = len(str(max(board)))+2
        #equivalent to len(boardlist) - col, -1, -col to loop reverse
        print("".join(f"{c:>{pad}}" for c in list(range(c))) + "]")
        for i in range(r*c - c, -1, -c):
            row = board[i:i+c]
            print("".join(f"{mark:>{pad}}" for mark in row))

    
    def valid_moves(self,heights):
        moveset = [col for col in range(self.cols) if heights[col] < self.rows]
        return moveset
    
    def move(self,board,heights,mark,col):
        height = heights[col]
        move_idx = height*self.cols + col
        new_board = board[:move_idx] + (mark,) + board[move_idx+1:]
        col_height = height+1
        new_heights = heights[:col] + (col_height,) + heights[col+1:]
        return new_board, new_heights, move_idx, col_height
    
    def check_win(self, board, mv_mark, mv_col, mv_idx, mv_ht):
        return help_check_win(
            self.win_cond, self.cols, self.rows,
            board, mv_mark, mv_col, mv_idx, mv_ht
        )


        

        
                        
        
                 



'''
This is where game rules are defined. 
We will use a state machine like structure 
that returns the next state given 
current state and action taken
'''
def help_check_win(win_cond, width, height, board, moveset, mv_mark, mv_col, mv_idx, mv_ht):
    max_right = width - mv_col
    max_left = mv_col + 1
    max_up =  height - mv_ht
    max_down = mv_ht + 1
    #vertical check
    if mv_ht >= win_cond:
        print("vche", win_cond)
        for i in range(1,win_cond):
            print(f"vert {mv_idx} - {i} * {width}) = {mv_idx - (i * width)}")
            if(board[mv_idx - (i * width)] != mv_mark):
                print("testing", mv_idx - (i * width), "eee",board[mv_idx - (i * width)], "HHH", mv_mark)
                break
        else: #if no loop break
            #print("vrt win")
            return 1
        
    #horizontal check
    aligned = 1
    for skew in range(1,max_right): #right check
        #print(f"right {mv_idx} + {skew} = {mv_idx + skew}")
        if board[mv_idx + skew] == mv_mark:
            aligned +=1
        else: #no match
            break
    if aligned >= win_cond: #win found
        #print("horiz(r) win")
        return 1
    for skew in range(1,max_left):
        #print(f"left {mv_idx} - {skew} = {mv_idx -skew}")
        if board[mv_idx - skew] == mv_mark:
            aligned +=1
            if aligned >= win_cond: #win found before end of loop
                #print("horiz(l) win")
                return 1
        else: #no match
            break
    #diagonal checks
    aligned = 1
    #up-right check
    ur_lim = max_up if max_up < max_right else max_right
    for skew in range(1,ur_lim):
        #print(f"ur {mv_idx} + {skew} * {width} -1) = {mv_idx + (skew * (width+1))} ")
        if board[mv_idx + (skew * (width+1))] == mv_mark:
            aligned +=1
        else: #no match
            break
    if aligned >= win_cond: #win found
        #print("ur win")
        return 1
    #down-left check
    dl_lim = max_down if max_down < max_left else max_left
    for skew in range(1,dl_lim):
        #print(f"dl {mv_idx} - {skew} * {width} -1) ={mv_idx - (skew * (width+1))}")
        if board[mv_idx - (skew * (width+1))] == mv_mark:
            aligned +=1
            if aligned >= win_cond: #win found before end of loop
                #print("dl win")
                return 1
        else: #no match
            break
    aligned = 1
    #up-left check
    ul_lim = max_up if max_up < max_left else max_left
    for skew in range(1,ul_lim):
        pos = (mv_idx-skew)+(skew * width)
        #print(f"ul {mv_idx} +({skew} * {width}) = {pos}")
        if board[pos] == mv_mark:
            aligned +=1
        else: # no match
            break
    if aligned >= win_cond:
        #print("ul win")
        return 1
    #down-right chck
    dr_lim = max_down if max_down < max_right else max_right
    #print("lim",dr_lim)
    #print(f"move {mv_idx}")
    for skew in range(1,dr_lim):
        pos = (mv_idx+skew)-(skew * width)
        #print(f"dr {mv_idx}+{skew}-{skew * width}) = {pos}")
        if board[pos] ==mv_mark:
            if pos < 0:break
            aligned +=1
            if aligned >= win_cond:
                #print("dr win")
                return 1
        else: #no match
            break
    if len(moveset) == 1:
        #print("tie")
        return -1
    return 0
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
        marks = ["0","X","O"]
        for i in range(r*c - c, -1, -c):
            row = board[i:i+c]
            print("".join(f"{(marks[mark]):>{pad}}" for mark in row))

    
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
    
    def check_win(self, board, moveset, mv_mark, mv_col, mv_idx, mv_ht):
        return help_check_win(
            self.win_cond, self.cols, self.rows,
            board, moveset, mv_mark, mv_col, mv_idx, mv_ht
        )


        

        
                        
        
                 



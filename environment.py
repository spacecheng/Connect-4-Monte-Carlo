'''
This is where game rules are defined. 
We will use a state machine like structure 
that returns the next state given 
current state and action taken
'''
def help_check_win(win_cond, width, height, board, moveset, mv_mark, mv_col, mv_idx, mv_ht):
    row = mv_ht - 1
    cols, rows, wc = width, height, win_cond
    for dr, dc in ((0, 1), (1, 0), (1, 1), (1, -1)):
        count = 1
        for sign in (1, -1):
            r, c = row + dr * sign, mv_col + dc * sign
            while 0 <= r < rows and 0 <= c < cols and board[r * cols + c] == mv_mark:
                count += 1
                r += dr * sign
                c += dc * sign
        if count >= wc:
            return 1
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
        marks = ["-","X","O"]
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


        

        
                        
        
                 



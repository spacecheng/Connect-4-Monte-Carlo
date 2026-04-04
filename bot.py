'''
This is where all the bot stuff like the 
tables and choosing action will be defined
'''
import environment
import random
def check_win(self, board, heights, mv_mark, mv_col, mv_idx, mv_ht):
        win_cond = self.win_cond
        width = self.cols
        max_right = width - mv_col
        max_left = mv_col + 1
        max_up =  self.rows - mv_ht
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

class rand:
    def act(board,heights,moveset):
        r = random.random
        move = moveset[int(r() * len(moveset))]
        return move